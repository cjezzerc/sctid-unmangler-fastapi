"""
Functions to service the main endpoint that takes entry from a text box, parses it to a set of sctids,
and returns corruption analysis
"""

import re

from .restore_corrupted_id import (
    analyse_sctid_for_corruption,
    check_corruption_analyses_for_codes_in_release,
)
from . import add_stem_and_trailing_digits


def parse_line(line=None):
    f = re.split(r"[\|\s]", line.strip())
    if f != []:
        sctid = f[0]
    else:
        sctid = ""
    rest_of_line = line.strip()[len(sctid) :]
    return sctid, rest_of_line


def check_entered_data(
    text: str = None,
    did_ignore_flag: bool = True,
):
    # fmt:off
    other_data    = []  # these two lists will correspond element by element to each line of input
    analyses_list = []  # and are combined at end into the final results list
    # fmt:on

    for i_line, line in enumerate(text.split("\n")):
        sctid, rest_of_line = parse_line(line)

        corruption_analysis = analyse_sctid_for_corruption(sctid=sctid)
        analyses_list.append(corruption_analysis)
        other_data.append({"rest_of_line": rest_of_line, "react_key": i_line})

    analyses_list = check_corruption_analyses_for_codes_in_release(
        analyses_list=analyses_list,
        did_ignore_flag=did_ignore_flag,
    )

    for analysis in analyses_list:
        add_stem_and_trailing_digits.add_stem_and_trailing_digits(analysis=analysis)

    results = []  # this holds the corresponding elements from
    #               other_data and analyses_list
    for i_line, other_data in enumerate(other_data):
        results.append(
            {
                "other_data": other_data,
                # "corruption_analysis": analyses_list[i_line].to_dict(),
                "corruption_analysis": analyses_list[i_line].model_dump(),
            }
        )
    return results
