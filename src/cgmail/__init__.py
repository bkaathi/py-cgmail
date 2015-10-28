# -*- encoding: utf-8 -*-
__version__ = "0.1.1"

from pyzmail.parse import message_from_string as pyzmail_message_from_string
from pyzmail.parse import get_mail_parts as pyzmail_get_mail_parts
from pyzmail.parse import decode_text as pyzmail_decode_text
from cgmail.urls import extract_urls as _extract_urls

# remove when done testing
from pprint import pprint

RE_URL_PLAIN = r'(https?://[^\s>]+)'


def parse_message(email):
    message = pyzmail_message_from_string(email)
    parts = pyzmail_get_mail_parts(message)

    return message, parts


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


def decode_text(p, d):

    if p.charset:
        try:
            d['decoded_body'] = p.get_payload().decode(p.charset)
        except (UnicodeDecodeError, LookupError):
            _decoded_body = pyzmail_decode_text(p.get_payload(), None, None)
            d['decoded_body'] = _decoded_body[0]
    else:
        _decoded_body = pyzmail_decode_text(p.get_payload(), None, None)
        d['decoded_body'] = _decoded_body[0]

    return d

    
def get_decoded_body(p, d):

    if p.type == "text/plain" and p.is_body == "text/plain":
        d = decode_text(p, d)
    elif p.type == "text/html" and p.is_body == "text/html":
        d = decode_text(p, d)

    return d

def get_attachments(message):
   
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
    elif p.type == "application/octet-stream":
        #need to process attached files here (e.g. .html)
        pass
    elif p.type == "application/zip":
        # need to extract zip files here
        pass
    elif p.type == "application/pdf":
        # process pdf's
        pass
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
        }

        d = process_part_type(p, d)

        mail_parts.append(d)

    return mail_parts


def extract_urls(mail_parts):
    
    links = set()
    
    for p in mail_parts:
        html = False

        if p['is_body']:
            if p['is_body'].startswith('text/html'):
                html = True
                l = _extract_urls(p['decoded_body'], html=html)
                links.update(l)
        
            if p['is_body'].startswith('text/plain'):
                l = _extract_urls(p['decoded_body'], html=html)
                links.update(l)

    return links

def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(s[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])

def parse_attached_emails(attachments):
    flattened = []
    for a in attachments:
        if a['type'] == "message/rfc822":
            d = parse_email_to_dict(a['attachment'])
            flattened = flatten(d)
    return flattened
 

def parse_email_to_dict(email):

    results = []

    # parse email into message and message parts
    message, message_parts = parse_message(email)

    # get message headers
    message_headers = parse_message_headers(message)

    # get mail parts
    mail_parts = parse_message_parts(message_parts)

    # get attachments
    attachments = get_attachments(message)

    # get attached emails
    attached_emails = parse_attached_emails(attachments)
    for email in attached_emails:
        results.append(email)

    '''
    # testing
    if attachments:
        for a in attachments:
            if a['type'] == "message/rfc822":
                d = parse_email_to_dict(a['attachment'])
                
                flattened = flatten(d)
                for f in flattened:
                    results.append(f)
    '''            
    # extract urls from message body and mail parts
    urls = extract_urls(mail_parts)

    # create dictionary of data structures
    d = {
        'headers': message_headers,
        'mail_parts': mail_parts,
        'attachments': attachments,
        'urls': urls,
    }

    results.append(d)

    return results

