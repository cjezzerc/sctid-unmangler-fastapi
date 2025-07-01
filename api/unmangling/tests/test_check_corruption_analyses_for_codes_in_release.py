from .. import restore_corrupted_id


def test_check_corruption_analyses_for_codes_in_release():

    # pre-checks

    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="123456789012345")
    # assert results.outcome_code.name == "NOT_16_TO_18_DIGITS"

    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="1234567890123456789")
    # assert results.outcome_code.name == "NOT_16_TO_18_DIGITS"

    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="S23456789012345678")
    # assert results.outcome_code.name == "NOT_PURE_DIGITS"

    # 16 digit branch

    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="1082551000000105")
    # assert results.outcome_code.name == "NOT_TRAILING_ZEROES"

    analyses_list = [
        restore_corrupted_id.analyse_sctid_for_corruption(sctid="1082551000000100")
    ]
    restore_corrupted_id.check_corruption_analyses_for_codes_in_release(
        analyses_list=analyses_list, did_ignore_flag=False
    )
    analysis = analyses_list[0]
    assert analysis.outcome_code.name == "POSSIBLE_CORRUPTION_UNAMBIG"
    assert analysis.r_cid == "1082551000000105"
    assert analysis.r_did == None

    analyses_list = [
        restore_corrupted_id.analyse_sctid_for_corruption(sctid="1012131000001110")
    ]
    restore_corrupted_id.check_corruption_analyses_for_codes_in_release(
        analyses_list=analyses_list, did_ignore_flag=False
    )
    analysis = analyses_list[0]
    assert analysis.outcome_code.name == "POSSIBLE_CORRUPTION_UNAMBIG"
    assert analysis.r_cid == None
    assert analysis.r_did == "1012131000001114"

    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="1012131000001110")
    # assert results.outcome_code.name == "POSSIBLE_CORRUPTION"
    # assert results.r_cid == None
    # assert results.r_did == "1012131000001114"

    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="3333333330009150")
    # assert results.outcome_code.name == "NOT_RECONSTRUCTABLE"

    # # 17 digit branch

    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="10836111000119108")
    # assert results.outcome_code.name == "NOT_TRAILING_ZEROES"

    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="10836111000119100")
    # assert results.outcome_code.name == "POSSIBLE_CORRUPTION"
    # assert results.r_cid == "10836111000119108"
    # assert results.r_did == "10836111000119112"

    # # 18 digit branch

    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="999001741000000107")
    # assert results.outcome_code.name == "NOT_TRAILING_ZEROES"

    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="999001741000000000")
    # assert results.outcome_code.name == "POSSIBLE_CORRUPTION"
    # assert results.r_cid == "999001741000000107"
    # assert results.r_did == "999001741000000111"

    # #(900000... case)
    # results = restore_corrupted_id.analyse_sctid_for_corruption(sctid="900000000000522000")
    # assert results.outcome_code.name == "POSSIBLE_CORRUPTION"
    # assert results.r_cid == "900000000000522004"
    # assert results.r_did == "900000000000522015"
