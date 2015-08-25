# -*- encoding: utf-8 -*-

import sys
import cgmail
import json
import logging
import textwrap
from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

logger = logging.getLogger(__name__)


def print_json(message_headers, message_body, mail_parts):

    # create dictionary of data structures
    d = {
        'headers': message_headers,
        'message_body': message_body,
        'mail_parts': mail_parts,
    }

    # convert dictionary to json and print to screen
    logger.info(json.dumps(d, indent=4, sort_keys=True))
        

def main():

    #
    # initialize module
    #

    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ cat test.eml | cgmail -v
            $ cgmail --file test.eml
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='cgmail'
    )

    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument("-f", "--file", dest="file", help="specify email file")
    p.add_argument('--urls', action='store_true')

    args = p.parse_args()

    loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)

    options = vars(args)

    #
    # get email from file or stdin
    #

    if options.get("file"):
        with open(options["file"]) as f:
            email = f.read()
    else:
        email = sys.stdin.read()

    #
    # parse email message
    #

    # parse email into message and message parts
    message, message_parts = cgmail.parse_message(email)

    # get message headers, body and mail parts
    message_body = cgmail.parse_message_body(message)
    message_headers = cgmail.parse_message_headers(message)
    mail_parts = cgmail.parse_message_parts(message_parts)

    # extract urls from message body and mail parts
    #urls = cgmail.extract_urls(message_body, mail_parts)

    if options.get('urls'):
        urls = cgmail.extract_urls(mail_parts)
        for u in urls:
            logger.info(u)
    else:
        print_json(message_headers, message_body, mail_parts)

if __name__ == "__main__":
    main()
