#!/usr/bin/bash

# Install packages
yum -y update
yum install -y tree python3
yum install -y git


# Configure/install custom software
cd /home/ec2-user
git clone https://github.com/ToddRizley/python-image-gallery.git
chown -R ec2-user:ec2-user python-image-gallery
su ec2-user -c "cd ~/python-image-gallery && pip3 install -r requirements.txt --user"


# Start/enable services
systemctl stop postfix
systemctl disable postfix
