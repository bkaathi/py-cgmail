# -*- coding: utf-8 -*

import cgmail

TEST_FILE = 'samples/email/single_plain_03.eml'

with open(TEST_FILE) as f:
    email = f.read()

results = cgmail.parse_email_from_string(email)

def test_message_headers():
    assert results[0]['headers']['return-path'][0] == '<john@csirtgadgets.org>'

def test_body_email_addresses():
    assert "yyounisammaarah2015@gmail.com" in results[0]['body_email_addresses']
