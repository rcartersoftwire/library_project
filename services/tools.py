# Encode Passwords using secret key
def encode(key, string):
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string

# Compare dates and return True if it is later
def check_if_late(due_date, prime_date):
    from datetime import date
    late = False

    due_date = due_date.split('/')
    due_date = [int(x) for x in due_date]
    due_date = date(due_date[2]+2000, due_date[1], due_date[0])
    
    prime_date = prime_date.split('/')
    prime_date = [int(x) for x in prime_date]
    prime_date = date(prime_date[2]+2000, prime_date[1], prime_date[0])
    
    if due_date < prime_date:
        late = True

    return late
