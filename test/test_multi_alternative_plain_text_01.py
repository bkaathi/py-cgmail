# -*- coding: utf-8 -*

import cgmail
from pprint import pprint

TEST_FILE = 'samples/email/multi_alternative_plain_text_01.eml'

with open(TEST_FILE) as f:
    email = f.read()

results = cgmail.parse_email_from_string(email)

def test_message_headers():
    assert results[0]['headers']['return-path'][0] == '<suppbaby@example.com>'

def test_message_parts():
    assert results[0]['mail_parts'][0]['decoded_body'].startswith("Dear O\xc3\xb9")

def test_extract_urls():
    urls = list(results[0]['urls'])
    assert 'http://www.geldfa.de/3957/generic-ranitidine-online-pharmacy-canadian-zantac-compresse' == urls[0]
