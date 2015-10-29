# -*- coding: utf-8 -*

import cgmail

TEST_FILE = 'samples/email/single_plain_02.eml'

with open(TEST_FILE) as f:
    email = f.read()

results = cgmail.parse_email_from_string(email)

def test_message_headers():
    assert results[0]['headers']['return-path'][0] == '<john@csirtgadgets.org>'

def test_message_parts():
    assert results[0]['mail_parts'][0]['decoded_body'].startswith('http://www.indiana.edu')

def test_extract_urls():
    urls = cgmail.extract_urls(email)
    assert "http://www.indiana.edu" in urls

