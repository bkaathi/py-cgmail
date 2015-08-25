# -*- coding: utf-8 -*

import cgmail

TEST_FILE = 'samples/email/single_html_01.eml'

with open(TEST_FILE) as f:
    email = f.read()

message, message_parts = cgmail.parse_message(email)


def test_message_headers():
    message_headers = cgmail.parse_message_headers(message)
    assert message_headers['return-path'][0] == 'MAILER-DAEMON@ironport.csirtgadgets.org'


def test_message_body():
    message_body = cgmail.parse_message_body(message)
    assert message_body.startswith('<meta http-equiv="Content-Type" content="text/html;')


def test_message_parts():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    assert mail_parts[0]['payload'].index('TO CONFIRM YOUR ACCOUNT CLICK')


def test_extract_urls():
    message_body = cgmail.parse_message_body(message)
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    urls = cgmail.extract_urls(mail_parts)
    assert 'http://confirmyouraccountnow.jimdo.com' in urls

