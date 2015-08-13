import sys
import cgmail
import json

# Why does this file exist, and why __main__?
# For more info, read:
# - https://www.python.org/dev/peps/pep-0338/
# - https://docs.python.org/2/using/cmdline.html#cmdoption-m
# - https://docs.python.org/3/using/cmdline.html#cmdoption-m

def main(argv=sys.argv):

    if len(argv) <= 1:
        print("ERROR: No file path given")
        sys.exit(0)

    try:
        with open(argv[1]) as f:
            email = f.read()
    except FileNotFoundError:
        print("ERROR: File not found")
        sys.exit(0)

    # parse email into message and message parts
    message, message_parts = cgmail.parse_message(email)

    # get message headers from message
    message_headers = cgmail.parse_message_headers(message)

    # get message body from message
    message_body = cgmail.parse_message_body(message)

    # get message parts
    mail_parts = cgmail.parse_message_parts(message_parts)  # returns an array of dictionaries

    # dictionary of data structures
    d = {
        'headers': message_headers,
        'message_body': message_body,
        'mail_parts': mail_parts
    }

    print(json.dumps(d, indent=4, sort_keys=True))


if __name__ == "__main__":
    sys.exit(main())
