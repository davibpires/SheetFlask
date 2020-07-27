import jwt


def generate_jwt(email):
    token = jwt.encode({'email': email}, 'z6Ct_d2Wy0ZcZZVUYD3beI5ZCSsFrR6-f3ZDyn_MW00')
    return token.decode('UTF-8')
