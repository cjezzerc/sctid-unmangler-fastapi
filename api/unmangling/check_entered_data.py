import re
import json

from .restore_corrupted_id import detect_corruption_and_restore_id
from .restore_corrupted_id_new_method import (
    new_detect_corruption_and_restore_id_no_release_checking,
    check_corruption_analyses_for_codes_in_release,
)
from .parse_and_validate_sctid import ParsedSCTID

# def do_checks(id_list):
#     results={}
#     results["mangling_analysis"]=[]
#     for sctid in id_list:
#         parsed_sctid=ParsedSCTID(string=str(sctid))
#         results["validity_check"] = {"valid_SCTID":parsed_sctid.valid, "message":parsed_sctid.validation_message}
#         results["mangling_analysis"].append(detect_corruption_and_restore_id(sctid=sctid))
#     return results


def parse_line(line=None):
    f = re.split(r"[\|\s]", line.strip())
    if f != []:
        sctid = f[0]
    else:
        sctid = ""
    rest_of_line = line.strip()[len(sctid) :]
    return sctid, rest_of_line


def check_entered_data(text=None):
    results = []
    for react_id, line in enumerate(text.split("\n")):
        sctid, rest_of_line = parse_line(line)
        mangling_analysis = detect_corruption_and_restore_id(sctid=sctid)

        mangling_analysis["rest_of_line"] = rest_of_line

        parsed_sctid = ParsedSCTID(string=str(sctid))
        mangling_analysis["validity"] = parsed_sctid.valid
        mangling_analysis["id"] = react_id

        results.append(mangling_analysis)
    # really need to move the checking for whether restored IDs are in release (and getting PT etc)
    # until after have done the initial mangling analysis so that can batch the data
    return results


def check_entered_data_new(text=None):
    other_data = []
    analyses_list = []
    for i_line, line in enumerate(text.split("\n")):
        sctid, rest_of_line = parse_line(line)

        corruption_analysis = new_detect_corruption_and_restore_id_no_release_checking(
            sctid=sctid
        )
        analyses_list.append(corruption_analysis)
        other_data.append({"rest_of_line": rest_of_line, "react_key": i_line})

    analyses_list = check_corruption_analyses_for_codes_in_release(
        analyses_list=analyses_list,
    )
    results = []
    for i_line, other_data in enumerate(other_data):
        results.append(
            {
                "other_data": other_data,
                "corruption_analysis": analyses_list[i_line].to_dict(),
            }
        )
    return results

