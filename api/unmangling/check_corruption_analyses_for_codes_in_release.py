from .corruption_analysis import CorruptionAnalysis
from .codes_in_release import (
    check_list_of_concept_ids_in_release_and_get_display,
    check_list_of_description_ids_in_release_and_get_term_and_concept_id,
)
from .outcome_codes import OutcomeCodes

def check_corruption_analyses_for_codes_in_release(
    analyses_list: list[CorruptionAnalysis] = None,
    did_ignore_flag: bool = False,
):
    """
    Takes a list of CorruptionAnalysis objects and uses sqllite release db to check if cid and/or did exist
    Deletes them if they do not exist
    Also extracts extra data such as preferred term
    """

    if did_ignore_flag:
        for a in analyses_list:
            a.r_did = None
            a.r_did_term = None

    cid_list = [a.r_cid for a in analyses_list if a.r_cid != None]
    did_list = [a.r_did for a in analyses_list if a.r_did != None]

    results_dict_cid = check_list_of_concept_ids_in_release_and_get_display(
        concept_id_list=cid_list,
    )

    results_dict_did = (
        check_list_of_description_ids_in_release_and_get_term_and_concept_id(
            description_id_list=did_list,
        )
    )

    for analysis in analyses_list:
        if analysis.outcome_code == OutcomeCodes.POSSIBLE_CORRUPTION:

            if analysis.r_cid is not None:
                in_release, pt = results_dict_cid[analysis.r_cid]
                if in_release:
                    analysis.r_cid_pt = pt
                else:
                    analysis.r_cid = None

            if analysis.r_did is not None:
                in_release, term, corresp_cid = results_dict_did[analysis.r_did]
                if in_release:
                    analysis.r_did_corresp_cid = corresp_cid
                    analysis.r_did_term = term
                else:
                    analysis.r_did = None
