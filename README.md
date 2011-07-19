<h1>Simple Cloud Files Uploader</h1>
<p>Python script to quickly upload a file to Rackspace Cloud Files. Originally developed to make one-liner uploads more manageable. Supports input via file arguments or standard input.</p>

<h3>Usage</h3>
	Usage: cfupload.py [options] <filename>

	Upload a file to Rackspace Cloud Files.

	Options:
	  -h, --help            show this help message and exit

	  Cloud Files Connection Information:
	    -k <api key>, --apikey=<api key>
				API key. Defaults to env[CLOUD_FILES_APIKEY]
	    -u <username>, --user=<username>
				Username. Defaults to env[CLOUD_FILES_USERNAME]
	    -c <container>, --container=<container>
				Container name. Defaults to env[CLOUD_FILES_CONTAINER]
	    -s, --snet          Use ServiceNet for connections

	  Output options:
	    -o <filename>, --file=<filename>
				Destination filename
	    -q                  Silence output
<h3>Pro Tips</h3>
* Export environment variables `CLOUD_FILES_{APIKEY,USERNAME,CONTAINER}` in your bash_profile to prevent the need to specify these options each time you run cfupload
* A destination filename must be provided with -o when uploading from standard input
* Pipe your files from standard input to make cronjob backups stupid easy:
	<p>`# mysqldump --all-databases | gzip -c | ./cfupload.py -u example -k 75cbad4d83e196fcdfc8618fd74720ae -c foo -o backup.sql.gz`</p>
