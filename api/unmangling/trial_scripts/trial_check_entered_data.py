import pprint

from .. import check_entered_data

text = """1082551000000105	16 digits; does not have appropriate pattern of trailing zeroes to be corrupted
1082551000000100	16 digits; can be reconstructed to a Concept Id
1012131000001110	16 digits; can be reconstructed to a Description Id (provided allow Description Ids)
1085961000119100	16 digits; although ends in 0, the provided ID exists in the release, and it is a Concept Id. Hence "silent".
1044401000000110	16 digits; although ends in 0, the provided ID exists in the release, and it is a Description Id. Hence "silent" (provided allow Description Ids)
4036431000001100	16 digits; ends in 0 but reconstruction does not exist in the release (penultimate digit 0)
2459643000001110	16 digits; ends in 0 but reconstruction does not exist in the release (penultimate digit 1)
3333333330009150	16 digits; penultimate digit is a neither a 0 nor a 1 so cannot reconstruct to a concept or Description Id.
10836111000119108	17 digits; does not have appropriate pattern of trailing zeroes to be corrupted
10836111000119100	17 digits; can be reconstructed to a Concept Id
35682801000001100	17 digits; can be reconstructed to a Description Id (provided allow Description Ids)
11972301000001100	17 digits; can be reconstructed to both a Concept and a Description Id (provided allow Description Ids)
44012211000001100	17 digits; although ends in 00, the provided ID exists in the release, and it is a Concept Id. Hence "silent". (No equivalent case can exist for a Description Id for 17 digits)
11424801000001100	17 digits; although ends in 00, the provided ID exists in the release, and it is a Concept Id. Hence "silent". However it can also be reconstructed to be a Description ID (provided allow Description IDs) so is ambiguous in that case.
28760821000119100	17 digits; ends in 00 but no reconstruction exists in the release 
262421481000087107	18 digits; does not have appropriate pattern of trailing zeroes to be corrupted
262421481000087000	18 digits; can be reconstructed to a Concept Id
106637601000001000	18 digits; can be reconstructed to a Description Id (provided allow Description Ids)
999001741000000000	18 digits; can be reconstructed to both a Concept and a Description Id (provided allow Description Ids)
900000000000497000	18 digits; although ends in 000, the provided ID exists in the release, and it is a Concept Id. Hence "silent". (No equivalent case can exist for a Description Id for 18 digits). Because starts 90000 is a "short form" case so penpenultimate digit is 0. Silent cases for 18 digits can only be the 90000 forms as otherwise digit 16 is a 1 so cannot be silent. (To date there are only 10 such cases.)
900000000000478000	17 digits; although ends in 000, the provided ID exists in the release, and it is a Concept Id. Hence "silent". Silent cases for 18 digits can only be the 90000 forms as otherwise digit 16 is a 1 so cannot be silent. (To date there are only 10 such cases.)  However it can also be reconstructed to be a Description ID (provided allow Description IDs) so is ambiguous in that case. (To date there are only 3 such cases)
145670821000119000	18 digits; ends in 000 but no reconstruction exists in the release
125605004	        Not 16-18 digits
S1082551000000105	Not purely digits""" 

results = check_entered_data.check_entered_data(text=text, did_ignore_flag=False)

pprint.pprint(results)
