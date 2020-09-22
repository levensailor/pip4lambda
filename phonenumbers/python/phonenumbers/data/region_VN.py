"""Auto-generated file, do not edit by hand. VN metadata"""
from ..phonemetadata import NumberFormat, PhoneNumberDesc, PhoneMetadata

PHONE_METADATA_VN = PhoneMetadata(id='VN', country_code=84, international_prefix='00',
    general_desc=PhoneNumberDesc(national_number_pattern='[12]\\d{9}|[135-9]\\d{8}|[16]\\d{7}|[16-8]\\d{6}', possible_length=(7, 8, 9, 10)),
    fixed_line=PhoneNumberDesc(national_number_pattern='2(?:0[3-9]|1[0-689]|2[0-25-9]|3[2-9]|4[2-8]|5[124-9]|6[0-39]|7[0-7]|8[2-7]|9[0-4679])\\d{7}', example_number='2101234567', possible_length=(10,)),
    mobile=PhoneNumberDesc(national_number_pattern='(?:(?:3\\d|7[06-9])\\d|5(?:2[238]|[689]\\d)|8(?:[1-58]\\d|6[5-9]|79|9[689])|9(?:[0-8]\\d|9[013-9]))\\d{6}', example_number='912345678', possible_length=(9,)),
    toll_free=PhoneNumberDesc(national_number_pattern='1800\\d{4,6}', example_number='1800123456', possible_length=(8, 9, 10)),
    premium_rate=PhoneNumberDesc(national_number_pattern='1900\\d{4,6}', example_number='1900123456', possible_length=(8, 9, 10)),
    voip=PhoneNumberDesc(national_number_pattern='672\\d{6}', example_number='672012345', possible_length=(9,)),
    uan=PhoneNumberDesc(national_number_pattern='(?:[17]99|80\\d)\\d{4}|69\\d{5,6}', example_number='1992000', possible_length=(7, 8)),
    no_international_dialling=PhoneNumberDesc(national_number_pattern='[17]99\\d{4}|69\\d{5,6}', possible_length=(7, 8)),
    national_prefix='0',
    national_prefix_for_parsing='0',
    number_format=[NumberFormat(pattern='(\\d{3})(\\d{4})', format='\\1 \\2', leading_digits_pattern=['[17]99'], national_prefix_formatting_rule='0\\1', national_prefix_optional_when_formatting=True),
        NumberFormat(pattern='(\\d{2})(\\d{5})', format='\\1 \\2', leading_digits_pattern=['80'], national_prefix_formatting_rule='0\\1', national_prefix_optional_when_formatting=True),
        NumberFormat(pattern='(\\d{3})(\\d{4,5})', format='\\1 \\2', leading_digits_pattern=['69'], national_prefix_formatting_rule='0\\1', national_prefix_optional_when_formatting=True),
        NumberFormat(pattern='(\\d{4})(\\d{4,6})', format='\\1 \\2', leading_digits_pattern=['1'], national_prefix_optional_when_formatting=True),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{2})(\\d{2})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['[69]'], national_prefix_formatting_rule='0\\1', national_prefix_optional_when_formatting=True),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['[3578]'], national_prefix_formatting_rule='0\\1', national_prefix_optional_when_formatting=True),
        NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['2[48]'], national_prefix_formatting_rule='0\\1', national_prefix_optional_when_formatting=True),
        NumberFormat(pattern='(\\d{3})(\\d{4})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['2'], national_prefix_formatting_rule='0\\1', national_prefix_optional_when_formatting=True)],
    intl_number_format=[NumberFormat(pattern='(\\d{2})(\\d{5})', format='\\1 \\2', leading_digits_pattern=['80']),
        NumberFormat(pattern='(\\d{4})(\\d{4,6})', format='\\1 \\2', leading_digits_pattern=['1']),
        NumberFormat(pattern='(\\d{2})(\\d{3})(\\d{2})(\\d{2})', format='\\1 \\2 \\3 \\4', leading_digits_pattern=['[69]']),
        NumberFormat(pattern='(\\d{3})(\\d{3})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['[3578]']),
        NumberFormat(pattern='(\\d{2})(\\d{4})(\\d{4})', format='\\1 \\2 \\3', leading_digits_pattern=['2[48]']),
        NumberFormat(pattern='(\\d{3})(\\d{4})(\\d{3})', format='\\1 \\2 \\3', leading_digits_pattern=['2'])])
