#!/usr/bin/env python
# Simple Cloud Files Uploader
# Uploads a single file to Rackspace Cloud Files
# Author: David Wittman <david@wittman.com>

import os
import sys
from optparse import OptionParser, OptionGroup

import cloudfiles

def main():
    """Main execution thread"""
    
    (options, args) = get_args()
    try:
        upload_to_cloudfiles(args[0], options)
    except cloudfiles.errors.NoSuchContainer:
        die("Container %s does not exist." % options.container)
    except cloudfiles.errors.AuthenticationFailed:
        die("Cloud Files authentication failed.")
    except:
        die("Unknown error establishing connection")

def usage():
    sys.stderr.write("usage: %s [options] <filename>\n" % sys.argv[0])


def get_env(value):
    """Gets an environment variable"""
    
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
        dest = "snet",
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

    (opts, args) = parser.parse_args()

    return check_opts(opts, args)

def check_opts(options, args):
    """Make sure we have all the necessary options"""
    
    if len(args) is 1 and sys.stdin.isatty():
        pass
    # if sys.stdin.isatty = true, script is standalone
    elif len(args) is 0 and not sys.stdin.isatty():
        if not options.destination:
            die("Destination filename must be provided with -o")
        args = [sys.stdin]
    else:
        die(usage)
    if not options.apikey or not options.user or not options.container:
        die("Missing Cloud Files account information. Seek help.")

    return (options, args)

def upload_to_cloudfiles(filename, opts):
    """Push the object to Cloud Files.
    
    Args:
        filename: A stream or path to the object to upload.
        opts: Options object returned by OptParser

    """
    
    if opts.destination is None:
        opts.destination = os.path.basename(filename)

    # Establish connection to Cloud Files and open container
    conn = cloudfiles.get_connection(opts.user, opts.apikey, 
                                    servicenet=opts.snet)
    container = conn.get_container(opts.container)
    cloudpath = container.create_object(opts.destination)

    # If it's iterable, use CF_storage_object's send method
    if hasattr(filename, "read"):
        cloudpath.send(filename)
        print("File %s uploaded successfully" % opts.destination)
    # Upload file to Cloud Files using load_from_filename()
    elif(os.path.exists(filename)):
        cloudpath.load_from_filename(filename)
        print("File %s uploaded successfully" % opts.destination)
    else:
        die("File not found")

if __name__ == '__main__':
    main()
