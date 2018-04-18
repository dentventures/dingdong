import argparse
import json
import datetime
import os
import sys
import requests
import smtplib
from email.mime.text import MIMEText
from twisted.internet import reactor


URL = os.environ.get('SLACK_DINGDONG', None)
# TODO(Brett): SHOULD probably just use environment variables for these as well as being able to be set via the script
INTERVAL = 60
FILEPATH = "domains.txt"


def slack(*msg):
    if not URL:
        print 'no slack url set in $SLACK_DINGDONG'
        return 

    message_data = json.dumps(dict(text=''.join(str(msg))))
    response = requests.post(str(URL),
                             headers=dict(content_type='application/json',),
                             data=message_data)

    if response.status_code < 200 or response.status_code > 400:
        print 'slack failed', response.text


# def alert(*msg):
#     message_data = json.dumps(dict(text=''.join(str(msg))))

#     s = smtplib.SMTP('localhost')
#     s.sendmail('dingdong', ['2085402546@vtext.com'], message_data)
#     s.quit()


def ding(interval_seconds=INTERVAL, domains_filepath=FILEPATH):
    '''
    reads the domains file and does a request to see if the server is up.
    '''

    print 'dingdong', interval_seconds, domains_filepath

    with open(domains_filepath, 'r') as file:
        print '-'*20
        print 'Reading domains file', domains_filepath

        for endpoint in file.readlines():

            endpoint  = endpoint.strip()
            response = requests.head(endpoint)

            if response.status_code < 200 or response.status_code > 400:
                response = requests.get(endpoint)
                print '\tDING DONG FAILED!', endpoint, response.status_code, response.text

                slack(endpoint, ' <', response.status_code, '> is down: ```\n', response.text[:min(1000, len(response.text))], '```')
            else:
                print '\tDomain is up:', endpoint


    reactor.callLater(interval_seconds,
                      ding,
                      interval_seconds,
                      domains_filepath)


def dong(interval_seconds=INTERVAL, domains_filepath=FILEPATH):
    reactor.callLater(interval_seconds, ding, interval_seconds, domains_filepath)
    reactor.run()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='start ding dong process against domains list')
    parser.add_argument('--interval', default=INTERVAL, help='interval to check domains list in seconds')
    parser.add_argument('--domains', default=FILEPATH, help='filepath to the list of domains to check')

    args         = parser.parse_args()
    interval     = int(args.interval)
    domains_path = args.domains

    dong(interval, domains_path)
