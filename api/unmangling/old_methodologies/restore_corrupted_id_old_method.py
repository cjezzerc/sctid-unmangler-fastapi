import re, json
from enum import Enum

from . import checkdigit

from ..terminology_server.terminology_server_module import TerminologyServer
from .codes_in_release_term_server_old import check_concept_id_in_release_and_get_display

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
