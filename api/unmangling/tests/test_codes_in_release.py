import sys
from .. import codes_in_release
from ...terminology_server.terminology_server_module import TerminologyServer

ts = TerminologyServer()


def test_1():
    in_release, preferred_term = (
        codes_in_release.check_concept_id_in_release_and_get_display(
            concept_id=91487003999,
            terminology_server=ts,
        )
    )
    assert in_release is False
    assert preferred_term is None


def test_2():
    in_release, preferred_term = (
        codes_in_release.check_concept_id_in_release_and_get_display(
            concept_id=91487003,
            terminology_server=ts,
        )
    )
    assert in_release is True
    assert preferred_term == "Nappy rash"

def test_3():
    in_release, corresponding_concept_id, preferred_term = codes_in_release.check_description_id_in_release_and_get_concept_id_and_display(
            description_id=509466017,
            terminology_server=ts,
        )
    assert in_release is True
    assert corresponding_concept_id == "91487003"
    assert preferred_term == "Nappy rash"

def test_4():
    in_release, corresponding_concept_id, preferred_term = codes_in_release.check_description_id_in_release_and_get_concept_id_and_display(
            description_id=509466017999,
            terminology_server=ts,
        )
    assert in_release is False
    assert corresponding_concept_id is None
    assert preferred_term is None