def generate_secret_key():
    import os
    return os.urandom(1024).encode('hex')
