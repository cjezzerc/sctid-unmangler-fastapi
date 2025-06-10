from .. import restore_corrupted_id


def test_restore_corrupted_id():
    analyses_list = []
    for sctid in [
        "123456789012345",  #  (15)
        "1234567890123456789",  #  (19)
        "S23456789012345678"  # (18, not all digits)
        "1082551000000100",  # 1082551000000105 (16)
        "1085961000119100",  # corruption silent (16)
        "3333333330009150",  # not reconstructable (16)
        "11424801000001100",  # itelf or DID 11424801000001116 (17)
        "262421481000087107",  # not corrupted (18)
        "262421481000087100",  # not corrupted but invalid (18)
        "262421481000087000",  # 262421481000087107 (18)
        "900000000000497000",  # itself or DID 900000000000497016 (18)
        "10760821000119100",  # itself or DID 10760821000119116 (17)
        "10836111000119100",  # 10836111000119108 or DID 10836111000119112 (17)
        "11972301000001100",  # ambiguous - 11972301000001103 and 11972301000001119 both exist
        "10093501000001100",  # ambiguous - 10093501000001107 and 10093501000001111 both exist
        "999001741000000000",  # ambiguous - 999001741000000107 and 999001741000000111 both exist
    ]:
        results = restore_corrupted_id.analyse_sctid_for_corruption(sctid=sctid)
        analyses_list.append(results.to_dict())


    assert analyses_list == [
        {
            "sctid_provided": "123456789012345",
            "validity": False,
            "outcome_code": "OutcomeCodes.CANNOT_BE_CORRUPTED",
            "r_cid": None,
            "r_did": None,
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "1234567890123456789",
            "validity": False,
            "outcome_code": "OutcomeCodes.CANNOT_BE_CORRUPTED",
            "r_cid": None,
            "r_did": None,
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "S234567890123456781082551000000100",
            "validity": False,
            "outcome_code": "OutcomeCodes.CANNOT_BE_CORRUPTED",
            "r_cid": None,
            "r_did": None,
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "1085961000119100",
            "validity": True,
            "outcome_code": "OutcomeCodes.ANY_CORRUPTION_IS_SILENT",
            "r_cid": None,
            "r_did": None,
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "3333333330009150",
            "validity": False,
            "outcome_code": "OutcomeCodes.NOT_RECONSTRUCTABLE",
            "r_cid": None,
            "r_did": None,
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "11424801000001100",
            "validity": True,
            "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
            "r_cid": None,
            "r_did": "11424801000001116",
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "262421481000087107",
            "validity": True,
            "outcome_code": "OutcomeCodes.NOT_CORRUPTED",
            "r_cid": None,
            "r_did": None,
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "262421481000087100",
            "validity": False,
            "outcome_code": "OutcomeCodes.NOT_CORRUPTED",
            "r_cid": None,
            "r_did": None,
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "262421481000087000",
            "validity": False,
            "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
            "r_cid": "262421481000087107",
            "r_did": "262421481000087111",
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "900000000000497000",
            "validity": True,
            "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
            "r_cid": None,
            "r_did": "900000000000497016",
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "10760821000119100",
            "validity": True,
            "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
            "r_cid": None,
            "r_did": "10760821000119116",
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "10836111000119100",
            "validity": False,
            "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
            "r_cid": "10836111000119108",
            "r_did": "10836111000119112",
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "11972301000001100",
            "validity": False,
            "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
            "r_cid": "11972301000001103",
            "r_did": "11972301000001119",
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "10093501000001100",
            "validity": False,
            "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
            "r_cid": "10093501000001107",
            "r_did": "10093501000001111",
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
        {
            "sctid_provided": "999001741000000000",
            "validity": False,
            "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
            "r_cid": "999001741000000107",
            "r_did": "999001741000000111",
            "r_cid_pt": None,
            "r_did_term": None,
            "r_did_corresp_cid": None,
        },
    ]
