# Utilities file to hold helper functions used across the entire project
import urllib.parse as parse


# Helper function to generate letterboxd urls
def get_url(url_string):

    url = "https://letterboxd.com/" + url_string + "/"
    return url


# Helper function to sanitize initial input of username, and ensure corresponds to an actually existing
# letterboxd user
def sanitize_user(user):

    # Sanitize input (to ensure not malicious)
    safe_user = parse.quote(user)

    # Check if input corresponds to a valid letterboxd user
    # TODO: Add user validation here
    valid_user = safe_user

    return valid_user
