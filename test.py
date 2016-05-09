#!/usr/bin/env python
# -*- coding: utf8 -*-
import pb
import sys
import time
import math
import urllib2
import argparse
import requests
import threading
from Queue import Queue
from time import sleep, ctime
from requests.packages.urllib3.util import parse_url
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

TEST_URL = 'https://www.baidu.com'
TIME_OUT = 30
REQUEST_NUM = 1  # 总请求次数
CONCURRENCY_NUM = 1  # 一次并发请求的次数，总的请求数(n)=次数*一次并发请求数(c)
FINISHED_NUM = 0  # 完成数
FAIL_NUM = 0  # 出错数
SUCCESS_NUM = 0  # 成功请求数
FILE_SIZE = 0
MY_DATA = None
MY_MEHTOD = 'GET'

MY_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit\
            /537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
            */*;q=0.8',
    'Accept-Encoding': 'gzip',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4'
}


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        apply(self.func, self.args)


def request_URL(url):
    global CONCURRENCY_NUM
    global TIME_OUT
    global TEST_URL
    global FINISHED_NUM
    global FAIL_NUM
    global SUCCESS_NUM
    global FILE_SIZE
    global MY_HEADERS
    global MY_DATA
    global METHOD

    for _ in xrange(CONCURRENCY_NUM):
        try:
            req = urllib2.Request(url, headers=MY_HEADERS)
            response = urllib2.urlopen(req, timeout=TIME_OUT, data=MY_DATA)
            html = response.read()
            SUCCESS_NUM += 1
            FILE_SIZE += len(html)
        except urllib2.HTTPError as e:
            print(e.reason)
            FAIL_NUM += 1
        except urllib2.URLError as e:
            print(e.reason)
            FAIL_NUM += 1
        FINISHED_NUM += 1


def progress_bar(p):
    global FINISHED_NUM
    global REQUEST_NUM
    while FINISHED_NUM < REQUEST_NUM:
        p.progress = int((FINISHED_NUM * 100 / REQUEST_NUM))
        p.show_progress()
    if FINISHED_NUM == REQUEST_NUM:
        p.progress = 100
        p.show_progress()


def handler(signum, frame):
    global is_exit
    is_exit = True
    print "receive a signal %d, is_exit = %d" % (signum, is_exit)


def test_start():
    threads = []
    global REQUEST_NUM
    global CONCURRENCY_NUM
    global TEST_URL
    if CONCURRENCY_NUM >= REQUEST_NUM:
        loop_num = 1
    else:
        loop_num = int(math.ceil(float(REQUEST_NUM) / float(CONCURRENCY_NUM)))

    for i in xrange(loop_num):
        if i < loop_num - 1:
            concurrency = CONCURRENCY_NUM
        else:
            concurrency = REQUEST_NUM % CONCURRENCY_NUM
        t = MyThread(
            request_URL, (TEST_URL,), request_URL.__name__)
        threads.append(t)

    p = pb.AnimatedProgressBar(end=100, width=65)
    t = MyThread(
        progress_bar, (p,), progress_bar.__name__)
    threads.append(t)

    for t in threads:
        t.setDaemon(True)
        t.start()

    for t in threads:
        t.join()


def get_server_info(method='GET'):
    global TEST_URL
    try:
        res = requests.get(TEST_URL)
        parts = parse_url(TEST_URL)
        if not parts.port and parts.scheme == 'https':
            port = 443
        elif not parts.port and parts.scheme == 'http':
            port = 80
        else:
            port = parts.port
        print(
            'Server Software: %s' %
            res.headers.get('server'))
        # print(res.headers)
        if str(res.history) == '[]':
            res.history = ''
        print('Status Code: %s %s' % (res.status_code, res.history))
        print('Server Port: %s' % port)
    except requests.exceptions.ConnectionError as e:
        pass


def main():
    global sys
    global CONCURRENCY_NUM
    global TEST_URL
    global REQUEST_NUM
    global FINISHED_NUM
    global FAIL_NUM
    global SUCCESS_NUM
    global FILE_SIZE
    global MY_DATA
    global MY_MEHTOD
    global MY_HEADERS

    _VERBS = ('GET', 'POST', 'DELETE', 'PUT', 'HEAD', 'OPTIONS',
              'get', 'post', 'delete', 'put', 'head', 'options')
    _DATA_VERBS = ('POST', 'PUT', 'post', 'put')

    parser = argparse.ArgumentParser(
        description='Simple Benchmark.')
    parser.usage = '[options] [http[s]://]hostname[:port]/path'
    parser.add_argument(
        '-v', '--version', action='store_true', default=False,
        help='Displays version and exits.')

    parser.add_argument('-m', '--method', help='HTTP Method',
                        type=str, default='GET', choices=_VERBS)

    parser.add_argument('--content-type', help='Content-Type',
                        type=str, default='text/plain')

    parser.add_argument('-s', '--timeout',
                        help=('Seconds to max. wait for each response'
                              'Default is 30 seconds'), type=str)

    parser.add_argument('-D', '--data',
                        help=('Data. Prefixed by "py:" to point '
                              'a python callable.'), type=str)

    parser.add_argument('-n', '--requests',
                        help='Number of requests', type=int)

    parser.add_argument('-c', '--concurrency', help='Concurrency',
                        type=int, default=1)

    parser.add_argument('-H', '--header', help=' Add Arbitrary header line,'
                        ' eg. "Accept-Encoding: gzip"'
                        'Inserted after all normal header lines. (repeatable)',
                        type=str, action='append')

    parser.add_argument('url', help='URL to benchmark', nargs='?')
    args = parser.parse_args()

    def _split(header):
        # split the header
        header = header.split(':')
        if len(header) != 2:
            print("A header must be of the form name:value")
            parser.print_usage()
            sys.exit(0)
        return header

    if args.version:
        print('v0.1')
        sys.exit(0)

    if args.url is None:
        print('You need to provide an URL.')
        parser.print_usage()
        sys.exit(0)
    else:
        TEST_URL = args.url

    if args.data is not None and args.method not in _DATA_VERBS:
        print("You can't provide data with %r" % args.method)
        parser.print_usage()
        sys.exit(0)
    else:
        MY_DATA = args.data
        MY_MEHTOD = args.method

    if args.requests is None:
        args.requests = 1
    else:
        REQUEST_NUM = args.requests

    if args.concurrency is None:
        args.concurrency = 1
    else:
        CONCURRENCY_NUM = args.concurrency

    if args.header is None:
        MY_HEADERS = {}
    else:
        MY_HEADERS = dict([_split(header) for header in args.header])

    print('Test starts at: %s' % (ctime()))
    print('Running %s requests\n' % (REQUEST_NUM))
    print('Host Name: %s' % (TEST_URL))
    StartTime = time.time()
    get_server_info()
    try:
        test_start()
    except KeyboardInterrupt:
        import sys
        sys.exit()
    finally:
        EndTime = time.time()
        SpendTime = EndTime - StartTime
    print('\n')
    print('--------------------Results--------------------')
    print('Request Method: \t\t %s' % MY_MEHTOD.upper())
    if MY_HEADERS != {}:
        print('Request Headers: \t\t %s' % MY_HEADERS)
    print('Complete requests: \t\t %s' % SUCCESS_NUM)
    print('Concurrency Level: \t\t %s' % CONCURRENCY_NUM)
    print('Failed requests: \t\t %s' % FAIL_NUM)
    print('Transfer Rate: \t\t\t %.3f [KB/sec] received' %
          (FILE_SIZE / 1024 / SpendTime))
    print('Time per request: \t\t %.3f [s](mean)' %
          (CONCURRENCY_NUM * SpendTime/REQUEST_NUM))
    print('Time per request: \t\t %.3f [s](mean, across all'
          'concurrent requests)' % (SpendTime / REQUEST_NUM))

    print('Requests per second: \t\t %.3f' % (REQUEST_NUM / SpendTime))
    print('\n')
    print('Spend Time: \t\t\t %.3f [s]' % (SpendTime))

if __name__ == "__main__":
    main()