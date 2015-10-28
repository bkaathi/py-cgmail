# -*- coding: utf-8 -*

import cgmail

TEST_FILE = 'samples/email/multi_mixed_plain_rfc822_plain_01.eml'

with open(TEST_FILE) as f:
    email = f.read()

message, message_parts = cgmail.parse_message(email)


def test_message_headers():
    message_headers = cgmail.parse_message_headers(message)
    assert message_headers['return-path'][0] == '<john@csirtgadgets.org>'


def test_message_parts():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    assert mail_parts[0]['decoded_body'].startswith('phishing message attached')
    assert mail_parts[1]['type'].startswith('message/rfc822')

def test_extract_urls():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    urls = cgmail.extract_urls(mail_parts) # returns a set
    assert "http://www.example.com" in urls

