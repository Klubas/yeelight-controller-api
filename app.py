#!/usr/bin/env python3
import sys
import argparse

from flask import Flask
from flask_restful import Api
from app.LightAPI import Index, Bulb

if __name__ == '__main__':

    app = Flask(__name__, static_folder="static", template_folder="templates")
    api = Api(app)

    # add resources
    api.add_resource(Index, '/')
    api.add_resource(Bulb, '/light/bulb')

    try:

        parser = argparse.ArgumentParser(
            description="Yeelight Controller"
        )

        parser.add_argument(
            '--hostname'
            , metavar='hostname:port'
            , type=str
            , help="hostname and port number for the server in the format: <hostname>:<port>"
        )

        parser.add_argument(
            '--debug'
            , help="Run in debug mode"
            , action='store_true'
        )

        args = parser.parse_args()
        
        print(args)
        
        if args.hostname:
            hostname = args.hostname.split(":")
            host = hostname[0]
            port = int(hostname[1])
        else:
            sys.exit(-1)

        app.config['EXPLAIN_TEMPLATE_LOADING'] = True
        
        app.run(host=host, port=port, debug=args.debug)

    except (KeyboardInterrupt, SystemExit):
        print("\nExiting...")

else:
    sys.exit()
