#!/usr/bin/env python
# Simple Cloud Files Uploader
# Uploads a file or files to Rackspace Cloud Files
# Author: David Wittman <david@wittman.com>

import argparse
import os
import sys
from contextlib import contextmanager

import cloudfiles

def main():
    "Main execution thread"
    
    args = get_args()

    # if sys.stdin.isatty = false, there is content in stdin
    if len(args.files) is 0 and not sys.stdin.isatty():
        if not args.destination:
            die("Destination filename must be provided with -o")
        files = [sys.stdin]
    elif len(args.files) > 0:
        if len(args.files) > 1 and args.destination:
            die("Destination filename can only be provided for individual "
                + "uploads")
        files = args.files
    else:
        die(usage)

    if not args.apikey or not args.user or not args.container:
        die("Missing Cloud Files account information. Seek help.")

    # Begin upload
    with get_cloudfiles_container(args) as container:
        for _file in files:
            upload_to_cloudfiles(container, _file, args)

def usage():
    sys.stderr.write("usage: %s [options] <filename>\n" % sys.argv[0])

def get_env(value):
    "Gets an environment variable"
    return os.environ.get(value, '')

def die(error):
    try:
        error()
    except TypeError:
        sys.stderr.write("Error: " + error + "\n")
    sys.exit(1)

def get_args():
    desc = "Upload files to Rackspace Cloud Files"

    parser = argparse.ArgumentParser(description=desc)

    conngroup = parser.add_argument_group("Cloud Files Connection Information")
    
    conngroup.add_argument(
        "-k", "--apikey", 
        dest = "apikey", 
        metavar = "<api key>", 
        help = "API key. Defaults to env[CLOUD_FILES_APIKEY]",
        default = get_env('CLOUD_FILES_APIKEY') )

    conngroup.add_argument(
        "-u", "--user", 
        dest = "user", 
        metavar = "<username>", 
        help = "Username. Defaults to env[CLOUD_FILES_USERNAME]",
        default = get_env('CLOUD_FILES_USERNAME') )

    conngroup.add_argument(
        "-s", "--snet",
        action = "store_true",
        dest = "servicenet",
        help = "Use ServiceNet for connections",
        default = False )

    conngroup.add_argument(
        "--uk",
        action = "store_true",
        dest = "uk",
        help = "Use London Auth URL (UK accounts only)",
        default = False)

    outputgroup = parser.add_argument_group("Output options")
    
    outputgroup.add_argument(
        "-o", "--file", 
        dest = "destination", 
        metavar = "<filename>", 
        help = "Destination filename in Cloud Files")

    outputgroup.add_argument(
        "-q", 
        action = "store_true", 
        dest = "quiet", 
        help = "Silence output", 
        default = False)

    parser.add_argument(
        "container",
        help = "Cloud Files container name")

    parser.add_argument(
        "files",
        help = "The file(s) to upload",
        # Accept all of the remaining arguments as filenames
        nargs = '*')

    return parser.parse_args()

@contextmanager
def get_cloudfiles_container(args):
    auth_url = cloudfiles.uk_authurl if args.uk else cloudfiles.us_authurl

    try:
        connection = cloudfiles.get_connection(args.user,
                                               args.apikey,
                                               servicenet=args.servicenet,
                                               authurl=auth_url)
        yield connection.get_container(args.container)
    except cloudfiles.errors.NoSuchContainer:
        die("Container %s does not exist." % args.container)
    except cloudfiles.errors.AuthenticationFailed:
        die("Cloud Files authentication failed.")
    except:
        die("Unknown error establishing connection")
    else:
        del connection

def upload_to_cloudfiles(container, filename, args):
    """
    Upload an object to Cloud Files.
    
    Args:
        container: A cloudfiles container object
        filename: A stream or path to the object to upload.
        args: Arguments Namespace returned by ArgumentParser

    """
    
    destination = args.destination and args.destination \
                                   or  os.path.basename(filename)
    cloudpath = container.create_object(destination)

    # If it's iterable, use CF_storage_object's send method
    if hasattr(filename, "read"):
        cloudpath.send(filename)
    # Upload file to Cloud Files using load_from_filename()
    elif (os.path.exists(filename)):
        cloudpath.load_from_filename(filename)
    else:
        die("File not found")

    if not args.quiet:
        print("File %s uploaded successfully." % destination)
        if container.is_public():
            print("CDN URL: %s/%s" % (container.public_uri(), destination))

if __name__ == '__main__':
    main()

# vim: set expandtab ts=4 sw=4 sts=4:
