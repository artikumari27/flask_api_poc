#!/bin/env python
from ansible.module_utils.basic import *
import os, json
import re, sys
import json
import boto3
import flask
import subprocess
#from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def main():
  module = AnsibleModule(
        argument_spec = dict(
              machine_id = dict(required = True,type = 'str'),
         )
  )
  machine_id = module.params['machine_id']
  #data = dict(
  #    output = "machine status",)
  #try:

  app.run()
  output = subprocess.getoutput("curl http://127.0.0.1/5000/machine_status?machine_id=machine_id")
  data = dict(
      output = output,)

    #file = open("/tmp/machine_status.txt","w")
   # file.write("Status of machine_id: "+machine_id +"is "+instance_status)
  module.exit_json(changed = True,success = data,msg = data)
 # except Exception as e:
  #     module.fail_json(msg = "OOOps ")

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
  
if __name__== "__main__":
  main()
