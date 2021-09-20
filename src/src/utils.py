"""
Utils module to hold helper functions used across project
"""
import urllib.parse as parse

# Constants

LETTERBOXD = "letterboxd"
LETTERBOXD_URL = "https://letterboxd.com/"
LETTERBOXD_DOMAIN = "letterboxd.com"


# Util functions

def get_url(url_string):
    """
    Generate letterboxd url from input string

    :param url_string: url params to include off of base letterboxd url
    :return: formatted letterboxd url
    """

    url = LETTERBOXD_URL + url_string + "/"
    return url


def sanitize_user(user):
    """
    Sanitize initial input of username, and ensure corresponds to an actually existing letterboxd user

    :param user: Inputted username
    :return: Sanitized username
    """

    safe_user = parse.quote(user)

    # TODO: Add user validation here
    valid_user = safe_user

    return valid_user
