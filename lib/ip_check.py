import re


def ip_check():
    """
    Asks to enter an IP address and checks its validity
    """
    valid_format = re.compile(r'(\d{1,3}\.){3}\d{1,3}$')

    while True:
        raw = input('Please enter the IP address: ')
        if valid_format.match(raw) is not None:
            if all(int(part) < 256 for part in raw.split('.')):
                return raw
            else:
                print('Error: Only numbers within 0-256 are valid for IP addresses!')
        else:
            print('Error: Format mismatch (expected: XXX.XXX.XXX.XXX)!')
