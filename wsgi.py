#!/usr/bin/env python3
import sys
import argparse

from api.run import app

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

    app.run(debug=args.debug)