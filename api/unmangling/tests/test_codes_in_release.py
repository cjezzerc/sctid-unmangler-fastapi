from .. import codes_in_release


def test_concepts():
    results_dict = (
        codes_in_release.check_list_of_concept_ids_in_release_and_get_display(
            concept_id_list=["86290005", "86290005999"],
        )
    )
    assert results_dict == {
        "86290005": (True, "Respiratory rate"),
        "86290005999": (False, None),
    }


def test_descriptions():

    results_dict = codes_in_release.check_list_of_description_ids_in_release_and_get_term_and_concept_id(
        description_id_list=["509466017", "509466017999"],
    )
    assert results_dict == {
        "509466017": (True, "Ammoniacal napkin dermatitis", "91487003"),
        "509466017999": (False, None, None),
    }
