# -*- coding: utf-8 -*

import cgmail

TEST_FILE = 'samples/email/multi_alternative_plain_html_03.eml'

with open(TEST_FILE) as f:
    email = f.read()

message, message_parts = cgmail.parse_message(email)


def test_message_headers():
    message_headers = cgmail.parse_message_headers(message)
    assert message_headers['to'][0] == 'undisclosed-recipients:;'


def test_message_body():
    message_body = cgmail.parse_message_body(message)
    assert message_body is None


def test_message_parts():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    assert mail_parts[0]['payload'].startswith(' \n\n-- \n\n [1]')


def test_extract_urls():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    urls = cgmail.extract_urls(mail_parts)
    assert 'http://geos.info/wp-content/uploads/scotiaonline/SignontoScotiaOnLine.htm' in urls

