# -*- coding: utf-8 -*

import cgmail
from pprint import pprint

file = 'samples/email/multi_mixed_plain_rfc822_plain_02.eml'

with open(file) as f:
    email = f.read()

message, message_parts = cgmail.parse_message(email)


def test_message_headers():
    message_headers = cgmail.parse_message_headers(message)
    assert message_headers['return-path'][0] == '<john@csirtgadgets.org>'

def test_message_body():
    message_body = cgmail.parse_message_body(message)
    assert message_body == None

def test_message_parts():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    assert mail_parts[0]['payload'].startswith('forward attachment as inline?')
    assert mail_parts[1]['payload'].index('give me your credentials')
