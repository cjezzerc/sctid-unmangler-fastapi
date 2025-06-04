import sys
from . import codes_in_release

import logging
logger=logging.getLogger()

from ..terminology_server.terminology_server_module import TerminologyServer
from .mytimer import MyTimer

ts=TerminologyServer()
concept_id=sys.argv[1]

timer1=MyTimer("t1")
in_release, preferred_term=codes_in_release.check_concept_id_in_release_and_get_display(
    concept_id=concept_id,
    terminology_server=ts)
print(timer1.make_end_message())
if in_release:
    print(f"{concept_id} | {preferred_term} |")
else:
    print(f" {concept_id} is not in lateset release")