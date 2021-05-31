#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from api.run import app

load_dotenv()

if __name__ == "__main__":
    host = os.getenv('YC_HOSTNAME') if os.getenv('YC_HOSTNAME') else '0.0.0.0'
    port = os.getenv('YC_PORT') if os.getenv('YC_PORT') else '5000'
    debug = True if os.getenv('YC_DEBUG') == 'True' else False
    app.run(host=host, port=port, debug=debug)
