# -*- encoding: utf-8 -*-

# Why does this file exist, and why __main__?
# For more info, read:
# - https://www.python.org/dev/peps/pep-0338/
# - https://docs.python.org/2/using/cmdline.html#cmdoption-m
# - https://docs.python.org/3/using/cmdline.html#cmdoption-m
# - https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/

import sys
import cgmail
import json
import logging
import os.path
import textwrap
import yaml

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter
from cifsdk.client import Client
from cifsdk.observable import Observable

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s[%(lineno)s] - %(message)s'
REMOTE_DEFAULT = "http://localhost:5000"

def print_json(message_headers,message_body,mail_parts,urls):

    # turn set into list to serialize in json
    list_urls = list(urls)

    # create dictionary of data structures
    d = {
        'headers': message_headers,
        'message_body': message_body,
        'mail_parts': mail_parts,
        'urls': list_urls
    }

    # convert dictionary to json and print to screen
    print(json.dumps(d, indent=4, sort_keys=True))


def submit_to_cif(logger,options,urls):

    # initialize cif client
    cli = Client(remote=options["remote"], token=options["token"], no_verify_ssl=options["no_verify_ssl"])

    for u in urls:
        logger.info("submitting: {0}".format(u))

        o = Observable(
            observable=u,
            confidence=options["confidence"],
            tlp=options["tlp"],
            group=options["group"],
            tags=options["tags"],
            provider=options["provider"]
        )
        r = cli.submit(submit=str(o))
        logger.info("submitted: {0}".format(r))

def main():

    #
    # initialize module
    #

    p = ArgumentParser(
        description=textwrap.dedent('''\
        example usage:
            $ cat test.eml | cif-procmail -v
            $ cif-procmail --file test.eml
        '''),
        formatter_class=RawDescriptionHelpFormatter,
        prog='cif-procmail'
    )

    p.add_argument("-v", "--verbose", dest="verbose", action="count",
                   help="set verbosity level [default: %(default)s]")
    p.add_argument('-d', '--debug', dest='debug', action="store_true")
    p.add_argument("-f", "--file", dest="file", help="specify email file")
    p.add_argument('-p', '--print', dest='print_stdout', action='store_true',
                   default=False, help='print json to stdout')
    p.add_argument('--cif-urls', dest='cif_urls', action='store_true', help='submit extracted urls to CIF')

    # cif arguments
    p.add_argument("--confidence", help="specify confidence for submitting to CIF", default="65")
    p.add_argument("--remote", help="specify CIF remote [default: %(default)s",
                   default=REMOTE_DEFAULT)
    p.add_argument("--token", help="specify CIF token")
    p.add_argument("--config", help="specify CIF config [default: %(default)s",
                   default=os.path.expanduser("~/.cif.yml"))
    p.add_argument("--tags", help="specify CIF tags [default: %(default)s", default=["phishing"])
    p.add_argument("--group", help="specify CIF group [default: %(default)s", default="everyone")
    p.add_argument("--tlp", help="specify CIF TLP [default: %(default)s", default="amber")
    p.add_argument("--no-verify-ssl", action="store_true", default=False)
    p.add_argument("--raw", help="include raw message data")
    p.add_argument("--raw-headers", help="include raw header data", action="store_true")
    p.add_argument("--provider", help="specify feed provider [default: %(default)s", default="localhost")

    args = p.parse_args()

    loglevel = logging.WARNING
    if args.verbose:
        loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG

    console = logging.StreamHandler()
    logging.getLogger('').setLevel(loglevel)
    console.setFormatter(logging.Formatter(LOG_FORMAT))
    logging.getLogger('').addHandler(console)
    logger = logging.getLogger(__name__)

    options = vars(args)

    if os.path.isfile(args.config):
        f = file(args.config)
        config = yaml.load(f)
        f.close()
        if not config['client']:
            raise Exception("Unable to read " + args.config + " config file")
        config = config['client']
        for k in config:
            if not options.get(k):
                options[k] = config[k]

        if config.get("remote") and options["remote"] == REMOTE_DEFAULT:
            options["remote"] = config["remote"]

    else:
        logger.info("{} config does not exist".format(args.config))

    #
    # get email from file or stdin
    #

    if not options.get("remote"):
        logger.critical("missing --remote")
        raise SystemExit

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
    urls = cgmail.extract_urls(message_body, mail_parts)

    if args.print_stdout:
        print_json(message_headers,message_body,mail_parts,urls)

    #
    # submit urls to a CIF instance
    #

    if args.cif_urls:
        submit_to_cif(logger,options,urls)

if __name__ == "__main__":
    main()
