# -*- coding: utf-8 -*

import cgmail

TEST_FILE = 'samples/email/multi_mixed_plain_rfc822_mixed_plain_rfc822_plain_01.eml'

with open(TEST_FILE) as f:
    email = f.read()

results = cgmail.parse_email_from_string(email)

def test_message_headers():
    assert results[0]['headers']['return-path'][0] == '<john@csirtgadgets.org>'
    assert results[1]['headers']['to'][0].startswith('John <john@csirtgadgets.org>')
    assert results[2]['headers']['to'][0].startswith('John <john@csirtgadgets.org>')

def test_message_parts():
    assert results[0]['mail_parts'][0]['decoded_body'].startswith('give me your credentials')
    assert results[1]['mail_parts'][0]['decoded_body'].startswith('phishing message attached')
    assert results[2]['mail_parts'][0]['decoded_body'].startswith('forward attachment of attachment')

def test_extract_urls():
    assert "http://www.example.com" in results[0]['urls']

