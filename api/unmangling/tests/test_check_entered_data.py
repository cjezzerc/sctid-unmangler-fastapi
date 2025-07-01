from .. import check_entered_data


def test_check_entered_data():
    text = """123456789012345  # (15)
        1234567890123456789    # (19)
        S23456789012345678     # (18, not all digits)
        1082551000000100       # 1082551000000105 (16)
        1085961000119100       # corruption silent (16)
        3333333330009150       # not reconstructable (16)
        11424801000001100      # itelf or DID 11424801000001116 both in release (17)
        262421481000087107     # not corrupted (18)
        262421481000087100     # not corrupted but invalid (18)
        10836111000119100      # 10836111000119108 or DID 10836111000119112 (DID not in release)  (17)
        262421481000087000     # 262421481000087107 or DID 262421481000087111 (DID not in release)  (18)
        10760821000119100      # itself or DID 10760821000119116 (DID not in release (17)
        900000000000497000     # itself or DID 900000000000497016 (DID not in release) (18)
        11972301000001100      # ambiguous - 11972301000001103 and 11972301000001119 both in release
        999001741000000000     # ambiguous - 999001741000000107 and 999001741000000111 both in release (18)"""

    results = check_entered_data.check_entered_data(text=text)

    assert results == [
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.NOT_16_TO_18_DIGITS",
                    "value": "6:The sctid provided is " "not 16-18 digits",
                },
                "r_cid": None,
                "r_cid_pt": None,
                "r_cid_stem": None,
                "r_cid_trailing_zeroes": None,
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "123456789012345",
                "sctid_provided_stem": "123456789012345",
                "sctid_provided_trailing_zeroes": "",
                "validity": False,
            },
            "other_data": {"react_key": 0, "rest_of_line": "  #  (15)"},
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.NOT_16_TO_18_DIGITS",
                    "value": "6:The sctid provided is " "not 16-18 digits",
                },
                "r_cid": None,
                "r_cid_pt": None,
                "r_cid_stem": None,
                "r_cid_trailing_zeroes": None,
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "1234567890123456789",
                "sctid_provided_stem": "1234567890123456789",
                "sctid_provided_trailing_zeroes": "",
                "validity": False,
            },
            "other_data": {"react_key": 1, "rest_of_line": "  #  (19)"},
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.NOT_PURE_DIGITS",
                    "value": "5:The sctid provided does " "not contain pure digits",
                },
                "r_cid": None,
                "r_cid_pt": None,
                "r_cid_stem": None,
                "r_cid_trailing_zeroes": None,
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "S23456789012345678",
                "sctid_provided_stem": "S23456789012345",
                "sctid_provided_trailing_zeroes": "678",
                "validity": False,
            },
            "other_data": {"react_key": 2, "rest_of_line": "  # (18, not all digits)"},
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.POSSIBLE_CORRUPTION_UNAMBIG",
                    "value": "1:The sctid provided is "
                    "invalid but can be "
                    "reconstructed to a single "
                    "form that is found in "
                    "release",
                },
                "r_cid": "1082551000000105",
                "r_cid_pt": "Requires information in " "aphasia-accessible format",
                "r_cid_stem": "108255100000010",
                "r_cid_trailing_zeroes": "5",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "1082551000000100",
                "sctid_provided_stem": "108255100000010",
                "sctid_provided_trailing_zeroes": "0",
                "validity": False,
            },
            "other_data": {"react_key": 3, "rest_of_line": "  # 1082551000000105 (16)"},
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.ANY_CORRUPTION_IS_SILENT",
                    "value": "4:The corrupted form is "
                    "the same as the original, "
                    "is in release, and there "
                    "is no alternative "
                    "reconstruction",
                },
                "r_cid": "1085961000119100",
                "r_cid_pt": "Dental caries on pit and fissure "
                "surface penetrating into dentin",
                "r_cid_stem": "108596100011910",
                "r_cid_trailing_zeroes": "0",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "1085961000119100",
                "sctid_provided_stem": "108596100011910",
                "sctid_provided_trailing_zeroes": "0",
                "validity": True,
            },
            "other_data": {
                "react_key": 4,
                "rest_of_line": "  # corruption silent (16)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.NOT_RECONSTRUCTABLE",
                    "value": "9:The sctid provided has "
                    "16 digits but digit 15 is "
                    "neither 0 nor 1",
                },
                "r_cid": None,
                "r_cid_pt": None,
                "r_cid_stem": None,
                "r_cid_trailing_zeroes": None,
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "3333333330009150",
                "sctid_provided_stem": "333333333000915",
                "sctid_provided_trailing_zeroes": "0",
                "validity": False,
            },
            "other_data": {
                "react_key": 5,
                "rest_of_line": "  # not reconstructable (16)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.ANY_CORRUPTION_IS_SILENT",
                    "value": "4:The corrupted form is "
                    "the same as the original, "
                    "is in release, and there "
                    "is no alternative "
                    "reconstruction",
                },
                "r_cid": "11424801000001100",
                "r_cid_pt": "DEXMEDETOMIDINE 1mg/10mL concentrate "
                "for soln for injection",
                "r_cid_stem": "114248010000011",
                "r_cid_trailing_zeroes": "00",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "11424801000001100",
                "sctid_provided_stem": "114248010000011",
                "sctid_provided_trailing_zeroes": "00",
                "validity": True,
            },
            "other_data": {
                "react_key": 6,
                "rest_of_line": "  # itelf or DID 11424801000001116 (17)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.NOT_TRAILING_ZEROES",
                    "value": "7:The sctid provided is "
                    "long enough to be "
                    "corrupted but does not "
                    "have the correct pattern "
                    "of trailing zeroes",
                },
                "r_cid": None,
                "r_cid_pt": None,
                "r_cid_stem": None,
                "r_cid_trailing_zeroes": None,
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "262421481000087107",
                "sctid_provided_stem": "262421481000087",
                "sctid_provided_trailing_zeroes": "107",
                "validity": True,
            },
            "other_data": {"react_key": 7, "rest_of_line": "  # not corrupted (18)"},
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.NOT_TRAILING_ZEROES",
                    "value": "7:The sctid provided is "
                    "long enough to be "
                    "corrupted but does not "
                    "have the correct pattern "
                    "of trailing zeroes",
                },
                "r_cid": None,
                "r_cid_pt": None,
                "r_cid_stem": None,
                "r_cid_trailing_zeroes": None,
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "262421481000087100",
                "sctid_provided_stem": "262421481000087",
                "sctid_provided_trailing_zeroes": "100",
                "validity": False,
            },
            "other_data": {
                "react_key": 8,
                "rest_of_line": "  # not corrupted but invalid (18)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.POSSIBLE_CORRUPTION_UNAMBIG",
                    "value": "1:The sctid provided is "
                    "invalid but can be "
                    "reconstructed to a single "
                    "form that is found in "
                    "release",
                },
                "r_cid": "262421481000087107",
                "r_cid_pt": "Acremonium sclerotigenum",
                "r_cid_stem": "262421481000087",
                "r_cid_trailing_zeroes": "107",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "262421481000087000",
                "sctid_provided_stem": "262421481000087",
                "sctid_provided_trailing_zeroes": "000",
                "validity": False,
            },
            "other_data": {
                "react_key": 9,
                "rest_of_line": "  # 262421481000087107 (18)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.ANY_CORRUPTION_IS_SILENT",
                    "value": "4:The corrupted form is "
                    "the same as the original, "
                    "is in release, and there "
                    "is no alternative "
                    "reconstruction",
                },
                "r_cid": "900000000000497000",
                "r_cid_pt": "CTV3 to SNOMED CT simple map",
                "r_cid_stem": "900000000000497",
                "r_cid_trailing_zeroes": "000",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "900000000000497000",
                "sctid_provided_stem": "900000000000497",
                "sctid_provided_trailing_zeroes": "000",
                "validity": True,
            },
            "other_data": {
                "react_key": 10,
                "rest_of_line": "  # itself or DID 900000000000497016 (18)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.ANY_CORRUPTION_IS_SILENT",
                    "value": "4:The corrupted form is "
                    "the same as the original, "
                    "is in release, and there "
                    "is no alternative "
                    "reconstruction",
                },
                "r_cid": "10760821000119100",
                "r_cid_pt": "Quintuplets, some live born",
                "r_cid_stem": "107608210001191",
                "r_cid_trailing_zeroes": "00",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "10760821000119100",
                "sctid_provided_stem": "107608210001191",
                "sctid_provided_trailing_zeroes": "00",
                "validity": True,
            },
            "other_data": {
                "react_key": 11,
                "rest_of_line": "  # itself or DID 10760821000119116 (17)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.POSSIBLE_CORRUPTION_UNAMBIG",
                    "value": "1:The sctid provided is "
                    "invalid but can be "
                    "reconstructed to a single "
                    "form that is found in "
                    "release",
                },
                "r_cid": "10836111000119108",
                "r_cid_pt": "Dislocation of symphysis pubis in " "labour and delivery",
                "r_cid_stem": "108361110001191",
                "r_cid_trailing_zeroes": "08",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "10836111000119100",
                "sctid_provided_stem": "108361110001191",
                "sctid_provided_trailing_zeroes": "00",
                "validity": False,
            },
            "other_data": {
                "react_key": 12,
                "rest_of_line": "  # 10836111000119108 or DID "
                "10836111000119112 (17)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.POSSIBLE_CORRUPTION_UNAMBIG",
                    "value": "1:The sctid provided is "
                    "invalid but can be "
                    "reconstructed to a single "
                    "form that is found in "
                    "release",
                },
                "r_cid": "11972301000001103",
                "r_cid_pt": "TraLife",
                "r_cid_stem": "119723010000011",
                "r_cid_trailing_zeroes": "03",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "11972301000001100",
                "sctid_provided_stem": "119723010000011",
                "sctid_provided_trailing_zeroes": "00",
                "validity": False,
            },
            "other_data": {
                "react_key": 13,
                "rest_of_line": "  # ambiguous - 11972301000001103 and "
                "11972301000001119 both exist",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.POSSIBLE_CORRUPTION_UNAMBIG",
                    "value": "1:The sctid provided is "
                    "invalid but can be "
                    "reconstructed to a single "
                    "form that is found in "
                    "release",
                },
                "r_cid": "10093501000001107",
                "r_cid_pt": "SENSURA CLICK 60mm/10031 cut-to-fit "
                "10mm-55mm stoma two-piece ostomy system "
                "base plates",
                "r_cid_stem": "100935010000011",
                "r_cid_trailing_zeroes": "07",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "10093501000001100",
                "sctid_provided_stem": "100935010000011",
                "sctid_provided_trailing_zeroes": "00",
                "validity": False,
            },
            "other_data": {
                "react_key": 14,
                "rest_of_line": "  # ambiguous - 10093501000001107 and "
                "10093501000001111 both exist",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.POSSIBLE_CORRUPTION_UNAMBIG",
                    "value": "1:The sctid provided is "
                    "invalid but can be "
                    "reconstructed to a single "
                    "form that is found in "
                    "release",
                },
                "r_cid": "999001741000000107",
                "r_cid_pt": "Gastroenterology outpatient diagnosis "
                "simple reference set",
                "r_cid_stem": "999001741000000",
                "r_cid_trailing_zeroes": "107",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "999001741000000000",
                "sctid_provided_stem": "999001741000000",
                "sctid_provided_trailing_zeroes": "000",
                "validity": False,
            },
            "other_data": {
                "react_key": 15,
                "rest_of_line": "  # ambiguous - 999001741000000107 and "
                "999001741000000111 both exist",
            },
        },
    ]
