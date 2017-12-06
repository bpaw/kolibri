from __future__ import absolute_import, print_function, unicode_literals

import json
import logging

from django.core.management.base import BaseCommand
from kolibri.core.webpack.hooks import WebpackBundleHook
# from kolibri.plugins.registry import initialize
import django
from django.conf import settings

settings.configure()
django.setup()

import kolibri.plugins.registry

import argparse

logger = logging.getLogger(__name__)


# class Command(BaseCommand):
#     help = 'Creates a new schema'  # @ReservedAssignment

# def add_arguments(self, parser):
#     parser.add_argument('--outputfile', type=str, default=None, dest="output_file")
#     parser.add_argument('-r', type=str, default=None, dest="input_file")

def handle(options):

    # logging.debug(args)

    print("YO HERE DOG\n")
    for hook in WebpackBundleHook().registered_hooks:
        print("right here:"%hook.webpack_bundle_data)

    result = []
    if "read" in options:
        input_file = open(options['read'], 'r').read().split('\n')
        input_file = filter(None, input_file)
        result = [hook.webpack_bundle_data for hook in WebpackBundleHook().registered_hooks if (hook.webpack_bundle_data and any(hook.__module__.startswith(input) for input in input_file))]
    else:
        result = [hook.webpack_bundle_data for hook in WebpackBundleHook().registered_hooks if hook.webpack_bundle_data]

    if "outputfile" in options:
        logger.info("Writing webpack_json output to {}".format(options["outputfile"]))
        with open(options["outputfile"], "w") as f:
            json.dump(result, f)
    else:
        logger.info("No output file argument; writing webpack_json output to stdout.")
        print(json.dumps(result))


# Executable code below

def main():

    print("argparse initialization")
    parser = argparse.ArgumentParser(description="Command for building kolibri front end webpack dependencies")
    parser.add_argument("-o", "--outputfile", help="provide a name for the file to create that will contain the JSON objects to send to Webpack")
    parser.add_argument("-r", "--read", help="provide a file to parse", action="store")

    args = parser.parse_args()
    options = {}
    if args.read:
        print("-r / --read flag was presented with : %s"%args.read)
        options["read"] = args.read
    else:
        print("No -r / --read flags given")

    if args.outputfile:
        options["outputfile"] = args.outputfile
        print("-r / --read flag was presented with : %s"%args.read)
    else:
        print("No -r / --read flags given")

    print(options)

    print("Bout to call handle()")
    handle(options)

main()