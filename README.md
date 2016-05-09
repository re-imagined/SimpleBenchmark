# Simple Benchmark
A simple command line tool based on **Python** for benchmarking your Protocol (HTTP) server,
which supports multiple threads and simulate the HTTP requests and responses of the Web pages under test.
You can take it as a simplified version of the AB(Apache Benchmark)

## Basic Usage
> $ python ./test.py -n 100 -c 10 -m POST http://stackoverflow.com/

```
Test starts at: Mon May 09 13:14:34 2016
Running 100 requests

Host Name: http://stackoverflow.com
Server Software: cloudflare-nginx
Status Code: 200
Server Port: 80
[=================================================================>] 100%

--------------------Results--------------------
Request Method:                  POST
Concurrency Level:               10
Complete requests:               0
Failed requests:                 100
Transfer Rate:                   0.000 [KB/sec] received
Time per request:                0.838 [s](mean)
Time per request:                0.084 [s](mean, across allconcurrent requests)
Requests per second:             11.926


Spend Time:                      8.385 [s]
```
#### Options
> python ./test.py -h

```
usage: [options] [http[s]://]hostname[:port]/path

Simple Benchmark.

positional arguments:
  url                  URL to benchmark

optional arguments:
  -h, --help           show this help message and exit
  -v, --version        Displays version and exits.
  -m , --method        HTTP Method
  -s , --timeout       Timeout for each response Default is 30 seconds
  -D , --data          Data. Prefixed by "py:" to point a python callable.
  -n , --requests      Number of requests
  -c , --concurrency   Concurrency
  -H , --header        Add Arbitrary header line, eg. "Accept-Encoding:
                       gzip"Inserted after all normal header lines.
                       (repeatable)
```
