"""
Functions and classes for detecting corruption of sctids and possible reconsructions
"""

import re
from enum import Enum
import logging

from pydantic import BaseModel, field_serializer, ConfigDict

from . import checkdigit
from .codes_in_release import (
    check_list_of_concept_ids_in_release_and_get_display,
    check_list_of_description_ids_in_release_and_get_concept_id_and_display,
)
from .parse_and_validate_sctid import ParsedSCTID

logger = logging.getLogger()


class OutcomeCodes(Enum):
    """An ENUM to contain the valid outcome_codes"""

    # fmt: off
    POSSIBLE_CORRUPTION_UNAMBIG      = "1:The sctid provided is invalid but can be reconstructed to a single form that is found in release"
    POSSIBLE_CORRUPTION_AMBIG        = "2:The sctid provided is invalid and can be reconstructed to both a concept id and a description id that is found in release???"
    POSSIBLE_CORRUPTION              = "3:This is a temporary outcome that indicates the sctid provided looks corrupted; should not occur once processing complete as is refined"
    ANY_CORRUPTION_IS_SILENT         = "4:The corrupted form is the same as the original, is in release, and there is no alternative reconstruction"
    AMBIG_COULD_BE_SILENT            = "5:The corrupted form is the same as the original, is in release, but there is also an alternative reconstruction"
    NOT_PURE_DIGITS                  = "8:The sctid provided does not contain pure digits"
    NOT_16_TO_18_DIGITS              = "6:The sctid provided is not 16-18 digits"
    NOT_TRAILING_ZEROES              = "7:The sctid provided is long enough to be corrupted but does not have the correct pattern of trailing zeroes"
    NOT_RECONSTRUCTABLE              = "9:The sctid provided has 16 digits but digit 15 is neither 0 nor 1"
    NO_RECONSTRUCTIONS_EXIST          = "10:The sctid provided looks like it may be corrupted but neither the original nor any reconstruction is in release"
    # fmt: on

    def to_dict(self):
        return {"name": "OutcomeCodes." + self.name, "value": self.value}


