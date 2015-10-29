# -*- coding: utf-8 -*

import cgmail

TEST_FILE = 'samples/email/multi_alternative_plain_html_03.eml'

with open(TEST_FILE) as f:
    email = f.read()

results = cgmail.parse_email_from_string(email)

def test_message_headers():
    assert results[0]['headers']['to'][0] == 'undisclosed-recipients:;'

def test_message_parts():
    assert results[0]['mail_parts'][0]['decoded_body'].startswith(' \n\n-- \n\n [1]')
    assert results[0]['mail_parts'][1]['decoded_body'].startswith('<!DOCTYPE html')

def test_extract_urls():
    urls = cgmail.extract_urls(email)
    assert 'http://geos.info/wp-content/uploads/scotiaonline/SignontoScotiaOnLine.htm' in urls
    assert 'https://www1.scotiaonline.scotiabank.com/online/authentication/authentication.bns' in urls

