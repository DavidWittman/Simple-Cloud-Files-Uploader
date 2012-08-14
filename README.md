# Simple Cloud Files Uploader
Python script to quickly upload files to Rackspace Cloud Files. Originally developed to make one-liner uploads more manageable. Supports input via file arguments or standard input.

## Usage

```
usage: cfupload.py [-h] [-k <api key>] [-u <username>] [-s] [-o <filename>]
                   [-q]
                   container [files [files ...]]

Upload files to Rackspace Cloud Files

positional arguments:
  container             Cloud Files container name
  files                 The file(s) to upload

optional arguments:
  -h, --help            show this help message and exit

Cloud Files Connection Information:
  -k <api key>, --apikey <api key>
                        API key. Defaults to env[CLOUD_FILES_APIKEY]
  -u <username>, --user <username>
                        Username. Defaults to env[CLOUD_FILES_USERNAME]
  -s, --snet            Use ServiceNet for connections

Output options:
  -o <filename>, --file <filename>
                        Destination filename in Cloud Files
  -q                    Silence output
```

## Examples

Each of these examples assume you have the environment variables `CLOUD_FILES_USERNAME` and `CLOUD_FILES_APIKEY` exported. Alternatively, you can pass the username and API key in as options with `-u` and `-k`, respectively.

### Upload a single file

`cfupload.py mycontainer ~/F4z2L.gif`

### Upload multiple files

`cfupload.py gifs ~/Pictures/*.gif`

### Upload from stdin

`tar cvzf - ~/important/* | cfupload.py -o backup-$(date '+%Y%m$d') backups`

## Pro Tips
* Export environment variables `CLOUD_FILES_{APIKEY,USERNAME}` in your bash_profile to prevent the need to specify these options each time you run cfupload
* A destination filename must be provided with -o when uploading from standard input
* Pipe your files from standard input to make cronjob backups stupid easy:
`# mysqldump --all-databases | gzip -c | cfupload.py -o backup-$(date '+%Y%m%d').sql.gz container`
