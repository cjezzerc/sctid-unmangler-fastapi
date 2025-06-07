import re
from enum import Enum

from . import checkdigit

from ..terminology_server.terminology_server_module import TerminologyServer
from .codes_in_release import check_concept_id_in_release_and_get_display


def check_if_in_release(sctid=None, ds=None, sct_version=None):

    # stub out checking
    return None

    if sctid[-2] == "0":
        data = ds.get_data_about_concept_id(
            concept_id=sctid,
            date_string=sct_version,
        )
        return (
            data != []
        )  # data about a concept id is a list of possible description ids
    elif sctid[-2] == "1":
        data = ds.get_data_about_description_id(
            description_id=sctid,
            date_string=sct_version,
        )
        return (
            data is not None
        )  # data about a description id is a single possible concept id
    else:
        return False


# def convert_to_dict(sctid, mangled, RC, RD, RC_in_release, RD_in_release):
#     return {
#         "sctid_provided": sctid,
#         "mangling_suspected": mangled,
#         "reconstructed_concept_ID": RC,
#         "reconstructed_description_ID": RD,
#         "RC_in_release": RC_in_release,
#         # "RD_in_release": RD_in_release,
#     }
def detect_corruption_and_restore_id(sctid=None, ds=None, sct_version=None):

    sctid = str(sctid)  # in case test with an int

    mangling_analysis = {
        "sctid_provided": sctid,
        "mangling_suspected": False,
        "reconstructed_concept_ID": None,
        "reconstructed_description_ID": None,
        "RC_in_release": None,
        "RC_preferred_term": None,
        # "RD_in_release": RD_in_release,
    }
    # can't be excel corruption if not purely digits
    if (re.search(r"^[0-9]+$", sctid.strip())) is None:
        return mangling_analysis

    # can't be excel corruption if not 16, 17 or 18 digits
    n_digits = len(sctid)
    if n_digits < 16 or n_digits > 18:
        return mangling_analysis

    # excel corruption will zero the trailing 1, 2 or 3 digits
    # fmt:off
    trailing_zeroes = (
        (n_digits==16 and sctid[-1] =="0") or
        (n_digits==17 and sctid[-2:]=="00") or
        (n_digits==18 and sctid[-3:]=="000")
        )
    # fmt:on
    # so if not seen it cannot be corrupted
    if not trailing_zeroes:
        return mangling_analysis

    exists_in_release = check_if_in_release(sctid=sctid, sct_version=sct_version, ds=ds)

    # if it exists in release, assume not corrupted
    # (In theory could report if is one of rare cases where the corrupted form is also an sctid in the release)
    if exists_in_release:
        return mangling_analysis

    # if cd_ok perhaps could report that might be from another namespace
    # but not implementing now
    # cd_ok=checkdigit.verhoeff_check(sctid)

    # reconstruct as concept_id (RC) or description_id(RD)
    if n_digits == 16:
        temp = sctid[:-1]
        RC = RD = None
        if temp[-1] == "0":
            RC = temp + str(checkdigit.verhoeff_compute(temp))
        elif temp[-1] == "1":
            RD = temp + str(checkdigit.verhoeff_compute(temp))
    # fmt: off
    elif (n_digits == 17) or (
          n_digits == 18 and sctid[:6] == "900000"
    # fmt: on
    ):  # 17 digit or 18 digit "short form" that all seem to start 900000
        temp = sctid[:-2]
        RC = temp + "0" + str(checkdigit.verhoeff_compute(temp + "0"))
        RD = temp + "1" + str(checkdigit.verhoeff_compute(temp + "1"))
    else:  # 18 digits long form
        temp = sctid[:-3]
        RC = temp + "10" + str(checkdigit.verhoeff_compute(temp + "10"))
        RD = temp + "11" + str(checkdigit.verhoeff_compute(temp + "11"))

    terminology_server = TerminologyServer()
    RC_in_release, RC_preferred_term = check_concept_id_in_release_and_get_display(
        concept_id=RC, terminology_server=terminology_server
    )
    RD_in_release = (RD is not None) and check_if_in_release(
        sctid=RD, sct_version=sct_version, ds=ds
    )

    mangling_analysis["mangling_suspected"] = (
        True  # this still may not be True if RC and RD both are None
    )
    # or neither is in release
    mangling_analysis["reconstructed_concept_ID"] = RC
    mangling_analysis["reconstructed_description_ID"] = RD
    mangling_analysis["RC_in_release"] = RC_in_release
    mangling_analysis["RC_preferred_term"] = RC_preferred_term
    return mangling_analysis


