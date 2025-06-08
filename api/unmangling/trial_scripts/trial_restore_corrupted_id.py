from .. import restore_corrupted_id
from ...terminology_server.terminology_server_module import TerminologyServer

ts = TerminologyServer()

analyses_list = []

for sctid in [
    "123456789012345",  #  (15)
    "1234567890123456789",  #  (19)
    "S23456789012345678"  # (18, not all digits)
    "1082551000000100",  # 1082551000000105 (16)
    "1085961000119100",  # corruption silent (16)
    "3333333330009150",  # not reconstructable (16)
    "11424801000001100",  # itelf or DID 11424801000001116 (17)
    "262421481000087107",  # not corrupted (18)
    "262421481000087100",  # not corrupted but invalid (18)
    "262421481000087000",  # 262421481000087107 (18)
    "900000000000497000",  # itself or DID 900000000000497016 (18)
    "10760821000119100",  # itself or DID 10760821000119116 (17)
    "10836111000119100",  # 10836111000119108 or DID 10836111000119112 (17)
]:
    print(sctid)
    results = (
        restore_corrupted_id.new_detect_corruption_and_restore_id_no_release_checking(
            sctid=sctid
        )
    )
    print(results)
    print(results.to_json())
    analyses_list.append(results)
    print("===================")

ts = TerminologyServer()
results_dict = restore_corrupted_id.check_corruption_analyses_for_codes_in_release(
    analyses_list=analyses_list,
    terminology_server=ts,
)

print(results_dict)
