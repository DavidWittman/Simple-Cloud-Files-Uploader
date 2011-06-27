#!/usr/bin/env python
#
# Rackspace Cloud Files Uploader
# by:   David Wittman <david@wittman.com>,
#       Jordan Callicoat <monkeesage@gmail.com>
#

import cloudfiles
import os
import sys
from optparse import OptionParser, OptionGroup

# Rackspace Cloud Files API Information (temporary)
username = ""
api_key = ""
container_name = ""

def main():
    errors = []

    (options, args) = get_args()
    if len(args) is 0:
        if not options.filename:
            die(["Destination filename must be provided with -o"])
        else:
            args = [sys.stdin]
    elif len(args) > 1:
        die(["Invalid number of arguments."])

    # TODO: test for valid options and accept environment variables
    try:
        upload_to_cloudfiles(args[0], options.filename)
    except cloudfiles.errors.NoSuchContainer:
        errors.append("Container %s does not exist." % container_name)
    except cloudfiles.errors.AuthenticationFailed:
        errors.append("Cloud Files authentication failed.")
    
    die(errors)

def die(errors):
    if errors:
        for error in errors:
            sys.stderr.write("Error: " + error + "\n")
        sys.exit(1)

def get_args():
    usage = "usage: %prog [options] filename"
    parser = OptionParser(usage=usage,description="Upload a file to Rackspace Cloud Files.")

    conngroup = OptionGroup(parser, "Cloud Files Connection Information")
    conngroup.add_option("-k", "--apikey", dest="apikey", metavar="<api key>", help="API key. Defaults to env[CLOUD_FILES_APIKEY]")
    conngroup.add_option("-u", "--user", dest="user", metavar="<username>", help="Username. Defaults to env[CLOUD_FILES_USERNAME]")
    conngroup.add_option("-c", "--container", dest="container", metavar="<container>", help="Container name. Defaults to env[CLOUD_FILES_CONTAINER]")
    parser.add_option_group(conngroup)

    outputgroup = OptionGroup(parser, "Output options")
    outputgroup.add_option("-o", "--file", dest="filename", metavar="<filename>", type="string", help="Destination filename")
    outputgroup.add_option("-s", action="store_true", dest="silent", help="Silence output", default=False)
    parser.add_option_group(outputgroup)

    return parser.parse_args()

def upload_to_cloudfiles(filename, destination):
    if destination is None:
        destination = os.path.basename(filename)

    # Establish connection to Cloud Files and open container
    conn = cloudfiles.get_connection(username, api_key, servicenet=True)
    container = conn.get_container(container_name)
    cloudpath = container.create_object(destination)

    # If it's iterable, use CF_storage_object's send method
    if hasattr(filename, "read"):
        cloudpath.send(filename)
    # Upload file to Cloud Files using load_from_filename()
    elif(os.path.exists(filename)):
        cloudpath.load_from_filename(filename)
        print("File %s uploaded successfully" % filename)
    else:
        print("File not found")

if __name__ == '__main__':
    main()
