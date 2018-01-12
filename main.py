import argparse,csv,logging,os,sys,time,threading

from parser import logger, formatter, start_making_requests

from server import runserver
from flask_server import app

parser = argparse.ArgumentParser()


def read_csv(file):
    with open(file,'r') as file_csv:
        csvData = csv.reader(file_csv,delimiter=',')
        urls = [url.strip() for row in csvData for url in list(map(str.strip,row)) if url != ""]
        return urls

def periodic_run(func,delay,*args,**kwargs):

    def inner():
        func(*args,**kwargs)
        threading.Timer(delay,inner).start()

    return inner


def main(args):
    try:
        urls = read_csv(args.file)
        with open(args.requirement,'r') as conf_file:
            requirement = conf_file.read().strip()

        periodic_run(start_making_requests,args.delay,urls,requirement)()
        if args.port:
            if args.flask:
                app.run(port=args.port)
            else:
                runserver(args.port)
        else:
            if args.flask:
                app.run()
            else:
                runserver(5000)
    except IOError as e:
        print("Error occured: {}".format(e.with_traceback))
    finally:
        sys.exit(1)


def p_float(val):
    try:
        f = float(val)
    except ValueError:
        raise argparse.ArgumentTypeError("delay should be positive float value" % val)
    if f <= 0:
        raise argparse.ArgumentTypeError("delay should be positive float value" % val)
    return f


if __name__ == '__main__':
    parser.add_argument("-f","--file",help="path to csv file with websites",type=str,required=True)
    parser.add_argument("-d","--delay",help="refresh delay for periodical requests (in seconds)",type=p_float,required=True)
    parser.add_argument("-l","--logfile",help="path to log file",type=str)
    parser.add_argument("-r","--requirement",help="config file with content requirement",type=str,required=True)
    parser.add_argument("-p","--port",help="port for http server",type=int)
    parser.add_argument("--flask",help="use flask as http server",action="store_true")
    if len(sys.argv) < 2:
        parser.print_help()
    args = parser.parse_args()
    if args.logfile:
        file_handler = logging.FileHandler(args.logfile)
    else:
        file_handler = logging.FileHandler('debug.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    main(args)
