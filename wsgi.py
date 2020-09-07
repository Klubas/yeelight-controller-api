#!/usr/bin/env python3
import os
import argparse
from dotenv import load_dotenv

from api.run import app

load_dotenv()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description="WSGI"
    )

    parser.add_argument(
            '--debug'
            , help="Run in debug mode"
            , action='store_true'
    )

    args = parser.parse_args()

    debug = args.debug

    if os.getenv('YC_DEBUG'):
        debug = os.getenv('YC_DEBUG')

    app.run(debug=debug)
