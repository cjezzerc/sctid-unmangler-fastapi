import sys
from .. import codes_in_release
from ...terminology_server.terminology_server_module import TerminologyServer

ts = TerminologyServer()


def do_call(concept_id=None):
    return codes_in_release.check_concept_id_in_release_and_get_display(
        concept_id=concept_id, terminology_server=ts
    )


def test_1():
    in_release, preferred_term = do_call(concept_id=91487003999)
    assert in_release is False
    assert preferred_term is None


def test_2():
    in_release, preferred_term = do_call(concept_id=91487003)
    assert in_release is True
    assert preferred_term == "Nappy rash"
