from .. import analyse_sctid_for_corruption

def test_analyse_sctid_for_corruption():
    
    # pre-checks

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="123456789012345")
    assert results.outcome_code.name == "NOT_16_TO_18_DIGITS"

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="1234567890123456789")
    assert results.outcome_code.name == "NOT_16_TO_18_DIGITS"

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="S23456789012345678")
    assert results.outcome_code.name == "NOT_PURE_DIGITS"

    # 16 digit branch

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="1082551000000105")
    assert results.outcome_code.name == "NOT_TRAILING_ZEROES"

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="1082551000000100")
    assert results.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert results.r_cid == "1082551000000105"
    assert results.r_did == None

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="1012131000001110")
    assert results.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert results.r_cid == None
    assert results.r_did == "1012131000001114"

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="3333333330009150")
    assert results.outcome_code.name == "NOT_RECONSTRUCTABLE"

    # 17 digit branch

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="10836111000119108")
    assert results.outcome_code.name == "NOT_TRAILING_ZEROES"

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="10836111000119100")
    assert results.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert results.r_cid == "10836111000119108"
    assert results.r_did == "10836111000119112"

    # 18 digit branch

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="999001741000000107")
    assert results.outcome_code.name == "NOT_TRAILING_ZEROES"

    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="999001741000000000")
    assert results.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert results.r_cid == "999001741000000107"
    assert results.r_did == "999001741000000111"

    #(900000... case)
    results = analyse_sctid_for_corruption.analyse_sctid_for_corruption(sctid="900000000000522000")
    assert results.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert results.r_cid == "900000000000522004"
    assert results.r_did == "900000000000522015"