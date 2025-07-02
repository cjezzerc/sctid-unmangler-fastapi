"""
Functions related to testing if lists of codes are in SNOMED release
and if so retrieving the preferred term, associated concept id (for descriptions) etc

Uses a simple sqllite database for speed
"""

import os
import sqlite3

def check_list_of_concept_ids_in_release_and_get_display(
    concept_id_list=None,
):
    """
    Takes a list of concept ids, and checks for each one if it is in the release
    and if so also retrieves the preferred term
    """

    descriptions_sqllite_file = os.environ["DESCRIPTIONS_SQLLITE_FILE"]
    with sqlite3.connect(descriptions_sqllite_file) as conn:
        cursor = conn.cursor()
        concept_id_list_string = ",".join(concept_id_list)

        sql_string = f"""
            SELECT * FROM concepts WHERE concept_id IN ( {concept_id_list_string} )
            """
        cursor.execute(sql_string)

        pt_dict = {cid: pt for cid, pt in cursor.fetchall()}
        
        results_dict = {}
        for concept_id in concept_id_list:
            if concept_id in pt_dict:
                results_dict[concept_id] = (True, pt_dict[concept_id])
            else:
                results_dict[concept_id] = (False, None)
        return results_dict

def check_list_of_description_ids_in_release_and_get_term_and_concept_id(
    description_id_list=None,
):
    """
    Takes a list of description ids, and checks for each one if it is in the release
    and if so also retrieves the term and the corresponding concept id
    """
    descriptions_sqllite_file = os.environ["DESCRIPTIONS_SQLLITE_FILE"]
    with sqlite3.connect(descriptions_sqllite_file) as conn:
        cursor = conn.cursor()
        description_id_list_string = ",".join(description_id_list)

        sql_string = f"""
            SELECT * FROM descriptions WHERE description_id IN ( {description_id_list_string} )
            """
        
        cursor.execute(sql_string)
        
        temp_dict = {did: (term, cid) for did, term, cid in cursor.fetchall()}
        results_dict = {}
        for description_id in description_id_list:
            if description_id in temp_dict:
                results_dict[description_id] = (
                    True,
                    temp_dict[description_id][0],
                    temp_dict[description_id][1],
                )
            else:
                results_dict[description_id] = (False, None, None)
        return results_dict
