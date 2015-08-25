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


def test_message_body():
    message_body = cgmail.parse_message_body(message)
    assert message_body is None


def test_message_parts():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    assert mail_parts[0]['payload'].index('For more information and sign up')
    assert mail_parts[1]['payload'].index('For more information and sign up form visit')


def test_extract_urls():
    message_body = cgmail.parse_message_body(message)
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    urls = cgmail.extract_urls(mail_parts)
    assert "http://jobswalmart.xyz/customer/de/proc/" in urls