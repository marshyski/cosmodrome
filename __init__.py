#!/usr/bin/env python

from OpenSSL import SSL
from flask import Flask, request, jsonify, make_response, abort
from flask_limiter import Limiter
import re
import yaml
import os.path
import glob
import difflib

config = 'config.yaml'
yamldir = 'data/'
common = yamldir + 'common.yaml'

config_yaml = yaml.load(file('config.yaml', 'r'))
if config_yaml['key']:
   from flask_sslify import SSLify
   context = SSL.Context(SSL.SSLv23_METHOD)
   context.use_privatekey_file(config_yaml['key'])
   context.use_certificate_file(config_yaml['cert'])
   app = Flask(__name__, static_url_path = "")
   sslify = SSLify(app, subdomains=True)
else:
   app = Flask(__name__, static_url_path = "")

print config_yaml['request_limit']

if config_yaml['request_limit']:
    request_limit = config_yaml['request_limit']
else:
    request_limit = '7200 per hour'

limiter = Limiter(app, global_limits=[request_limit])

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Unknown Endpoint, try '/metadata/common'"}), 404)

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({"error": "Unknown Environment, Missing YAML File"}), 400)

@app.route('/', methods = ['GET'])
def api_doc():
    """API Endpoint Reference"""
    func_list = {}
    for rule in app.url_map.iter_rules():
        if rule.endpoint != 'static':
            func_list[rule.rule] = app.view_functions[rule.endpoint].__doc__
    return jsonify(func_list)

@app.route('/metadata/common', methods=['GET'])
def common_metadata():
    """Common Data for All Environments Defined"""
    if os.path.isfile(common):
        return str(yaml.load(file(common, 'r'))).replace(',', ',\n').replace('{', ' ').replace('}', '\n')
    else:
        abort(400)

@app.route('/metadata/env', methods=['GET'])
def all_metadata():
    """All Environment Data Defined by Incoming Request"""
    twoocts = re.match(r'(\d+\.\d+)',request.remote_addr).groups()[0]
    threeocts = re.match(r'(\d+\.\d+\.\d+)',request.remote_addr).groups()[0]
    yamlconfig = yamldir + threeocts + '.yaml'
    if os.path.isfile(yamlconfig):
       ipaddy = threeocts
    else:
       ipaddy = twoocts
    yamlconfig = yamldir + ipaddy + '.yaml'
    if os.path.isfile(yamlconfig):
        return str(yaml.load(file(yamlconfig, 'r'))).replace(',', ',\n').replace('{', ' ').replace('}', '\n')
    else:
        abort(400)

@app.route('/metadata/<string:metadata>', methods=['GET'])
def get_metadata(metadata):
    """Requested Value Data by Defined Environment or Host"""
    yamlfiles = glob.glob(yamldir + '*.yaml')
    yamlconfig = yamldir + metadata + '.yaml'
    if not os.path.isfile(yamlconfig):
       twoocts = re.match(r'(\d+\.\d+)',request.remote_addr).groups()[0]
       threeocts = re.match(r'(\d+\.\d+\.\d+)',request.remote_addr).groups()[0]
       yamlconfig = yamldir + threeocts + '.yaml'
       if os.path.isfile(yamlconfig):
          ipaddy = threeocts
       else:
          ipaddy = twoocts
       yamlconfig = yamldir + ipaddy + '.yaml'
    if os.path.isfile(yamlconfig) and metadata in open(yamlconfig).read():
        allmetadata = yaml.load(file(yamlconfig, 'r'))
        return(str(allmetadata[metadata]))
    if os.path.isfile(common) and metadata in open(common).read():
        allmetadata = yaml.load(file(common, 'r'))
        return(str(allmetadata[metadata]))
    if os.path.isfile(yamlconfig):
        return str(yaml.load(file(yamlconfig, 'r'))).replace(',', ',\n').replace('{', ' ').replace('}', '\n')
    newyamlconfig = sorted(yamlfiles, key=lambda x: difflib.SequenceMatcher(None, x, yamldir + metadata).ratio(), reverse=True)[0]
    if newyamlconfig:
        return str(yaml.load(file(newyamlconfig, 'r'))).replace(',', ',\n').replace('{', ' ').replace('}', '\n')
    abort(404)

@app.route('/metadata/<string:host>/<string:metadata>', methods=['GET'])
def host_metadata(host, metadata):
    """Requested Value Data by Host"""
    yamlfiles = glob.glob(yamldir + '*.yaml')
    yamlconfig = yamldir + host + '.yaml'
    if os.path.isfile(yamlconfig) and metadata in open(yamlconfig).read():
       allmetadata = yaml.load(file(yamlconfig, 'r'))
       return(str(allmetadata[metadata]))
    newyamlconfig = sorted(yamlfiles, key=lambda x: difflib.SequenceMatcher(None, x, yamldir + host).ratio(), reverse=True)[0]
    if newyamlconfig and metadata in open(newyamlconfig).read():
       allmetadata = yaml.load(file(newyamlconfig, 'r'))
       return(str(allmetadata[metadata]))
    abort(404)

if __name__ == '__main__':
    if config_yaml['key'] and config_yaml['host']:
    	app.run(host = config_yaml['host'], port = config_yaml['port'], debug = False, ssl_context=context)

    if config_yaml['host']:
        app.run(host = config_yaml['host'], port = config_yaml['port'], debug = False)

    app.run(host = "127.0.0.1", port = config_yaml['port'], debug = False)
