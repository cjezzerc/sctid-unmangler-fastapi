from ..analyse_sctid_for_corruption import analyse_sctid_for_corruption
from ..check_corruption_analyses_for_codes_in_release import (
    check_corruption_analyses_for_codes_in_release,
)
from ..refine_outcome_codes import refine_outcome_codes


def test_check_corruption_analyses_for_codes_in_release():

    # setup analyses_list
    analyses_list = [
        analyse_sctid_for_corruption(sctid="1082551000000100"),
        analyse_sctid_for_corruption(sctid="1012131000001110"),
        analyse_sctid_for_corruption(sctid="4036431000001100"),
        analyse_sctid_for_corruption(sctid="1085961000119100"),
        analyse_sctid_for_corruption(sctid="11972301000001100"),
        analyse_sctid_for_corruption(sctid="900000000000478000"),
        
    ]
    check_corruption_analyses_for_codes_in_release(
        analyses_list=analyses_list, did_ignore_flag=False
    )

    # now the tests
    refine_outcome_codes(analyses_list=analyses_list)

    assert analyses_list[0].outcome_code.name == "POSSIBLE_CORRUPTION_UNAMBIG"
    assert analyses_list[1].outcome_code.name == "POSSIBLE_CORRUPTION_UNAMBIG"
    assert analyses_list[2].outcome_code.name == "NO_RECONSTRUCTIONS_EXIST"
    assert analyses_list[3].outcome_code.name == "ANY_CORRUPTION_IS_SILENT"
    assert analyses_list[4].outcome_code.name == "POSSIBLE_CORRUPTION_AMBIG"
    assert analyses_list[5].outcome_code.name == "AMBIG_COULD_BE_SILENT"
