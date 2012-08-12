#!/usr/bin/env python
# Simple Cloud Files Uploader
# Uploads a file or files to Rackspace Cloud Files
# Author: David Wittman <david@wittman.com>

import os
import sys
from contextlib import contextmanager
from optparse import OptionParser, OptionGroup

import cloudfiles

def main():
    "Main execution thread"
    
    (options, args) = get_args()

    # if sys.stdin.isatty = false, there is content in stdin
    if len(args) is 0 and not sys.stdin.isatty():
        if not options.destination:
            die("Destination filename must be provided with -o")
        files = [sys.stdin]
    elif len(args) > 0:
        files = args
    else:
        die(usage)

    if not options.apikey or not options.user or not options.container:
        die("Missing Cloud Files account information. Seek help.")

    # Begin upload
    with get_cloudfiles_container(options) as container:
        for _file in files:
            upload_to_cloudfiles(container, _file, options)

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
    u = "%prog [options] <filename>"
    parser = OptionParser(
        usage = u, 
        description = "Upload a file to Rackspace Cloud Files.")

    conngroup = OptionGroup(parser, "Cloud Files Connection Information")
    
    conngroup.add_option(
        "-k", "--apikey", 
        dest = "apikey", 
        metavar = "<api key>", 
        help = "API key. Defaults to env[CLOUD_FILES_APIKEY]",
        default = get_env('CLOUD_FILES_APIKEY') )

    conngroup.add_option(
        "-u", "--user", 
        dest = "user", 
        metavar = "<username>", 
        help = "Username. Defaults to env[CLOUD_FILES_USERNAME]",
        default = get_env('CLOUD_FILES_USERNAME') )

    conngroup.add_option(
        "-c", "--container", 
        dest = "container", 
        metavar = "<container>", 
        help = "Container name. Defaults to env[CLOUD_FILES_CONTAINER]",
        default = get_env('CLOUD_FILES_CONTAINER') )
    
    conngroup.add_option(
        "-s", "--snet",
        action = "store_true",
        dest = "servicenet",
        help = "Use ServiceNet for connections",
        default = False )

    parser.add_option_group(conngroup)

    outputgroup = OptionGroup(parser, "Output options")
    
    outputgroup.add_option(
        "-o", "--file", 
        dest = "destination", 
        metavar = "<filename>", 
        type = "string", 
        help = "Destination filename")

    outputgroup.add_option(
        "-q", 
        action = "store_true", 
        dest = "quiet", 
        help = "Silence output", 
        default = False)

    parser.add_option_group(outputgroup)

    return parser.parse_args()

@contextmanager
def get_cloudfiles_container(opts):
    try:
        connection = cloudfiles.get_connection(opts.user,
                                               opts.apikey,
                                               servicenet=opts.servicenet)
        yield connection.get_container(opts.container)
    except cloudfiles.errors.NoSuchContainer:
        die("Container %s does not exist." % opts.container)
    except cloudfiles.errors.AuthenticationFailed:
        die("Cloud Files authentication failed.")
    except:
        die("Unknown error establishing connection")
    finally:
        del connection

def upload_to_cloudfiles(container, filename, opts):
    """
    Upload an object to Cloud Files.
    
    Args:
        container: A cloudfiles container object
        filename: A stream or path to the object to upload.
        opts: Options object returned by OptParser

    """
    
    if opts.destination is None:
        destination = os.path.basename(filename)

    cloudpath = container.create_object(destination)

    # If it's iterable, use CF_storage_object's send method
    if hasattr(filename, "read"):
        cloudpath.send(filename)
    # Upload file to Cloud Files using load_from_filename()
    elif (os.path.exists(filename)):
        cloudpath.load_from_filename(filename)
    else:
        die("File not found")

    print("File %s uploaded successfully." % destination)
    if container.is_public():
        print("CDN URL: %s/%s" % (container.public_uri(), destination))

if __name__ == '__main__':
    main()

# vim: set expandtab ts=4 sw=4 sts=4:
