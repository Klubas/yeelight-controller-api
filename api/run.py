#!/usr/bin/env python3
import os
import sys
import argparse
from flask import Flask
from flask_restful import Api

from api.views.Index import Index
from api.views.Bulbs import Bulbs
from api.views.Bulb import Bulb
from api.views.Power import Power
from api.views.Color import Color
from api.views.Authentication import Logon

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__, static_folder="static", template_folder="templates")

# configs
app.config['EXPLAIN_TEMPLATE_LOADING'] = False
app.config['BUNDLE_ERRORS'] = True

api = Api(app)

# add resources
api.add_resource(Index, '/api')
api.add_resource(Logon, '/api/logon')
api.add_resource(Bulbs, '/api/bulbs')
api.add_resource(Bulb,  '/api/bulb')
api.add_resource(Power, '/api/bulb/power')
api.add_resource(Color, '/api/bulb/color')

host = "0.0.0.0"
port = 5000


if __name__ == '__main__':

    try:

        parser = argparse.ArgumentParser(
            description="Yeelight Controller"
        )

        parser.add_argument(
            '--hostname'
            , metavar='hostname:port'
            , type=str
            , help="hostname and port number for the server in the format: <hostname>:<port>"
            , nargs="?"
        )

        parser.add_argument(
            '--debug'
            , help="Run in debug mode"
            , action='store_true'
        )

        args = parser.parse_args()
                
        if args.hostname:
            hostname = args.hostname.split(":")
            host = hostname[0]
            port = int(hostname[1])
        else:
            sys.exit(-1)

        debug = args.debug

        if os.getenv('YC_DEBUG'):
            debug = os.getenv('YC_DEBUG')

        app.run(host=host, port=port, debug=debug)

    except (KeyboardInterrupt, SystemExit):
        print("\nExiting...")


