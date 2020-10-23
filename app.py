#!/usr/bin/env python3

from flask import Flask, request, Response, jsonify, json

import logging

import pagelist.ia_source as IAS

app = Flask(__name__)


@app.route('/')
def home():
    return Response(
        """<h2>Inductiveload Tools</h2>""",
        content_type='text/html')


@app.route('/pagelist/v1/list', methods=['GET'])
def pagelist():

    if 'source' not in request.args:
        return jsonify({'error': 'No source field'})

    if 'id' not in request.args:
        return jsonify({'error': 'No id field'})

    if request.args['source'] == 'ia':
        source = IAS.IaSource(request.args['id'])
    else:
        return jsonify({'error': 'Unknown source: {}'.format(request.args['source'])})

    try:
        pl = source.get_pagelist()
    except Exception as e:
        print(e)
        return jsonify({'error': 'Failed to get pagelist from source'})

    # logging.error(pl.to_pagelist_tag())
    response = jsonify({
            'source': request.args['source'],
            'id': request.args['id'],
            'pagelist': pl.to_pagelist_tag()
        })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response

if __name__ == '__main__':
    app.run()
