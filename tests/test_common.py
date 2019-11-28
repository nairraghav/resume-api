from src import common

required_parameter_list = ["name", "number"]


def test_parameters_in_request_json():
    request_json = {"name": "sample name", "number": 12345}
    assert common.parameters_in_request_json(
        request_json, required_parameter_list
    )


def test_parameters_not_in_request_json():
    request_json = {"name": "sample name", "nomber": 12345}
    assert not common.parameters_in_request_json(
        request_json, required_parameter_list
    )


def test_valid_user_params():
    request_json = {"email_address": "ron@lol.com", "number": 12345}
    assert common.valid_user_params(request_json)


def test_invalid_email_no_domain_user_params():
    request_json = {"email_address": "ron"}
    assert not common.valid_user_params(request_json)


def test_invalid_email_no_top_level_domain_user_params():
    request_json = {"email_address": "ron@lol"}
    assert not common.valid_user_params(request_json)


def test_invalid_email_no_user_user_params():
    request_json = {"email_address": "@lol"}
    assert not common.valid_user_params(request_json)


def test_invalid_password_less_than_4_chars_user_params():
    request_json = {"password": "r0N"}
    assert not common.valid_user_params(request_json)


def test_invalid_password_greater_than_15_chars_user_params():
    request_json = {"password": "Ronaldisa5trongpassword"}
    assert not common.valid_user_params(request_json)


def test_invalid_password_no_numbers_user_params():
    request_json = {"password": "ronald"}
    assert not common.valid_user_params(request_json)


def test_valid_experience_params():
    request_json = {"start_date": "01-01-2019", "end_date": "01-02-2019"}
    assert common.validate_experience_params(request_json)


def test_invalid_start_date_format_experience_params():
    request_json = {"start_date": "2019-01-01"}
    assert not common.validate_experience_params(request_json)


def test_invalid_end_date_format_experience_params():
    request_json = {"end_date": "01-2019-01"}
    assert not common.validate_experience_params(request_json)


def test_invalid_start_date_experience_params():
    request_json = {"start_date": "25-01-2019", "end_date": "01-02-2019"}
    assert not common.validate_experience_params(request_json)


def test_invalid_end_date_experience_params():
    request_json = {"start_date": "01-02-2019", "end_date": "25-01-2019"}
    assert not common.validate_experience_params(request_json)
