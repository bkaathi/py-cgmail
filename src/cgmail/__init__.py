# -*- encoding: utf-8 -*-
__version__ = "0.1.0"

from pyzmail.parse import message_from_string as pyzmail_message_from_string
from pyzmail.parse import get_mail_parts as pyzmail_get_mail_parts
from pyzmail.parse import decode_text as pyzmail_decode_text
from cgmail.urls import extract_urls as _extract_urls

RE_URL_PLAIN = r'(https?://[^\s>]+)'


def parse_message(email):
    message = pyzmail_message_from_string(email)
    parts = pyzmail_get_mail_parts(message)
    return message, parts


def parse_message_body(msg):
    # Do we need to process text/plain and text/html separately? 
    # It's not clear to me that we do. 
    body = None
    if msg.get_content_type() == "text/plain":
        body = msg.get_payload(decode=True)
        if body:
            if msg.get_charset():
                decoded_body = pyzmail_decode_text(body, msg.get_charset(), None)
                body = decoded_body[0]
            elif msg.get_charsets():
                for c in msg.get_charsets():
                    decoded_body = pyzmail_decode_text(body, c, None)
                    body = decoded_body[0]
            else:
                decoded_body = pyzmail_decode_text(body, msg.get_charset(), None)
                body = decoded_body[0]
    elif msg.get_content_type() == "text/html":
        body = msg.get_payload(decode=True)
        if body:
            if msg.get_charset():
                decoded_body = pyzmail_decode_text(body, msg.get_charset(), None)
                body = decoded_body[0]
            elif msg.get_charsets():
                for c in msg.get_charsets():
                    decoded_body = pyzmail_decode_text(body, c, None)
                    body = decoded_body[0]
            else:
                decoded_body = pyzmail_decode_text(body, msg.get_charset(), None)
                body = decoded_body[0]
    return body


def parse_message_headers(msg):
    msg_headers = {}
    for header in msg.keys():
        header = header.lower()
        value = msg.get_decoded_header(header)
        try:
            msg_headers[header].append(value)
        except KeyError:
            msg_headers[header] = [value]
    return msg_headers


def parse_message_parts(message_parts):
    mail_parts = []
    for p in message_parts:
        d = {}
        d["charset"] = p.charset
        d["content_id"] = p.content_id
        d["description"] = p.description
        d["filename"] = p.filename
        d["is_body"] = p.is_body
        d["sanitized_filename"] = p.sanitized_filename
        d["type"] = p.type

        if p.charset:
            try:
                d["payload"] = p.get_payload().decode(p.charset)
            except UnicodeDecodeError:
                decoded_body = pyzmail_decode_text(p.get_payload(), None, None)
                d["payload"] = decoded_body[0]
        else:
            decoded_body = pyzmail_decode_text(p.get_payload(), None, None)
            d["payload"] = decoded_body[0]
        mail_parts.append(d)
    return mail_parts


def extract_urls(parts):

    links = set()
    for p in parts:
        html = False
        if p['type'].startswith('text/html'):
            html = True

        l = _extract_urls(p['payload'], html=html)

        links.update(l)

    return links

def parse_email_to_dict(email):

    # parse email into message and message parts
    message, message_parts = parse_message(email)

    # get message headers, body and mail parts
    message_body = parse_message_body(message)
    message_headers = parse_message_headers(message)
    mail_parts = parse_message_parts(message_parts)

    # extract urls from message body and mail parts
    urls = list(extract_urls(message_body, mail_parts))

    # create dictionary of data structures
    d = {
        'headers': message_headers,
        'message_body': message_body,
        'mail_parts': mail_parts,
        'urls': urls
    }

    return d
