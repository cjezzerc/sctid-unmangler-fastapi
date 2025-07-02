from ..analyse_sctid_for_corruption import analyse_sctid_for_corruption
from ..check_corruption_analyses_for_codes_in_release import check_corruption_analyses_for_codes_in_release

def test_check_corruption_analyses_for_codes_in_release():

    # setup analyses_list
    analyses_list = [
        analyse_sctid_for_corruption(sctid="1082551000000100"),
        analyse_sctid_for_corruption(sctid="1012131000001110"),
        analyse_sctid_for_corruption(sctid="4036431000001100"),
        analyse_sctid_for_corruption(sctid="2459643000001110"),
    ]

    # now the tests
    check_corruption_analyses_for_codes_in_release(
        analyses_list=analyses_list, did_ignore_flag=False
    )
    analysis = analyses_list[0]
    assert analysis.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert analysis.r_cid == "1082551000000105"
    assert analysis.r_did == None

    analysis = analyses_list[1]
    assert analysis.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert analysis.r_cid == None
    assert analysis.r_did == "1012131000001114"

    analysis = analyses_list[2]
    assert analysis.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert analysis.r_cid == None
    assert analysis.r_did == None

    analysis = analyses_list[2]
    assert analysis.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert analysis.r_cid == None
    assert analysis.r_did == None

    check_corruption_analyses_for_codes_in_release(
        analyses_list=analyses_list, did_ignore_flag=True
    )
    analysis = analyses_list[0]
    assert analysis.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert analysis.r_cid == "1082551000000105"
    assert analysis.r_did == None

    analysis = analyses_list[1]
    assert analysis.outcome_code.name == "POSSIBLE_CORRUPTION"
    assert analysis.r_cid == None
    assert analysis.r_did == None

    