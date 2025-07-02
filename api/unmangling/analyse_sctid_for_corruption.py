import re
import logging

from . import checkdigit
from .parse_and_validate_sctid import ParsedSCTID
from .outcome_codes import OutcomeCodes
from .corruption_analysis import CorruptionAnalysis

logger = logging.getLogger()

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
