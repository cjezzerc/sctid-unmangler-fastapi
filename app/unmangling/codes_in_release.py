"""
functions related to testing if a code is a SNOMED release 
and if so retrieving the preferred term, associated concept id (for descriptions) etc
"""
import logging
# from fhir.resources.parameters import Parameters
logger=logging.getLogger()

def check_status_code(response):
    if response.status_code!=200:
        logger.error(f"Error: Call to {response.url} gave reponse status {response.status_code}")
        logger.error(f"Error: Call to {response.url} gave reponse {response.text}")
        return None
    return response

def check_concept_id_in_release_and_get_display(concept_id=None, terminology_server=None):
    relative_url=f"CodeSystem/$validate-code?url=http://snomed.info/sct&code={concept_id}"
    response=terminology_server.do_get(relative_url=relative_url, verbose=True, timing=True)
    checked_response=check_status_code(response) 
    if checked_response:
        # p=Parameters.model_validate(checked_response.json()) - quite slow, ca 1ms
        preferred_term=None
        for parameter in response.json()["parameter"]:
            if parameter["name"]=="result":
                in_release=parameter["valueBoolean"]
            if parameter["name"]=="display": # (only exists in response if in_release is True)
                preferred_term=parameter["valueString"]
        # print("\n".join(repr_resource(p)))
        
    return in_release, preferred_term
    

