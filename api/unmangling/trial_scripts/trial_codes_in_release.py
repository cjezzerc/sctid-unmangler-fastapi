import sys
from .. import codes_in_release

import pprint

results_dict = (
    codes_in_release.check_list_of_concept_ids_in_release_and_get_display(
        concept_id_list=['86290005','86290005999'],
    )
)

print(results_dict)

results_dict = (
    codes_in_release.check_list_of_description_ids_in_release_and_get_concept_id_and_display(
        description_id_list=['509466017','509466017999'],
    )
)

print(results_dict)

