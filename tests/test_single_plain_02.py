# -*- coding: utf-8 -*

import cgmail
from pprint import pprint

file = 'samples/email/single_plain_02.eml'

with open(file) as f:
    email = f.read()

message, message_parts = cgmail.parse_message(email)


def test_message_headers():
    message_headers = cgmail.parse_message_headers(message)
    assert message_headers['return-path'][0] == '<john@csirtgadgets.org>'
    #pprint(message_headers['Return-Path'][0])

def test_message_body():
    message_body = cgmail.parse_message_body(message)
    assert message_body.startswith('http://www.indiana.edu')
    #pprint(message_body)


def test_message_parts():
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    assert mail_parts[0]['payload'].startswith('http://www.indiana.edu')
    #pprint(mail_parts[0])

def test_extract_urls():
    message_body = cgmail.parse_message_body(message)
    mail_parts = cgmail.parse_message_parts(message_parts) # returns an array of dictionaries
    urls = cgmail.extract_urls(message_body, mail_parts)
    assert 'http://www.indiana.edu' in urls

