from enum import Enum

class OutcomeCodes(Enum):
    """An Enum to contain the valid outcome_codes"""

    # fmt: off
    POSSIBLE_CORRUPTION_UNAMBIG      = "1:The sctid provided is invalid but can be reconstructed to a single form that is found in release"
    POSSIBLE_CORRUPTION_AMBIG        = "2:The sctid provided is invalid and can be reconstructed to both a concept id and a description id that is found in release???"
    POSSIBLE_CORRUPTION              = "3:This is a temporary outcome that indicates the sctid provided looks corrupted; should not occur once processing complete as is refined"
    ANY_CORRUPTION_IS_SILENT         = "4:The corrupted form is the same as the original, is in release, and there is no alternative reconstruction"
    AMBIG_COULD_BE_SILENT            = "5:The corrupted form is the same as the original, is in release, but there is also an alternative reconstruction"
    NOT_PURE_DIGITS                  = "8:The sctid provided does not contain pure digits"
    NOT_16_TO_18_DIGITS              = "6:The sctid provided is not 16-18 digits"
    NOT_TRAILING_ZEROES              = "7:The sctid provided is long enough to be corrupted but does not have the correct pattern of trailing zeroes"
    NOT_RECONSTRUCTABLE              = "9:The sctid provided has 16 digits but digit 15 is neither 0 nor 1"
    NO_RECONSTRUCTIONS_EXIST         = "10:The sctid provided looks like it may be corrupted but neither the original nor any reconstruction is in release"
    # fmt: on

    def to_dict(self):
        return {"name": "OutcomeCodes." + self.name, "value": self.value}