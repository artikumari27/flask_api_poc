#!/bin/env python
from ansible.module_utils.basic import *
import os, json
import re, sys
import json
import boto3
import flask
from flask import Flask, request, jsonify
def main():
  module = AnsibleModule(
        argument_spec = dict(
              machine_id = dict(required = True,type = 'str'),
         )
  )
  machine_id = module.params['machine_id']
  data = dict(
          output = "machine status",)
  try:
     app = flask.Flask(__name__)
     app.config["DEBUG"] = True
     # machine_id = sys.argv[0]
     @app.route('/', methods=['GET'])
     def home():
       return '''<h1>A sample test example</h1>
       <p>1. Launch EC2 Instance </p>
       <p>2. Check status of machine </p>'''

    @app.route('/machine_status', methods=["GET"])
    def machine_status():
      ec2 = boto3.client('ec2')
      if 'machine_id' in request.args:
         machine_id = str(request.args['machine_id'])
      else:
         return "Error: No machine provided. Please specify an machine id."
      describe_instance= ec2.describe_instances(
         InstanceIds=[machine_id])
      instance_status= describe_instance['Reservations'][0]['Instances'][0]['State']['Name']
      # print(instance_status)
      return instance_status
    app.run()
    file = open("/tmp/machine_status.txt","w")
    file.write("Status of machine_id: "+machine_id +"is "+ instance_status)
    module.exit_json(changed = True,success = instance_status,msg = instance_status)
  except Exception as e:
       module.fail_json(msg = "OOOps ")

if __name__== "__main__":
  main()
