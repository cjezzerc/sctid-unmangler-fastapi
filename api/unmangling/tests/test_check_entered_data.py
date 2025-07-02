from .. import check_entered_data


def test_check_entered_data():
    text = """1082551000000105	16 digits; does not have appropriate pattern of trailing zeroes to be corrupted
1082551000000100	16 digits; can be reconstructed to a Concept Id
1012131000001110	16 digits; can be reconstructed to a Description Id (provided allow Description Ids)
1085961000119100	16 digits; although ends in 0, the provided ID exists in the release, and it is a Concept Id. Hence "silent".
1044401000000110	16 digits; although ends in 0, the provided ID exists in the release, and it is a Description Id. Hence "silent" (provided allow Description Ids)
4036431000001100	16 digits; ends in 0 but reconstruction does not exist in the release (penultimate digit 0)
2459643000001110	16 digits; ends in 0 but reconstruction does not exist in the release (penultimate digit 1)
3333333330009150	16 digits; penultimate digit is a neither a 0 nor a 1 so cannot reconstruct to a concept or Description Id.
10836111000119108	17 digits; does not have appropriate pattern of trailing zeroes to be corrupted
10836111000119100	17 digits; can be reconstructed to a Concept Id
35682801000001100	17 digits; can be reconstructed to a Description Id (provided allow Description Ids)
11972301000001100	17 digits; can be reconstructed to both a Concept and a Description Id (provided allow Description Ids)
44012211000001100	17 digits; although ends in 00, the provided ID exists in the release, and it is a Concept Id. Hence "silent". (No equivalent case can exist for a Description Id for 17 digits)
11424801000001100	17 digits; although ends in 00, the provided ID exists in the release, and it is a Concept Id. Hence "silent". However it can also be reconstructed to be a Description ID (provided allow Description IDs) so is ambiguous in that case.
28760821000119100	17 digits; ends in 00 but no reconstruction exists in the release 
262421481000087107	18 digits; does not have appropriate pattern of trailing zeroes to be corrupted
262421481000087000	18 digits; can be reconstructed to a Concept Id
106637601000001000	18 digits; can be reconstructed to a Description Id (provided allow Description Ids)
999001741000000000	18 digits; can be reconstructed to both a Concept and a Description Id (provided allow Description Ids)
900000000000497000	18 digits; although ends in 000, the provided ID exists in the release, and it is a Concept Id. Hence "silent". (No equivalent case can exist for a Description Id for 18 digits). Because starts 90000 is a "short form" case so penpenultimate digit is 0. Silent cases for 18 digits can only be the 90000 forms as otherwise digit 16 is a 1 so cannot be silent. (To date there are only 10 such cases.)
900000000000478000	17 digits; although ends in 000, the provided ID exists in the release, and it is a Concept Id. Hence "silent". Silent cases for 18 digits can only be the 90000 forms as otherwise digit 16 is a 1 so cannot be silent. (To date there are only 10 such cases.)  However it can also be reconstructed to be a Description ID (provided allow Description IDs) so is ambiguous in that case. (To date there are only 3 such cases)
145670821000119000	18 digits; ends in 000 but no reconstruction exists in the release"""

    results = check_entered_data.check_entered_data(text=text, did_ignore_flag=False)

    assert results == [
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
                "sctid_provided": "1082551000000105",
                "sctid_provided_stem": "108255100000010",
                "sctid_provided_trailing_zeroes": "5",
                "validity": True,
            },
            "other_data": {
                "react_key": 0,
                "rest_of_line": "\t16 digits; does not have appropriate "
                "pattern of trailing zeroes to be corrupted",
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
            "other_data": {
                "react_key": 1,
                "rest_of_line": "\t16 digits; can be reconstructed to a " "Concept Id",
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
                "r_cid": None,
                "r_cid_pt": None,
                "r_cid_stem": None,
                "r_cid_trailing_zeroes": None,
                "r_did": "1012131000001114",
                "r_did_corresp_cid": "37248411000001109",
                "r_did_stem": "101213100000111",
                "r_did_term": "Aripiprazole 1mg/ml oral solution "
                "sugar free (Thornton & Ross Ltd) 150 "
                "ml",
                "r_did_trailing_zeroes": "4",
                "sctid_provided": "1012131000001110",
                "sctid_provided_stem": "101213100000111",
                "sctid_provided_trailing_zeroes": "0",
                "validity": False,
            },
            "other_data": {
                "react_key": 2,
                "rest_of_line": "\t16 digits; can be reconstructed to a "
                "Description Id (provided allow Description "
                "Ids)",
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
                "react_key": 3,
                "rest_of_line": "\t16 digits; although ends in 0, the "
                "provided ID exists in the release, and it is "
                'a Concept Id. Hence "silent".',
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.ANY_CORRUPTION_IS_SILENT",
                    "value": "4:The corrupted form is the same as the original, is in "
                    + "release, and there is no alternative reconstruction",
                },
                "r_cid": None,
                "r_cid_pt": None,
                "r_cid_stem": None,
                "r_cid_trailing_zeroes": None,
                "r_did": "1044401000000110",
                "r_did_corresp_cid": "485971000000109",
                "r_did_stem": "104440100000011",
                "r_did_term": "Ex-cigarette smoker",
                "r_did_trailing_zeroes": "0",
                "sctid_provided": "1044401000000110",
                "sctid_provided_stem": "104440100000011",
                "sctid_provided_trailing_zeroes": "0",
                "validity": True,
            },
            "other_data": {
                "react_key": 4,
                "rest_of_line": "\t16 digits; although ends in 0, the "
                "provided ID exists in the release, and it is "
                'a Description Id. Hence "silent" (provided '
                "allow Description Ids)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.NO_RECONSTRUCTIONS_EXIST",
                    "value": "10:The sctid provided "
                    "looks like it may be "
                    "corrupted but neither the "
                    "original nor any "
                    "reconstruction is in "
                    "release",
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
                "sctid_provided": "4036431000001100",
                "sctid_provided_stem": "403643100000110",
                "sctid_provided_trailing_zeroes": "0",
                "validity": False,
            },
            "other_data": {
                "react_key": 5,
                "rest_of_line": "\t16 digits; ends in 0 but reconstruction "
                "does not exist in the release (penultimate "
                "digit 0)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.NO_RECONSTRUCTIONS_EXIST",
                    "value": "10:The sctid provided "
                    "looks like it may be "
                    "corrupted but neither the "
                    "original nor any "
                    "reconstruction is in "
                    "release",
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
                "sctid_provided": "2459643000001110",
                "sctid_provided_stem": "245964300000111",
                "sctid_provided_trailing_zeroes": "0",
                "validity": False,
            },
            "other_data": {
                "react_key": 6,
                "rest_of_line": "\t16 digits; ends in 0 but reconstruction "
                "does not exist in the release (penultimate "
                "digit 1)",
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
                "react_key": 7,
                "rest_of_line": "\t16 digits; penultimate digit is a neither "
                "a 0 nor a 1 so cannot reconstruct to a "
                "concept or Description Id.",
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
                "sctid_provided": "10836111000119108",
                "sctid_provided_stem": "108361110001191",
                "sctid_provided_trailing_zeroes": "08",
                "validity": True,
            },
            "other_data": {
                "react_key": 8,
                "rest_of_line": "\t17 digits; does not have appropriate "
                "pattern of trailing zeroes to be corrupted",
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
                "react_key": 9,
                "rest_of_line": "\t17 digits; can be reconstructed to a " "Concept Id",
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
                "r_cid": None,
                "r_cid_pt": None,
                "r_cid_stem": None,
                "r_cid_trailing_zeroes": None,
                "r_did": "35682801000001115",
                "r_did_corresp_cid": "10391111000001102",
                "r_did_stem": "356828010000011",
                "r_did_term": "Metformin 850mg tablets (Arrow "
                "Generics Ltd) 300 tablet",
                "r_did_trailing_zeroes": "15",
                "sctid_provided": "35682801000001100",
                "sctid_provided_stem": "356828010000011",
                "sctid_provided_trailing_zeroes": "00",
                "validity": False,
            },
            "other_data": {
                "react_key": 10,
                "rest_of_line": "\t17 digits; can be reconstructed to a "
                "Description Id (provided allow Description "
                "Ids)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.POSSIBLE_CORRUPTION_AMBIG",
                    "value": "2:The sctid provided is "
                    "invalid and can be "
                    "reconstructed to both a "
                    "concept id and a "
                    "description id that is "
                    "found in release???",
                },
                "r_cid": "11972301000001103",
                "r_cid_pt": "TraLife",
                "r_cid_stem": "119723010000011",
                "r_cid_trailing_zeroes": "03",
                "r_did": "11972301000001119",
                "r_did_corresp_cid": "3444001000001100",
                "r_did_stem": "119723010000011",
                "r_did_term": "Lansoprazole 30mg oral suspension - " "product",
                "r_did_trailing_zeroes": "19",
                "sctid_provided": "11972301000001100",
                "sctid_provided_stem": "119723010000011",
                "sctid_provided_trailing_zeroes": "00",
                "validity": False,
            },
            "other_data": {
                "react_key": 11,
                "rest_of_line": "\t17 digits; can be reconstructed to both a "
                "Concept and a Description Id (provided allow "
                "Description Ids)",
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
                "r_cid": "44012211000001100",
                "r_cid_pt": "Disopyramide 100mg capsules (Drugsrus " "Ltd)",
                "r_cid_stem": "440122110000011",
                "r_cid_trailing_zeroes": "00",
                "r_did": None,
                "r_did_corresp_cid": None,
                "r_did_stem": None,
                "r_did_term": None,
                "r_did_trailing_zeroes": None,
                "sctid_provided": "44012211000001100",
                "sctid_provided_stem": "440122110000011",
                "sctid_provided_trailing_zeroes": "00",
                "validity": True,
            },
            "other_data": {
                "react_key": 12,
                "rest_of_line": "\t17 digits; although ends in 00, the "
                "provided ID exists in the release, and it is "
                'a Concept Id. Hence "silent". (No equivalent '
                "case can exist for a Description Id for 17 "
                "digits)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.AMBIG_COULD_BE_SILENT",
                    "value": "5:The corrupted form is "
                    "the same as the original, "
                    "is in release, but there "
                    "is also an alternative "
                    "reconstruction",
                },
                "r_cid": "11424801000001100",
                "r_cid_pt": "DEXMEDETOMIDINE 1mg/10mL concentrate "
                "for soln for injection",
                "r_cid_stem": "114248010000011",
                "r_cid_trailing_zeroes": "00",
                "r_did": "11424801000001116",
                "r_did_corresp_cid": "4016901000001105",
                "r_did_stem": "114248010000011",
                "r_did_term": "Mandanol 6+ Paracetamol",
                "r_did_trailing_zeroes": "16",
                "sctid_provided": "11424801000001100",
                "sctid_provided_stem": "114248010000011",
                "sctid_provided_trailing_zeroes": "00",
                "validity": True,
            },
            "other_data": {
                "react_key": 13,
                "rest_of_line": "\t17 digits; although ends in 00, the "
                "provided ID exists in the release, and it is "
                'a Concept Id. Hence "silent". However it can '
                "also be reconstructed to be a Description ID "
                "(provided allow Description IDs) so is "
                "ambiguous in that case.",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.NO_RECONSTRUCTIONS_EXIST",
                    "value": "10:The sctid provided "
                    "looks like it may be "
                    "corrupted but neither the "
                    "original nor any "
                    "reconstruction is in "
                    "release",
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
                "sctid_provided": "28760821000119100",
                "sctid_provided_stem": "287608210001191",
                "sctid_provided_trailing_zeroes": "00",
                "validity": False,
            },
            "other_data": {
                "react_key": 14,
                "rest_of_line": "\t17 digits; ends in 00 but no "
                "reconstruction exists in the release",
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
            "other_data": {
                "react_key": 15,
                "rest_of_line": "\t18 digits; does not have appropriate "
                "pattern of trailing zeroes to be corrupted",
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
                "react_key": 16,
                "rest_of_line": "\t18 digits; can be reconstructed to a " "Concept Id",
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
                "r_cid": None,
                "r_cid_pt": None,
                "r_cid_stem": None,
                "r_cid_trailing_zeroes": None,
                "r_did": "106637601000001117",
                "r_did_corresp_cid": "398695002",
                "r_did_stem": "106637601000001",
                "r_did_term": "Atenolol + Nifedipine",
                "r_did_trailing_zeroes": "117",
                "sctid_provided": "106637601000001000",
                "sctid_provided_stem": "106637601000001",
                "sctid_provided_trailing_zeroes": "000",
                "validity": False,
            },
            "other_data": {
                "react_key": 17,
                "rest_of_line": "\t18 digits; can be reconstructed to a "
                "Description Id (provided allow Description "
                "Ids)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.POSSIBLE_CORRUPTION_AMBIG",
                    "value": "2:The sctid provided is "
                    "invalid and can be "
                    "reconstructed to both a "
                    "concept id and a "
                    "description id that is "
                    "found in release???",
                },
                "r_cid": "999001741000000107",
                "r_cid_pt": "Gastroenterology outpatient diagnosis "
                "simple reference set",
                "r_cid_stem": "999001741000000",
                "r_cid_trailing_zeroes": "107",
                "r_did": "999001741000000111",
                "r_did_corresp_cid": "999000821000000100",
                "r_did_stem": "999001741000000",
                "r_did_term": "Laterality simple reference set",
                "r_did_trailing_zeroes": "111",
                "sctid_provided": "999001741000000000",
                "sctid_provided_stem": "999001741000000",
                "sctid_provided_trailing_zeroes": "000",
                "validity": False,
            },
            "other_data": {
                "react_key": 18,
                "rest_of_line": "\t18 digits; can be reconstructed to both a "
                "Concept and a Description Id (provided allow "
                "Description Ids)",
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
                "react_key": 19,
                "rest_of_line": "\t18 digits; although ends in 000, the "
                "provided ID exists in the release, and it is "
                'a Concept Id. Hence "silent". (No equivalent '
                "case can exist for a Description Id for 18 "
                'digits). Because starts 90000 is a "short '
                'form" case so penpenultimate digit is 0. '
                "Silent cases for 18 digits can only be the "
                "90000 forms as otherwise digit 16 is a 1 so "
                "cannot be silent. (To date there are only 10 "
                "such cases.)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.AMBIG_COULD_BE_SILENT",
                    "value": "5:The corrupted form is "
                    "the same as the original, "
                    "is in release, but there "
                    "is also an alternative "
                    "reconstruction",
                },
                "r_cid": "900000000000478000",
                "r_cid_pt": "Unsigned integer",
                "r_cid_stem": "900000000000478",
                "r_cid_trailing_zeroes": "000",
                "r_did": "900000000000478016",
                "r_did_corresp_cid": "900000000000225001",
                "r_did_stem": "900000000000478",
                "r_did_term": "Qualifying relationship (core " "metadata concept)",
                "r_did_trailing_zeroes": "016",
                "sctid_provided": "900000000000478000",
                "sctid_provided_stem": "900000000000478",
                "sctid_provided_trailing_zeroes": "000",
                "validity": True,
            },
            "other_data": {
                "react_key": 20,
                "rest_of_line": "\t17 digits; although ends in 000, the "
                "provided ID exists in the release, and it is "
                'a Concept Id. Hence "silent". Silent cases '
                "for 18 digits can only be the 90000 forms as "
                "otherwise digit 16 is a 1 so cannot be "
                "silent. (To date there are only 10 such "
                "cases.)  However it can also be "
                "reconstructed to be a Description ID "
                "(provided allow Description IDs) so is "
                "ambiguous in that case. (To date there are "
                "only 3 such cases)",
            },
        },
        {
            "corruption_analysis": {
                "outcome_code": {
                    "name": "OutcomeCodes.NO_RECONSTRUCTIONS_EXIST",
                    "value": "10:The sctid provided "
                    "looks like it may be "
                    "corrupted but neither the "
                    "original nor any "
                    "reconstruction is in "
                    "release",
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
                "sctid_provided": "145670821000119000",
                "sctid_provided_stem": "145670821000119",
                "sctid_provided_trailing_zeroes": "000",
                "validity": False,
            },
            "other_data": {
                "react_key": 21,
                "rest_of_line": "\t18 digits; ends in 000 but no "
                "reconstruction exists in the release",
            },
        },
    ]
