from pydantic import BaseModel, field_serializer, ConfigDict

from .outcome_codes import OutcomeCodes


class CorruptionAnalysis(BaseModel):
    """
    class to hold all data about analysing (and reconstructing if necessary) one provided sctid
    """

    model_config = ConfigDict(validate_assignment=True)
    sctid_provided: str | None = None
    sctid_provided_stem: str | None = None
    sctid_provided_trailing_zeroes: str | None = None
    validity: bool | None = None
    outcome_code: OutcomeCodes | None = None
    r_cid: str | None = None
    r_cid_stem: str | None = None
    r_cid_trailing_zeroes: str | None = None
    r_did: str | None = None
    r_did_stem: str | None = None
    r_did_trailing_zeroes: str | None = None
    r_cid_pt: str | None = None
    r_did_term: str | None = None
    r_did_corresp_cid: str | None = None  # although populated, not used by front end

    @field_serializer("outcome_code")
    def serialize_outcome_code(self, outcome_code: OutcomeCodes, _info):
        return outcome_code.to_dict()