class CorruptionAnalysis:
    __slots__ = [
        "sctid_provided",
        "outcome_code",
        "r_cid",
        "r_did",
        "r_cid_pt",
        "r_did_corresp_cid",
        "r_did_corresp_cid_pt",
    ]

    def __init__(self, sctid=None):
        self.sctid_provided = sctid
        self.outcome_code = None
        self.r_cid = None
        self.r_cid_pt = None
        self.r_did = None
        self.r_did_corresp_cid = None
        self.r_did_corresp_cid_pt = None

    def __repr__(self):
        return "\n".join([f" {x}:{getattr(self, x)}" for x in self.__slots__])


class OutcomeCodes(Enum):
    CANNOT_BE_CORRUPTED = (
        "The code is not 16-18 digits (or does not contain pure digits)"
    )
    NOT_CORRUPTED = "The code is long enough to be corrupted but does not have the correct pattern of trailing zeroes"
    ANY_CORRUPTION_IS_SILENT = (
        "This is a 16 digit ccode with a correct check digit of 0"
    )
    NOT_RECONSTRUCTABLE = "The code has 16 digits but digit 15 is neither 0 nor 1"
    POSSIBLE_CORRUPTION = "???"


def new_detect_corruption_and_restore_id_no_release_checking(
    sctid=None,
):

    sctid = str(sctid)  # in case test with an int

    corruption_analysis = CorruptionAnalysis()

    # can't be excel corruption if not purely digits
    if (
        ((re.search(r"^[0-9]+$", sctid.strip())) is None)
        or (len(sctid) < 16)
        or (len(sctid) > 18)
    ):
        corruption_analysis.outcome_code = OutcomeCodes.CANNOT_BE_CORRUPTED
        return corruption_analysis

    n_digits = len(sctid)

    # import pdb
    # pdb.set_trace()
    match n_digits:
        case 16:
            match sctid[-1]:
                case "0":
                    match checkdigit.verhoeff_check(sctid):
                        case True:
                            corruption_analysis.outcome_code = (
                                OutcomeCodes.ANY_CORRUPTION_IS_SILENT
                            )
                            return corruption_analysis
                        case False:
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
                    corruption_analysis.outcome_code = OutcomeCodes.NOT_CORRUPTED
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
                    corruption_analysis.outcome_code = OutcomeCodes.NOT_CORRUPTED
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
                    corruption_analysis.outcome_code = OutcomeCodes.NOT_CORRUPTED
                    return corruption_analysis

    # Now remove r_cid if it is the same as sctid
    # The logic is a bit complicated around this part and can probably be expressed in
    # a number of different ways.
    # Already above the case of 16 digits with valid chk digit is dealt with
    # as in that case no alernate type (i.e. cid or did) is possible.
    # The code above as simple as possible and allows for the case
    # the case of 17 or 18 digits where the corruption of a DID might be missed if assumed that a valid
    # code ending in 00 (17 digits) or 000 (18 digits) were not corrupted.
    # But it means that r_cid may in fact be identical to sctid hence the next check and removal.
    if n_digits in [17, 18] and corruption_analysis.r_cid == sctid:
        corruption_analysis.r_cid = None

    corruption_analysis.outcome_code = OutcomeCodes.POSSIBLE_CORRUPTION
    
    return corruption_analysis
