import json
import boto3
import time
import flask
from flask import Flask, request, jsonify
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return '''<h1>A sample test example</h1>
<p>1. Launch EC2 Instance </p>
<p>2. Check status of machine </p>'''
    
    
@app.route('/create_machine', methods=["GET"])
def launch_machine():
    ec2 = boto3.client('ec2')  
    launch_instance = ec2.run_instances(
        ImageId = "ami-087c17d1fe0178315",
        InstanceType = 't1.micro',
        MaxCount = 1,
        MinCount = 1,
        Monitoring = {
           'Enabled': False
        }
    )
    print(launch_instance)
    machine_id = launch_instance['Instances'][0]['InstanceId']
    return machine_id
   ## time.sleep(10)  Not Required

@app.route('/machine_status', methods=["GET"])
def machine_status():
    ec2 = boto3.client('ec2')   
    if 'machine_id' in request.args:
       machine_id = str(request.args['machine_id'])
    else:
        return "Error: No machine provided. Please specify an machine id."
    describe_instance= ec2.describe_instances(
         InstanceIds=[machine_id] 
    )
    instance_status= describe_instance['Reservations'][0]['Instances'][0]['State']['Name']
    print(instance_status)
    return instance_status
app.run()

