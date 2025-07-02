from .corruption_analysis import CorruptionAnalysis
from .outcome_codes import OutcomeCodes


def refine_outcome_codes(
    analyses_list: list[CorruptionAnalysis] = None,
):
    """
    for analyses where reconstruction has been attempted, refines POSSIBLE_CORRUPTION to
    one of five outcomes
    """
    for analysis in analyses_list:
        if analysis.outcome_code == OutcomeCodes.POSSIBLE_CORRUPTION:

            if (analysis.r_cid is not None) ^ (analysis.r_did is not None):
                analysis.outcome_code = OutcomeCodes.POSSIBLE_CORRUPTION_UNAMBIG

                if analysis.sctid_provided in [
                    analysis.r_cid,
                    analysis.r_did,
                ]:  # see comment below
                    analysis.outcome_code = OutcomeCodes.ANY_CORRUPTION_IS_SILENT

            elif (analysis.r_cid is not None) and (analysis.r_did is not None):
                analysis.outcome_code = OutcomeCodes.POSSIBLE_CORRUPTION_AMBIG

                if analysis.sctid_provided in [
                    analysis.r_cid,
                    analysis.r_did,
                ]:  # see comment below
                    analysis.outcome_code = OutcomeCodes.AMBIG_COULD_BE_SILENT

            else:  # i.e. (analysis.r_cid is None) and (analysis.r_did is None):
                assert (analysis.r_cid is None) and (analysis.r_did is None)
                analysis.outcome_code = OutcomeCodes.NO_RECONSTRUCTIONS_EXIST

            # re the checks for "SILENT" using the "if x in a list" style
            # these are both written the same for clarity.
            # however the provided_sctid==r_did case can only happen for 16 digits and it can never be ambiguous so only
            # really needed for the unambiguous ANY_CORRUPTION_IS_SILENT case
            # and the did case does not really need to be considered for the ambiguous case, as ambiguity
            # can only occur for 17 or 18 digits and an entered sctid can never look like a did in that case
            # I think coded like this the intent is clear even if certain of the subconditions can never be true
            # under certain circumstances
