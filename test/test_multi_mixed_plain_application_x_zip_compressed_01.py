# -*- coding: utf-8 -*

import cgmail

TEST_FILE = 'samples/email/multi_mixed_plain_application_x_zip_compressed_01.eml'

with open(TEST_FILE) as f:
    email = f.read()

results = cgmail.parse_email_from_string(email)

def test_message_headers():
    assert results[0]['headers']['to'][0] == 'Larry <larry@example.com>'

def test_message_parts():
    assert results[0]['mail_parts'][0]['decoded_body'].startswith('See the attached zip file')
    assert results[0]['mail_parts'][1]['base64_encoded_payload'].startswith('UEsDBBQACAAIAO')

