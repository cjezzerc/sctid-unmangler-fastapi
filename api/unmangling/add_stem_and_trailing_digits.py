from .restore_corrupted_id import CorruptionAnalysis


def do_one(sctid=None):
    l = len(sctid)
    if l in [16, 17, 18]:
        stem = sctid[:15]
        trailing_zeroes = sctid[15:]
    else:
        stem = sctid
        trailing_zeroes = ""
    return stem, trailing_zeroes


def add_stem_and_trailing_digits(analysis: CorruptionAnalysis = None):

    analysis.sctid_provided_stem, analysis.sctid_provided_trailing_zeroes = do_one(
        sctid=analysis.sctid_provided
    )
    if analysis.r_cid is not None:
        analysis.r_cid_stem, analysis.r_cid_trailing_zeroes = do_one(
            sctid=analysis.r_cid
        )
    if analysis.r_did is not None:
        analysis.r_did_stem, analysis.r_did_trailing_zeroes = do_one(
            sctid=analysis.r_did
        )
