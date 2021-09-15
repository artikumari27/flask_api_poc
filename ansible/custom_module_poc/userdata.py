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
#      file = open("/tmp/userdata.txt","w")
#      file.write("machine_id: "+machine_id +" status is running")
     ec2 = boto3.client('ec2')
     describe_instance= ec2.describe_instances(
             InstanceIds=[machine_id])
     instance_status= describe_instance['Reservations'][0]['Instances'][0]['State']['Name']
     file = open("/tmp/machine_status.txt","w")
     file.write("Status of machine_id: "+machine_id +"is "+ instance_status)
     module.exit_json(changed = True,success = instance_status,msg = instance_status)
  except Exception as e:
       module.fail_json(msg = "OOOps ")

if __name__== "__main__":
  main()
