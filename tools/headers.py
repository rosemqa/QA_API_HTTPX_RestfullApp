

class Headers:
    auth_header = lambda token: {'Authorization': f'JWT {token}'}
