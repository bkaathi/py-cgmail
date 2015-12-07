# -*- coding: utf-8 -*

import cgmail
from pprint import pprint
from cgmail.urls import extract_urls

TEST_FILE = 'samples/email/single_html_03.eml'

with open(TEST_FILE) as f:
    email = f.read()

results = cgmail.parse_email_from_string(email)

pprint(results)

def test_message_headers():
    assert results[0]['headers']['return-path'][0] == '<advertisebz09ua@gmail.com>'

def test_body_email_addresses():
    assert "dhlcourier.c1950@outlook.com" in results[0]['body_email_addresses']

