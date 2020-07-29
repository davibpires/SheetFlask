import jwt


def generate_jwt(email, access_token=None):
    """Generates a signed JWT."""
    json_dict = {'email': email}

    if access_token:
        json_dict['access_token'] = access_token

    token = jwt.encode(json_dict, 'z6Ct_d2Wy0ZcZZVUYD3beI5ZCSsFrR6-f3ZDyn_MW00')

    return token.decode('UTF-8')
