#!/usr/bin/env python3
import os
import sys
import argparse
from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from dotenv import load_dotenv

from api.views.Index import Index
from api.views.LightBulbs import LightBulbs
from api.views.LightBulb import LightBulb
from api.views.Power import Power
from api.views.Color import Color
from api.views.Authentication import Logon

# configs
load_dotenv()
app = Flask(__name__)

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['EXPLAIN_TEMPLATE_LOADING'] = os.getenv('YC_EXPLAIN_TEMPLATE_LOADING')
app.config['BUNDLE_ERRORS'] = not os.getenv('YC_DISABLE_ERROR_BUNDLE')

# add resources
api = Api(app)
api.add_resource(Index, '/api')
api.add_resource(Logon, '/api/logon')
api.add_resource(LightBulbs, '/api/bulbs')
api.add_resource(LightBulb, '/api/bulb')
api.add_resource(Power, '/api/bulb/power')
api.add_resource(Color, '/api/bulb/color')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


host = "localhost"
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