class CorruptionAnalysis(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    sctid_provided: str | None = None
    sctid_provided_stem: str | None = None
    sctid_provided_trailing_zeroes: str | None = None
    validity: bool | None = None
    outcome_code: OutcomeCodes | None = None
    r_cid: str | None = None
    r_cid_stem: str | None = None
    r_cid_trailing_zeroes: str | None = None
    r_did: str | None = None
    r_did_stem: str | None = None
    r_did_trailing_zeroes: str | None = None
    r_cid_pt: str | None = None
    r_did_term: str | None = None
    r_did_corresp_cid: str | None = None

    @field_serializer("outcome_code")
    def serialize_outcome_code(self, outcome_code: OutcomeCodes, _info):
        return outcome_code.to_dict()


def analyse_sctid_for_corruption(
    sctid=None,
) -> CorruptionAnalysis:
    """
    Works out if sctid may be corrupted and if so create possible restored forms
    No checking of releases is done here (so that release checking can be batched)
    """

    sctid = str(sctid)  # in case test with an int

    corruption_analysis = CorruptionAnalysis()
    corruption_analysis.sctid_provided = sctid
    corruption_analysis.validity = ParsedSCTID(
        string=sctid
    ).valid  # don't actually use this in this function
    # - it is for reporting in the front end

    # can't be excel corruption if not purely digits
    if (re.search(r"^[0-9]+$", sctid.strip())) is None:
        corruption_analysis.outcome_code = OutcomeCodes.NOT_PURE_DIGITS
        return corruption_analysis

    # can't be excel corruption if not purely digits
    if len(sctid) not in [16, 17, 18]:
        corruption_analysis.outcome_code = OutcomeCodes.NOT_16_TO_18_DIGITS
        return corruption_analysis

    n_digits = len(sctid)

    match n_digits:
        case 16:
            match sctid[-1]:
                case "0":
                    # match checkdigit.verhoeff_check(sctid):
                    #     case True:
                    #         corruption_analysis.outcome_code = (
                    #             OutcomeCodes.ANY_CORRUPTION_IS_SILENT_16_CHANGE
                    #         )
                    #         return corruption_analysis
                    #     case False:
                    match sctid[-2]:
                        case "0":
                            stem = sctid[:-1]
                            corruption_analysis.r_cid = stem + str(
                                checkdigit.verhoeff_compute(stem)
                            )
                        case "1":
                            stem = sctid[:-1]
                            corruption_analysis.r_did = stem + str(
                                checkdigit.verhoeff_compute(stem)
                            )
                        case _:
                            corruption_analysis.outcome_code = (
                                OutcomeCodes.NOT_RECONSTRUCTABLE
                            )
                            return corruption_analysis
                case _:
                    corruption_analysis.outcome_code = OutcomeCodes.NOT_TRAILING_ZEROES
                    return corruption_analysis

        case 17:
            match sctid[-2:]:
                case "00":
                    stem = sctid[:-2]
                    corruption_analysis.r_cid = (
                        stem + "0" + str(checkdigit.verhoeff_compute(stem + "0"))
                    )
                    corruption_analysis.r_did = (
                        stem + "1" + str(checkdigit.verhoeff_compute(stem + "1"))
                    )
                case _:
                    corruption_analysis.outcome_code = OutcomeCodes.NOT_TRAILING_ZEROES
                    return corruption_analysis
        case 18:
            match sctid[-3:]:
                case "000":
                    match sctid[:6]:
                        case "900000":
                            stem = sctid[:-3]
                            corruption_analysis.r_cid = (
                                stem
                                + "00"
                                + str(checkdigit.verhoeff_compute(stem + "00"))
                            )
                            corruption_analysis.r_did = (
                                stem
                                + "01"
                                + str(checkdigit.verhoeff_compute(stem + "01"))
                            )
                        case _:
                            stem = sctid[:-3]
                            corruption_analysis.r_cid = (
                                stem
                                + "10"
                                + str(checkdigit.verhoeff_compute(stem + "10"))
                            )
                            corruption_analysis.r_did = (
                                stem
                                + "11"
                                + str(checkdigit.verhoeff_compute(stem + "11"))
                            )
                case _:
                    corruption_analysis.outcome_code = OutcomeCodes.NOT_TRAILING_ZEROES
                    return corruption_analysis

    corruption_analysis.outcome_code = OutcomeCodes.POSSIBLE_CORRUPTION

    return corruption_analysis


def check_corruption_analyses_for_codes_in_release(
    analyses_list: list[CorruptionAnalysis] = None,
    did_ignore_flag: bool = False,
):
    """
    Takes a list of CorruptionAnalysis objects and uses sqllite release db to check if cid and/or did exist
    Deletes them if they do not exist
    Also extracts extra data such as preferred term
    """

    if did_ignore_flag:
        for a in analyses_list:
            a.r_did = None
            a.r_did_term = None

    cid_list = [a.r_cid for a in analyses_list if a.r_cid != None]
    did_list = [a.r_did for a in analyses_list if a.r_did != None]

    results_dict_cid = check_list_of_concept_ids_in_release_and_get_display(
        concept_id_list=cid_list,
    )

    results_dict_did = (
        check_list_of_description_ids_in_release_and_get_concept_id_and_display(
            description_id_list=did_list,
        )
    )

    for analysis in analyses_list:
        if analysis.outcome_code == OutcomeCodes.POSSIBLE_CORRUPTION:
            temp_r_cid = analysis.r_cid

            if analysis.r_cid is not None:
                in_release, pt = results_dict_cid[analysis.r_cid]
                if in_release:
                    analysis.r_cid_pt = pt
                else:
                    analysis.r_cid = None

            if analysis.r_did is not None:
                in_release, term, corresp_cid = results_dict_did[analysis.r_did]
                if in_release:
                    analysis.r_did_corresp_cid = corresp_cid
                    analysis.r_did_term = term
                else:
                    analysis.r_did = None

            # refine outcome code
            if (analysis.r_cid is not None) ^ (analysis.r_did is not None):
                analysis.outcome_code = OutcomeCodes.POSSIBLE_CORRUPTION_UNAMBIG

            if (analysis.r_cid is not None) and (analysis.r_did is not None):
                analysis.outcome_code = OutcomeCodes.POSSIBLE_CORRUPTION_AMBIG

            if (analysis.r_cid is None) and (analysis.r_did is None):
                analysis.outcome_code = OutcomeCodes.NO_RECONSTRUCTIONS_EXIST

            if (
                (analysis.r_cid is not None)
                and (analysis.r_did is None)
                and (temp_r_cid == analysis.sctid_provided)
            ):
                analysis.outcome_code = OutcomeCodes.ANY_CORRUPTION_IS_SILENT

            if (
                (analysis.r_cid is not None)
                and (analysis.r_did is not None)
                and (temp_r_cid == analysis.sctid_provided)
            ):
                analysis.outcome_code = OutcomeCodes.AMBIG_COULD_BE_SILENT
                