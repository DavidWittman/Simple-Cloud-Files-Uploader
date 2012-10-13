# Simple Cloud Files Uploader
Python script to quickly upload files to Rackspace Cloud Files or Openstack swift. Originally developed to make one-liner uploads more manageable. Supports input via file arguments or standard input.

## Installation
For the love of Guido, use [virtualenv](http://www.virtualenv.org/en/latest/index.html) with whichever of the following methods you choose:

### pip
`pip install cfupload`

### EasyInstall
`easy_install cfupload`

### setuptools
```
git clone git://github.com/DavidWittman/Simple-Cloud-Files-Uploader.git
cd Simple-Cloud-Files-Uploader
python setup.py install
```

## Usage

```
usage: cfupload [-h] [-k <api key>] [-u <username>] [-a <auth_url>] [-s]
                    [-o <filename>] [-q] [-c]
                    container [files [files ...]]

    Upload files to Rackspace Cloud Files or Openstack Swift.

    positional arguments:
      container             Container name in Cloud Files or Openstack Swift
      files                 The file(s) to upload

    optional arguments:
      -h, --help            show this help message and exit

    Cloud Files Connection Information:
      -k <api key>, --apikey <api key>
                            API key. Defaults to env[CLOUD_FILES_APIKEY]
      -u <username>, --user <username>
                            Username. Defaults to env[CLOUD_FILES_USERNAME]
      -a <auth_url>, --auth <auth_url>
                            Authentiction end point. Defaults to
                            env[CLOUD_FILE_AUTHENTICAION_URL]
      -s, --snet            Use ServiceNet for connections

    Output options:
      -o <filename>, --file <filename>
                            Destination filename in Cloud Files or Openstack Swift
      -q                    Silence output
      -c, --cdn             Print CDN URL to stdout
```

## Examples

Each of these examples assume you have the environment variables `CLOUD_FILE_AUTHENTICAION_URL`, `CLOUD_FILES_USERNAME` and `CLOUD_FILES_APIKEY` exported. Alternatively, you can pass the username, auth_url and API key in as options with `-u`,`a` and `-k`, respectively.

### Upload a single file

`cfupload mycontainer ~/F4z2L.gif`

### Upload multiple files

`cfupload gifs ~/Pictures/*.gif`

### Upload from stdin

`tar cvzf - ~/important/* | cfupload -o backup-$(date '+%Y%m$d') backups`

## Pro Tips
* Export environment variables `CLOUD_FILES_{APIKEY,USERNAME,AUTHENTICAION_URL}` in your bash_profile to prevent the need to specify these options each time you run cfupload
* A destination filename must be provided with -o when uploading from standard input
* Pipe your files from standard input to make cronjob backups stupid easy:
`# mysqldump --all-databases | gzip -c | cfupload -o backup-$(date '+%Y%m%d').sql.gz container`
