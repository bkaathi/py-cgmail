# -*- coding: utf-8 -*

import cgmail

TEST_FILE = 'samples/email/multi_mixed_html_application_octet-stream_01.eml'

with open(TEST_FILE) as f:
    email = f.read()

message, message_parts = cgmail.parse_message(email)


def test_message_headers():
    message_headers = cgmail.parse_message_headers(message)
    assert message_headers['return-path'][0] == 'Noreply941@pcgamesupply.com'


def test_message_body():
    message_body = cgmail.parse_message_body(message)
    assert message_body is None


def test_message_parts():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    assert mail_parts[0]['payload'].index('been activity in your account')
    assert mail_parts[1]['payload'].index('<script type="text/javascript"><!--')

