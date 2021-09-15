#!/bin/env python
from ansible.module_utils.basic import *
import os, json
import re, sys
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
      file = open("/tmp/userdata.txt","w")
      file.write("machine_id: "+machine_id +" status is running")
      module.exit_json(changed = True,success = data,msg = data)
  except Exception as e:
       module.fail_json(msg = "OOOps ")

if __name__== "__main__":
  main()
