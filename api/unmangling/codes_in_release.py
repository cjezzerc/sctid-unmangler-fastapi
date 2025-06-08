"""
functions related to testing if a code is a SNOMED release
and if so retrieving the preferred term, associated concept id (for descriptions) etc
"""

import urllib.parse
import re

import logging
from fhir.resources.bundle import Bundle, BundleEntry, BundleEntryRequest

logger = logging.getLogger()


def check_status_code(response):
    if response.status_code != 200:
        logger.error(
            f"Error: Call to {response.url} gave reponse status {response.status_code}"
        )
        logger.error(f"Error: Call to {response.url} gave response {response.text}")
        return None
    return response


def check_concept_id_in_release_and_get_display(
    concept_id=None, terminology_server=None
):
    relative_url = (
        f"CodeSystem/$validate-code?url=http://snomed.info/sct&code={concept_id}"
    )
    response = terminology_server.do_get(
        relative_url=relative_url, verbose=True, timing=True
    )
    checked_response = check_status_code(response)
    if checked_response:
        preferred_term = None
        for parameter in response.json()["parameter"]:
            if parameter["name"] == "result":
                in_release = parameter["valueBoolean"]
            if (
                parameter["name"] == "display"
            ):  # (only exists in response if in_release is True)
                preferred_term = parameter["valueString"]
        return in_release, preferred_term
    else:
        return None, None


def check_list_of_concept_ids_in_release_and_get_display(
    concept_id_list=None, terminology_server=None
):
    b = Bundle(type="batch", entry=[])
    for concept_id in concept_id_list:
        be = BundleEntry(
            request=BundleEntryRequest(
                method="GET",
                url=f"CodeSystem/$validate-code?url=http://snomed.info/sct&code={concept_id}",
            )
        )
        b.entry.append(be)
    relative_url = ""
    response = terminology_server.do_post(
        relative_url=relative_url,
        json=b.model_dump(),
        verbose=True,
        timing=True,
    )

    checked_response = check_status_code(response)
    if checked_response:
        results_dict = {}
        for entry in response.json()["entry"]:
            preferred_term = None
            for parameter in entry["resource"]["parameter"]:
                if parameter["name"] == "result":
                    in_release = parameter["valueBoolean"]
                if parameter["name"] == "code":
                    code = parameter["valueCode"]
                if (
                    parameter["name"] == "display"
                ):  # (only exists in response if in_release is True)
                    preferred_term = parameter["valueString"]
            results_dict[code] = (in_release, preferred_term)
        return results_dict
    else:
        return None


def check_description_id_in_release_and_get_concept_id_and_display(
    description_id=None,
    terminology_server=None,
):
    relative_url = f'ValueSet/$expand?url=http://snomed.info/sct?fhir_vs=ecl/(* {{{{ term = wild:"{description_id}"}}}})'
    print(relative_url)
    response = terminology_server.do_get(
        relative_url=relative_url, verbose=True, timing=True
    )
    checked_response = check_status_code(response)
    if checked_response:
        if "contains" in checked_response.json()["expansion"]:
            in_release = True
            contains = checked_response.json()["expansion"]["contains"]
            corresponding_concept_id = contains[0]["code"]
            preferred_term = contains[0]["display"]
        else:
            in_release = False
            corresponding_concept_id = None
            preferred_term = None
        return in_release, corresponding_concept_id, preferred_term
    else:
        return None, None, None


def check_list_of_description_ids_in_release_and_get_concept_id_and_display(
    description_id_list=None,
    terminology_server=None,
):
    b = Bundle(type="batch", entry=[])
    for description_id in description_id_list:
        be = BundleEntry(
            request=BundleEntryRequest(
                method="GET",
                url="ValueSet/$expand?url="
                + urllib.parse.quote_plus(
                    f'http://snomed.info/sct?fhir_vs=ecl/(* {{{{ term = wild:"{description_id}"}}}})'
                ),
            )
        )
        b.entry.append(be)
    # print(b.model_dump_json(indent=2))
    relative_url = ""
    response = terminology_server.do_post(
        relative_url=relative_url,
        json=b.model_dump(),
        verbose=True,
        timing=True,
    )

    checked_response = check_status_code(response)
    if checked_response:
        results_dict = {}
        for entry in response.json()["entry"]:

            # only way to extract back the description id seems to be from 
            # an re search on the url that is returned in each bundle entry in the response
            url = entry["resource"]["url"]
            description_id = re.search(r'"(.*)"', url).groups()[0]

            if "contains" in entry["resource"]["expansion"]:
                in_release = True
                contains = entry["resource"]["expansion"]["contains"]
                corresponding_concept_id = contains[0]["code"]
                preferred_term = contains[0]["display"]
            else:
                in_release = False
                corresponding_concept_id = None
                preferred_term = None
            results_dict[description_id] = (
                in_release,
                corresponding_concept_id,
                preferred_term,
            )

    return results_dict
