# -*- coding: utf-8 -*

import cgmail
from pprint import pprint

TEST_FILE = 'samples/email/multi_mixed_plain_application_zip.eml'


with open(TEST_FILE) as f:
    email = f.read()

message, message_parts = cgmail.parse_message(email)


def test_message_headers():
    message_headers = cgmail.parse_message_headers(message)
    print(type(message_headers))
    assert message_headers['return-path'][0] == '<xeroxesgt2@raininboxes.com>'

def test_message_parts():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    assert mail_parts[0]['decoded_body'].startswith('Sir/Madam\n\nUpon')
    assert mail_parts[1]['filename'].startswith('PaymentAdvice_Ref')
    assert mail_parts[2]['type'].startswith('text/plain')

