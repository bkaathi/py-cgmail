# -*- encoding: utf-8 -*-

import sys
import cgmail
import logging
import textwrap
import json

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'

logger = logging.getLogger(__name__)


def print_json(results):

    # convert dictionary to json and print to screen
    logger.info(json.dumps(results, indent=4, sort_keys=True))


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

    results = cgmail.parse_email_from_string(email) 

    if options.get('urls'):
        u = cgmail.extract_urls(email)
        urls = {
            'urls': list(u)
        }
        results.append(urls)
        print_json(results)
    else:
        print_json(results)

if __name__ == "__main__":
    main()
