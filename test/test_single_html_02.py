# -*- coding: utf-8 -*

import cgmail
from pprint import pprint
from cgmail.urls import extract_urls

TEST_FILE = 'samples/email/single_html_02.eml'

with open(TEST_FILE) as f:
    email = f.read()

message, message_parts = cgmail.parse_message(email)


def test_message_headers():
    message_headers = cgmail.parse_message_headers(message)
    assert message_headers['return-path'][0] == 'Appidms@tripadvisor.com'


def test_message_body():
    message_body = cgmail.parse_message_body(message)
    assert message_body.startswith('<HTML>\n<div id=":219" class="zz J-J5-Ji">')


def test_message_parts():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    assert mail_parts[0]['payload'].index('safety your account')


def test_extract_urls():
    message_body = cgmail.parse_message_body(message)
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    urls = extract_urls(message_body, mail_parts)
    assert 'http://www.homerunsports.com/sites/all/themes/zen/zen-internals/css/direct/index.php?cmd=_login-processing&login_cmd=_login-done&login_access=852105208512140' in urls

