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
    ascii_encoded_body = results[0]['mail_parts'][0]['decoded_body'].encode('ascii', 'ignore')
    assert ascii_encoded_body.startswith('Dear O Acheter Warfarin')

def test_extract_urls():
    urls = list(results[0]['urls'])
    ascii_encoded_url = urls[1].encode('ascii', 'ignore')
    assert 'https://vk.com/away.php?to=http://mediasheet.ru/361389/tadalis-anfordring-levering-tadalafil-generisk-billige"' == ascii_encoded_url
