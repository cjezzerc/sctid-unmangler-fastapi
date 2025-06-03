
import re

from .restore_corrupted_id import detect_corruption_and_restore_id
from .parse_and_validate_sctid import ParsedSCTID

def do_checks(id_list):    
    results={}
    results["mangling_analysis"]=[]
    print("hi!!!")
    for sctid in id_list:
        parsed_sctid=ParsedSCTID(string=str(sctid))
        results["validity_check"] = {"valid_SCTID":parsed_sctid.valid, "message":parsed_sctid.validation_message}
        results["mangling_analysis"].append(detect_corruption_and_restore_id(sctid=sctid))
    return results

def parse_line(line=None):
    f=re.split(r'[\|\s]', line.strip())
    if f != []:             
        sctid=f[0]
    else: 
        sctid=""
    rest_of_line=line.strip()[len(sctid):]  
    return sctid, rest_of_line   

def check_entered_data(text=None):
    results=[]
    for react_id, line in enumerate(text.split('\n')):
        sctid, rest_of_line=parse_line(line)
        mangling_analysis=detect_corruption_and_restore_id(sctid=sctid)
        mangling_analysis["rest_of_line"]=rest_of_line
        parsed_sctid=ParsedSCTID(string=str(sctid))
        mangling_analysis["validity"]=parsed_sctid.valid
        mangling_analysis["id"]=react_id
        results.append(mangling_analysis)
        print(mangling_analysis)
    return results