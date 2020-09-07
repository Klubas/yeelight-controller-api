import os
from flask import render_template, make_response
from flask_restful import Resource


class Index(Resource):
    @staticmethod
    def get():
        headers = {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*'
        }

        html = os.path.join('index.html')
        return make_response(
            render_template(html), 200, headers)