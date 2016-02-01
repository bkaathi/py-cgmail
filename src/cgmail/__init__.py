# -*- encoding: utf-8 -*-
__version__ = "0.1.1"

import base64
import sys
import chardet
from pyzmail.parse import message_from_string as pyzmail_message_from_string
from pyzmail.parse import get_mail_parts as pyzmail_get_mail_parts
from pyzmail.parse import decode_text as pyzmail_decode_text
from cgmail.urls import extract_urls as _extract_urls
from cgmail.urls import extract_email_addresses as _extract_email_addresses

RE_URL_PLAIN = r'(https?://[^\s>]+)'

IS_PY2 = sys.version_info < (3, 0)
if not IS_PY2:
    # Helper for Python 2 and 3 compatibility
    unicode = str

def make_compat_str(in_str):
    """
    Tries to guess encoding of [str/bytes] and decode it into
    an unicode object.
    """
    assert isinstance(in_str, (bytes, str, unicode))
    if not in_str:
        return unicode()

    # Chardet in Py2 works on str + bytes objects
    if IS_PY2 and isinstance(in_str, unicode):
        return in_str

    # Chardet in Py3 works on bytes objects
    if not IS_PY2 and not isinstance(in_str, bytes):
        return in_str

    # Detect the encoding now
    enc = chardet.detect(in_str)

    # Decode the object into a unicode object
    out_str = in_str.decode(enc['encoding'])

    # Cleanup: Sometimes UTF-16 strings include the BOM
    if enc['encoding'] == "UTF-16BE":
        # Remove byte order marks (BOM)
        if out_str.startswith('\ufeff'):
            out_str = out_str[1:]

    # Return the decoded string
    return out_str

def parse_message(email):
    message = pyzmail_message_from_string(email)
    parts = pyzmail_get_mail_parts(message)

    return message, parts


def parse_message_headers(msg):

    keys = msg.keys()
    values = msg.values()
    msg_headers = {}

    for k, v in zip(keys, values):
        msg_headers.setdefault(k.lower(), []).append(v)

    return msg_headers


def decode_text(p, d):

    if p.charset:
        try:
            #d['decoded_body'] = p.get_payload().decode(p.charset).encode('ascii', 'replace')
            d['decoded_body'] = p.get_payload().decode(p.charset)
        except (UnicodeDecodeError, LookupError): 
            #d['decoded_body'] = make_compat_str(p.get_payload()).encode('ascii', 'replace')
            d['decoded_body'] = make_compat_str(p.get_payload())
    else:
        #d['decoded_body'] = make_compat_str(p.get_payload()).encode('ascii', 'replace')
        d['decoded_body'] = make_compat_str(p.get_payload())

    return d

    
def get_decoded_body(p, d):

    if p.type == "text/plain" and p.is_body == "text/plain":
        d = decode_text(p, d)
    elif p.type == "text/html" and p.is_body == "text/html":
        d = decode_text(p, d)

    return d


def get_messages_as_attachments(message):
   
    results = []

    msg = message.get_payload()
    if isinstance(msg, list):
        for z in msg:
            if z.get_content_type() == "message/rfc822":
                attachments = z.get_payload()
                if attachments:
                    for attachment in attachments:
                        a = {
                            'type': z.get_content_type(),
                            'attachment': str(attachment),
                        }
                        results.append(a)
    return results
 

def process_part_type(p, d):

    if p.type == "text/plain" or p.type == "text/html":
        d = get_decoded_body(p, d)
    elif p.type.startswith('application'):
        d['base64_encoded_payload'] = base64.b64encode(p.get_payload())
    
    return d


def parse_message_parts(message_parts):
    mail_parts = []
    for p in message_parts:
        d = {
            'charset': p.charset,
            'content_id': p.content_id,
            'description': p.description,
            'disposition': p.disposition,
            'filename': p.filename,
            'is_body': p.is_body,
            'sanitized_filename': p.sanitized_filename,
            'type': p.type,
            'decoded_body': None,
            'base64_encoded_payload': None,
        }

        d = process_part_type(p, d)

        mail_parts.append(d)

    return mail_parts


def extract_urls(mail_parts):

    links = set()

    #results = parse_email_from_string(email)

    for mail_part in mail_parts:
        if mail_part['is_body']:
            if mail_part['is_body'].startswith('text/html'):
                l = _extract_urls(mail_part['decoded_body'], html=True)
                links.update(l)
            if mail_part['is_body'].startswith('text/plain'):
                l = _extract_urls(mail_part['decoded_body'], html=False)
                links.update(l)
    return links

def extract_email_addresses(mail_parts):

    email_addresses = set()

    for mail_part in mail_parts:
        if mail_part['is_body']:
            if mail_part['is_body'].startswith('text/html'):
                email_address = _extract_email_addresses(mail_part['decoded_body'], html=True)
                email_addresses.update(email_address)
            if mail_part['is_body'].startswith('text/plain'):
                email_address = _extract_email_addresses(mail_part['decoded_body'], html=False)
                email_addresses.update(email_address)

    return email_addresses

def flatten(s):
    if s == []:
        return s
    if isinstance(s[0], list):
        return flatten(s[0]) + flatten(s[1:])
    return s[:1] + flatten(s[1:])


def parse_attached_emails(attachments):
    flattened = []
    for a in attachments:
        if a['type'] == "message/rfc822":
            d = parse_email_from_string(a['attachment'])
            flattened = flatten(d)
    return flattened
 

def parse_email_from_string(email):

    results = []

    d = {}

    # parse email into message and message parts
    message, message_parts = parse_message(email)

    # get message headers
    d['headers'] = message_headers = parse_message_headers(message)

    # get mail parts
    d['mail_parts'] = mail_parts = parse_message_parts(message_parts)

    # get attachments
    attachments = get_messages_as_attachments(message)

    # get urls from message body
    d['urls'] = urls = extract_urls(mail_parts)

    # get email addresses from message body
    d['body_email_addresses'] = email_addresses = extract_email_addresses(mail_parts)

    # find encapsulated emails in attachments
    attached_emails = parse_attached_emails(attachments)
    for attached_email in attached_emails:
        results.append(attached_email)

    results.append(d)

    return results
