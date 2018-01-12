# Website monitor

A simple program that monitors websites and shows their availability. It uses `asyncio` and `threading` modules for sending asynchronous and periodical requests to websites, `HTTPServer` with custom HTTP handler based on `BaseHTTPRequestHandler` and Flask as HTTP web server (which one to use can be specified from command line).

### Requirements:
* Python 3 installed. (This program was tested on Python 3.5.2)

- Dependencies: beautifulsoup4, requests, Flask, Jinja2

- virtualenv and virtualenvwrapper (optional).

Dependencies  can be installed from `requirements.txt` using ` pip install -r requirements.txt` command in terminal.

### Description:

Program is capable of:

- Reading list of web pages (HTTP urls) from CSV format file and content requirement token from configuration file.

- Making periodic HTTP requests to websites

- Verifying if webpage contains required content requirement token.

- Measuring time (in seconds) taken to complete request.

- Writing progress of periodic requests to log file.

- Running single-page HTTP webserver. One based on [BaseHTTPRequestHandler and HTTPServer ](https://docs.python.org/3/library/http.server.html) and second is Flask server. By default first one is used but you can choose [Flask](http://flask.pocoo.org/) using `--flask` flag.

### Configuration and usage:

**Configuration (optional step):** if you have virtualenv or  virtualenvwrapper installed in order not to brake your system dependencies you can create virtual environment using this command:
	
	$ virtualenv monitor-env --python python3 
or by using virtualenvwrapper:

	$ mkvirtualenv monitor-env --python=python3 
	
Activate environment if you created it using virtualenv:
	
	$ source monitor-env/bin/activate
	
Activate if you created it by using virtualenvwrapper:

	$ workon monitor-env
	

**Usage:**

In order to start program  you need to execute `main.py` file:
	
	$ python main.py
	
If file is executed like this the quick help menu will show up:

	usage: main.py [-h] -f FILE -d DELAY [-l LOGFILE] -r REQUIREMENT [-p PORT]
               [--flask]

	optional arguments:
	  -h, --help            show this help message and exit
	  -f FILE, --file FILE  path to csv file with websites
	  -d DELAY, --delay DELAY
		                refresh delay for periodical requests (in seconds)
	  -l LOGFILE, --logfile LOGFILE
		                path to log file
	  -r REQUIREMENT, --requirement REQUIREMENT
		                config file with content requirement
	  -p PORT, --port PORT  port for http server
	  --flask               use flask as http server
	usage: main.py [-h] -f FILE -d DELAY [-l LOGFILE] -r REQUIREMENT [-p PORT]
		       [--flask]
	main.py: error: the following arguments are required: -f/--file, -d/--delay, -r/--requirement
 
 To run program correctly you need to specify `--file` parameter  followed by path to CSV file with urls, `--delay` parameter  followed floating point type number, `--requirement` which is path to configuraton file with phrase you want to check in your requests. 
 
	$ python main.py -f ./urls.csv -d 2 -r ./config.conf

 You can also specify port for your webserver (default is 5000) and name and path of log file (default path is current directory and default filename is `debug.log`). 
 
 	$ python main.py -f ./urls.csv -d 2 -r ./config.conf -p 8080 -l ./log.txt
 	
 You can also change default http server to Flask server:
 
 	$ python main.py -f ./urls.csv -d 2 -r ./config.conf -p 8080 --flask
 
 After running `main.py` you can type http:/127.0.0.1:{your port number}/  and check if everything is working.A simple program that monitors websites and shows their availability.

 
