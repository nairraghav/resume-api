import re
from datetime import datetime


def parameters_in_request_json(request_json, parameter_list):
    for parameter in parameter_list:
        if parameter not in request_json:
            return False
    return True


def valid_user_params(request_json):
    email_regex = re.compile("[^@]+@[^@]+\\.[^@]+")
    password_regex = re.compile("^(?=.*\\d).{4,15}$")
    if "email_address" in request_json:
        if not email_regex.match(request_json["email_address"]):
            return False
    if "password" in request_json:
        if not password_regex.match(request_json["password"]):
            return False
    return True


def validate_experience_params(request_json):
    if "start_date" in request_json:
        try:
            datetime.strptime(request_json["start_date"], "%m-%d-%Y")
        except ValueError:
            return False
    if "end_date" in request_json:
        try:
            datetime.strptime(request_json["end_date"], "%m-%d-%Y")
        except ValueError:
            return False
    return True
