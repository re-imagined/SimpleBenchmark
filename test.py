#!/usr/bin/env python
# -*- coding: utf8 -*-
import pb
import sys
import time
import math
import urllib
import urllib2
import argparse
import requests
import threading
from Queue import Queue
from time import sleep, ctime
from requests.packages.urllib3.util import parse_url
from requests.packages.urllib3.connectionpool import HTTPConnectionPool
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse

TEST_URL = 'https://www.zhihu.com'
TIME_OUT = 30
REQUEST_NUM = 1  # 总请求次数
CONCURRENCY_NUM = 1  # 一次并发请求的次数，总的请求数(n)=次数*一次并发请求数(c)
FINISHED_NUM = 0  # 完成数
FAIL_NUM = 0  # 出错数
SUCCESS_NUM = 0  # 成功请求数
FILE_SIZE = 0
MY_MEHTOD = 'GET'  # 默认使用 GET 方法
MY_HEADERS = {}


class MyThread(threading.Thread):
    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        apply(self.func, self.args)


def request_URL(url, concurrency):
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

    for _ in xrange(concurrency):
        try:
            req = urllib2.Request(url, headers=MY_HEADERS)
            response = urllib2.urlopen(req, timeout=TIME_OUT)
            html = response.read()
            SUCCESS_NUM += 1
            FILE_SIZE += len(html)
        except urllib2.HTTPError as e:
            # print(e.reason)
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
            if REQUEST_NUM % CONCURRENCY_NUM == 0:
                concurrency = CONCURRENCY_NUM
            else:
                concurrency = REQUEST_NUM % CONCURRENCY_NUM
        t = MyThread(
            request_URL, (TEST_URL, concurrency), request_URL.__name__)
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

    def _make_request(self, conn, method, url, **kwargs):
        response = self._old_make_request(conn, method, url, **kwargs)
        sock = getattr(conn, 'sock', False)
        if sock:
            setattr(response, 'peer', sock.getpeername())
        else:
            setattr(response, 'peer', None)
        return response

    HTTPConnectionPool._old_make_request = HTTPConnectionPool._make_request
    HTTPConnectionPool._make_request = _make_request

    try:
        res = requests.get(TEST_URL)
        print('Server IP: %s' % res.raw._original_response.peer[0])
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

    parser = argparse.ArgumentParser(
        description='Simple Benchmark.')
    parser.usage = '[options] [http[s]://]hostname[:port]/path'
    parser.add_argument(
        '-v', '--version', action='store_true', default=False,
        help='Displays version and exits.')

    parser.add_argument('-m', '--method', help='HTTP Method', metavar='',
                        type=str, default='GET', choices=_VERBS)

    parser.add_argument('-s', '--timeout', metavar='',
                        help=('Timeout for each response '
                              'Default is 30 seconds'), type=str)

    parser.add_argument('-k', '--keep-alive', action="store_true",
                        default=False, help='Use HTTP KeepAlive feature')

    parser.add_argument('-n', '--requests', metavar='',
                        help='Number of requests. Default is 1', type=int)

    parser.add_argument('-c', '--concurrency', help='Number of concurrency.'
                        ' Default is 1', metavar='', type=int, default=1)

    parser.add_argument('-H', '--header', help=' Add Arbitrary header line,'
                        ' eg. "Accept-Encoding: gzip" '
                        'Inserted after all normal header lines. (repeatable)',
                        type=str, action='append', metavar='')

    parser.add_argument('url', help='URL to benchmark', nargs='?')
    args = parser.parse_args()

    def _split(header_or_data):
        # split the header or data
        header_or_data = header_or_data.split(':')
        if len(header_or_data) != 2:
            print("A header or data must be of the form name:value")
            parser.print_usage()
            sys.exit(0)
        return header_or_data

    if args.version:
        print('v0.1')
        sys.exit(0)

    if args.url is None:
        print('You need to provide an URL.')
        parser.print_usage()
        sys.exit(0)
    else:
        TEST_URL = args.url

    if args.method not in _VERBS:
        print("You can't provide data with %r" % args.method)
        parser.print_usage()
        sys.exit(0)
    else:
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

    if args.keep_alive is True:
        MY_HEADERS['Connection'] = 'keep-alive'
    else:
        MY_HEADERS['Connection'] = 'close'

    print('')
    print('Test starts at: %s' % (ctime()))
    print('')
    print('Host Name: %s' % (TEST_URL))

    StartTime = time.time()
    get_server_info()

    print('')
    print('Running %s requests\n' % (REQUEST_NUM))

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
    print('Concurrency Level: \t\t %s' % CONCURRENCY_NUM)
    print('Complete requests: \t\t %s' % SUCCESS_NUM)
    print('Failed requests: \t\t %s' % FAIL_NUM)
    print('Total transferred: \t\t %.3f KB' % (float(FILE_SIZE) / 1024))
    print('Transfer Rate: \t\t\t %.3f [KB/sec] received' %
          (float(FILE_SIZE) / 1024 / SpendTime))
    print('Time per request: \t\t %.3f [s](mean)' %
          (CONCURRENCY_NUM * SpendTime/REQUEST_NUM))
    print('Time per request: \t\t %.3f [s](mean, across all '
          'concurrent requests)' % (SpendTime / REQUEST_NUM))
    print('Requests per second: \t\t %.3f' % (REQUEST_NUM / SpendTime))
    print('')
    print('Spend Time: \t\t\t %.3f [s]' % (SpendTime))

if __name__ == "__main__":
    main()
