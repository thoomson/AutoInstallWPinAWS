def password_generator(iteration=16):
    import random

    chars ='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMOPQRSTUVWXYZ0123456789*#%'

    password=''
    i=0

    while i < iteration:
        password += random.choice(chars)
        i += 1
    
    return password