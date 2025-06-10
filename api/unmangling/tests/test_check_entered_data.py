from .. import check_entered_data

def test_check_entered_data():
    text = """
        123456789012345  #  (15)
        1234567890123456789  #  (19)
        S23456789012345678  # (18, not all digits)
        1082551000000100  # 1082551000000105 (16)
        1085961000119100  # corruption silent (16)
        3333333330009150  # not reconstructable (16)
        11424801000001100  # itelf or DID 11424801000001116 (17)
        262421481000087107  # not corrupted (18)
        262421481000087100  # not corrupted but invalid (18)
        262421481000087000  # 262421481000087107 (18)
        900000000000497000  # itself or DID 900000000000497016 (18)
        10760821000119100  # itself or DID 10760821000119116 (17)
        10836111000119100  # 10836111000119108 or DID 10836111000119112 (17)
        11972301000001100  # ambiguous - 11972301000001103 and 11972301000001119 both exist
        10093501000001100  # ambiguous - 10093501000001107 and 10093501000001111 both exist
        999001741000000000  # ambiguous - 999001741000000107 and 999001741000000111 both exist"""

    results = check_entered_data.check_entered_data(text=text)

    assert results == [
        {
            "other_data": {"rest_of_line": "", "react_key": 0},
            "corruption_analysis": {
                "sctid_provided": "",
                "validity": False,
                "outcome_code": "OutcomeCodes.CANNOT_BE_CORRUPTED",
                "r_cid": None,
                "r_did": None,
                "r_cid_pt": None,
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {"rest_of_line": "  #  (15)", "react_key": 1},
            "corruption_analysis": {
                "sctid_provided": "123456789012345",
                "validity": False,
                "outcome_code": "OutcomeCodes.CANNOT_BE_CORRUPTED",
                "r_cid": None,
                "r_did": None,
                "r_cid_pt": None,
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {"rest_of_line": "  #  (19)", "react_key": 2},
            "corruption_analysis": {
                "sctid_provided": "1234567890123456789",
                "validity": False,
                "outcome_code": "OutcomeCodes.CANNOT_BE_CORRUPTED",
                "r_cid": None,
                "r_did": None,
                "r_cid_pt": None,
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {"rest_of_line": "  # (18, not all digits)", "react_key": 3},
            "corruption_analysis": {
                "sctid_provided": "S23456789012345678",
                "validity": False,
                "outcome_code": "OutcomeCodes.CANNOT_BE_CORRUPTED",
                "r_cid": None,
                "r_did": None,
                "r_cid_pt": None,
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {"rest_of_line": "  # 1082551000000105 (16)", "react_key": 4},
            "corruption_analysis": {
                "sctid_provided": "1082551000000100",
                "validity": False,
                "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
                "r_cid": "1082551000000105",
                "r_did": None,
                "r_cid_pt": "Requires information in aphasia-accessible format",
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {"rest_of_line": "  # corruption silent (16)", "react_key": 5},
            "corruption_analysis": {
                "sctid_provided": "1085961000119100",
                "validity": True,
                "outcome_code": "OutcomeCodes.ANY_CORRUPTION_IS_SILENT",
                "r_cid": None,
                "r_did": None,
                "r_cid_pt": None,
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {"rest_of_line": "  # not reconstructable (16)", "react_key": 6},
            "corruption_analysis": {
                "sctid_provided": "3333333330009150",
                "validity": False,
                "outcome_code": "OutcomeCodes.NOT_RECONSTRUCTABLE",
                "r_cid": None,
                "r_did": None,
                "r_cid_pt": None,
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {
                "rest_of_line": "  # itelf or DID 11424801000001116 (17)",
                "react_key": 7,
            },
            "corruption_analysis": {
                "sctid_provided": "11424801000001100",
                "validity": True,
                "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
                "r_cid": None,
                "r_did": "11424801000001116",
                "r_cid_pt": None,
                "r_did_term": "Mandanol 6+ Paracetamol",
                "r_did_corresp_cid": "4016901000001105",
            },
        },
        {
            "other_data": {"rest_of_line": "  # not corrupted (18)", "react_key": 8},
            "corruption_analysis": {
                "sctid_provided": "262421481000087107",
                "validity": True,
                "outcome_code": "OutcomeCodes.NOT_CORRUPTED",
                "r_cid": None,
                "r_did": None,
                "r_cid_pt": None,
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {
                "rest_of_line": "  # not corrupted but invalid (18)",
                "react_key": 9,
            },
            "corruption_analysis": {
                "sctid_provided": "262421481000087100",
                "validity": False,
                "outcome_code": "OutcomeCodes.NOT_CORRUPTED",
                "r_cid": None,
                "r_did": None,
                "r_cid_pt": None,
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {"rest_of_line": "  # 262421481000087107 (18)", "react_key": 10},
            "corruption_analysis": {
                "sctid_provided": "262421481000087000",
                "validity": False,
                "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
                "r_cid": "262421481000087107",
                "r_did": None,
                "r_cid_pt": "Acremonium sclerotigenum",
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {
                "rest_of_line": "  # itself or DID 900000000000497016 (18)",
                "react_key": 11,
            },
            "corruption_analysis": {
                "sctid_provided": "900000000000497000",
                "validity": True,
                "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
                "r_cid": None,
                "r_did": None,
                "r_cid_pt": None,
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {
                "rest_of_line": "  # itself or DID 10760821000119116 (17)",
                "react_key": 12,
            },
            "corruption_analysis": {
                "sctid_provided": "10760821000119100",
                "validity": True,
                "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
                "r_cid": None,
                "r_did": None,
                "r_cid_pt": None,
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {
                "rest_of_line": "  # 10836111000119108 or DID 10836111000119112 (17)",
                "react_key": 13,
            },
            "corruption_analysis": {
                "sctid_provided": "10836111000119100",
                "validity": False,
                "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
                "r_cid": "10836111000119108",
                "r_did": None,
                "r_cid_pt": "Dislocation of symphysis pubis in labour and delivery",
                "r_did_term": None,
                "r_did_corresp_cid": None,
            },
        },
        {
            "other_data": {
                "rest_of_line": "  # ambiguous - 11972301000001103 and 11972301000001119 both exist",
                "react_key": 14,
            },
            "corruption_analysis": {
                "sctid_provided": "11972301000001100",
                "validity": False,
                "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
                "r_cid": "11972301000001103",
                "r_did": "11972301000001119",
                "r_cid_pt": "TraLife",
                "r_did_term": "Lansoprazole 30mg oral suspension - product",
                "r_did_corresp_cid": "3444001000001100",
            },
        },
        {
            "other_data": {
                "rest_of_line": "  # ambiguous - 10093501000001107 and 10093501000001111 both exist",
                "react_key": 15,
            },
            "corruption_analysis": {
                "sctid_provided": "10093501000001100",
                "validity": False,
                "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
                "r_cid": "10093501000001107",
                "r_did": "10093501000001111",
                "r_cid_pt": "SENSURA CLICK 60mm/10031 cut-to-fit 10mm-55mm stoma two-piece ostomy system base plates",
                "r_did_term": "56sachets",
                "r_did_corresp_cid": "2034401000001107",
            },
        },
        {
            "other_data": {
                "rest_of_line": "  # ambiguous - 999001741000000107 and 999001741000000111 both exist",
                "react_key": 16,
            },
            "corruption_analysis": {
                "sctid_provided": "999001741000000000",
                "validity": False,
                "outcome_code": "OutcomeCodes.POSSIBLE_CORRUPTION",
                "r_cid": "999001741000000107",
                "r_did": "999001741000000111",
                "r_cid_pt": "Gastroenterology outpatient diagnosis simple reference set",
                "r_did_term": "Laterality simple reference set",
                "r_did_corresp_cid": "999000821000000100",
            },
        },
    ]
