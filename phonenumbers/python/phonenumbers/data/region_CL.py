"""Auto-generated file, do not edit by hand. CL metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_CL = PhoneMetadata(id='CL', country_code=56, international_prefix='(?:0|1(?:1[0-69]|2[0-57]|5[13-58]|69|7[0167]|8[018]))0',
    general_desc=PhoneNumberDesc(national_number_pattern='1230\\d{7}|6\\d{9,10}|[2-9]\\d{8}', possible_length=(9, 10, 11)),
    fixed_line=PhoneNumberDesc(national_number_pattern='21962\\d{4}|(?:232[0-46-8]|80[1-9]\\d)\\d{5}|(?:22|3[2-5]|[47][1-35]|5[1-3578]|6[13-57]|8[1-9]|9[2-9])\\d{7}', example_number='221234567', possible_length=(9,)),
    mobile=PhoneNumberDesc(national_number_pattern='21962\\d{4}|(?:232[0-46-8]|80[1-9]\\d)\\d{5}|(?:22|3[2-5]|[47][1-35]|5[1-3578]|6[13-57]|8[1-9]|9[2-9])\\d{7}', example_number='221234567', possible_length=(9,)),
    toll_free=PhoneNumberDesc(national_number_pattern='(?:1230\\d|800)\\d{6}', example_number='800123456', possible_length=(9, 11)),
    shared_cost=PhoneNumberDesc(national_number_pattern='600\\d{7,8}', example_number='6001234567', possible_length=(10, 11)),
    voip=PhoneNumberDesc(national_number_pattern='44\\d{7}', example_number='441234567', possible_length=(9,)),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='600\\d{7,8}', possible_length=(10, 11)),
    number_format=[NumberFormat(pattern='(\\d{4})', format='\\1', leading_digits_pattern=['1(?:[03-589]|21)|[29]0|78']),
        NumberFormat(pattern='(\\d{5})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['21'], national_prefix_formatting_rule='(\\1)'),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['44']),
        NumberFormat(pattern='(\\d)(\\d{4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['2[23]'], national_prefix_formatting_rule='(\\1)'),
        NumberFormat(pattern='(\\d)(\\d{4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['9[2-9]']),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['3[2-5]|[47]|5[1-3578]|6[13-57]|8(?:0[1-9]|[1-9])'], national_prefix_formatting_rule='(\\1)'),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['60|8']),
        NumberFormat(pattern='(\\d{4})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['1']),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{2})(\\d{3})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['60'])],
    intl_number_format=[NumberFormat(pattern='(\\d{5})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['21']),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['44']),
        NumberFormat(pattern='(\\d)(\\d{4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['2[23]']),
        NumberFormat(pattern='(\\d)(\\d{4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['9[2-9]']),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['3[2-5]|[47]|5[1-3578]|6[13-57]|8(?:0[1-9]|[1-9])']),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3,4})', format='\\1 \\2 \\3', leading_digits_pattern=['60|8']),
        NumberFormat(pattern='(\\d{4})(\\d{3})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['1']),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{2})(\\d{3})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['60'])],
    mobile_number_portable_region=True)