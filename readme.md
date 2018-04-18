# DING DONG

This is a simple python script to ping endpoints and make sure they return something in the 200 range. Both the ping interval and endpoints path can be specified using arguments.

### howto

Slack intergration works right now and uses a webhook. You will need to put the target slack webhook URL in an environment variable named "SLACK_DINGDONG". The script will automatically pull that environment variable in.

```
virtualenv venv
. venv/bin/acitvate

pip install -r requirements.txt

... edit the domains.txt with any endpoints you want to ping ...

python dingdong.py

```

### notes

* Everything here is subject to change and an ongoing project. 

* The included service file is for systemd and an example using a base ubuntu (16.04) setup from amazon.