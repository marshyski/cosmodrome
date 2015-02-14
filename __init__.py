#!/usr/bin/python

from OpenSSL import SSL
from flask import Flask, request, jsonify, make_response, abort
from flask_sslify import SSLify
import re, yaml, os.path

config = 'config.yaml'
yamldir = 'data/'
common = yamldir + 'common.yaml'

config_yaml = yaml.load(file('config.yaml', 'r'))
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file(config_yaml['key'])
context.use_certificate_file(config_yaml['cert'])

app = Flask(__name__, static_url_path = "")
sslify = SSLify(app, subdomains=True)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Unknown Endpoint, try '/metadata/common'"}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Unknown Environment, Missing YAML File"}), 400)

@app.route('/metadata/common', methods=["GET"])
def common_metadata():
    if os.path.isfile(common):
        return str(yaml.load(file(common, 'r'))).replace(',', ',\n').replace('{', ' ').replace('}', '\n')
    else:
        abort(400)

@app.route('/metadata/env', methods=["GET"])
def all_metadata():
    ipaddy = re.match(r'(\d+\.\d+)',request.remote_addr).groups()[0]
    yamlconfig = yamldir + ipaddy + '.yaml'
    if os.path.isfile(yamlconfig):
        return str(yaml.load(file(yamlconfig, 'r'))).replace(',', ',\n').replace('{', ' ').replace('}', '\n')
    else:
        abort(400)

@app.route('/metadata/<string:metadata>', methods=["GET"])
def get_metadata(metadata):
    ipaddy = re.match(r'(\d+\.\d+)',request.remote_addr).groups()[0]
    yamlconfig = yamldir + ipaddy + '.yaml'
    if os.path.isfile(yamlconfig) and metadata in open(yamlconfig).read():
        allmetadata = yaml.load(file(yamlconfig, 'r'))
        return(str(allmetadata[metadata]))
    if os.path.isfile(common) and metadata in open(common).read():
        allmetadata = yaml.load(file(common, 'r'))
        return(str(allmetadata[metadata]))
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = config_yaml['port'], debug = False, ssl_context=context)
