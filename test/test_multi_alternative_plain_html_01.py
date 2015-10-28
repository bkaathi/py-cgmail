# -*- coding: utf-8 -*

import cgmail
from pprint import pprint

TEST_FILE = 'samples/email/multi_alternative_plain_html_01.eml'

with open(TEST_FILE) as f:
    email = f.read()

message, message_parts = cgmail.parse_message(email)


def test_message_headers():
    message_headers = cgmail.parse_message_headers(message)
    assert message_headers['return-path'][0] == 'career@walmart.com'

def test_message_parts():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    assert mail_parts[0]['decoded_body'].startswith(' \n\nYou have been selected')
    assert mail_parts[1]['decoded_body'].startswith('<!DOCTYPE HTML PUBLIC')

def test_extract_urls():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    urls = cgmail.extract_urls(mail_parts) # returns a set
    assert "http://jobswalmart.xyz/customer/de/proc/" in urls
