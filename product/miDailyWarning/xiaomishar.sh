#!/bin/bash
sudo smbmount //10.237.2.61/'sharefiles'/ /home/will/xiaomishare/sharefiles -o 'username=lishuzu,password=xxxxxx,workgroup=OFFICENET'
sudo smbmount //10.237.2.61/'Users'/ /home/will/xiaomishare/Users -o 'username=lishuzu,password=xxxxx,workgroup=OFFICENET'
