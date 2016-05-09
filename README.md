# Simple Benchmark
A simple command line tool based on **Python** for benchmarking your Protocol (HTTP) server,
which supports multiple threads and simulate the HTTP requests and responses of the Web pages under test.
You can take it as a simplified version of the AB(Apache Benchmark)

## Basic Usage
```
 $ python ./test.py -n 100 -c 10 -s 10 -m post http://www.gamersky.com/
```
```
Test starts at: Mon May 09 16:26:38 2016
Running 100 requests

Host Name: http://www.gamersky.com/
Server Software: Microsoft-IIS/7.5
Status Code: 200
Server Port: 80
[=================================================================>] 100%

--------------------Results--------------------
Request Method:                  POST
Concurrency Level:               10
Complete requests:               100
Failed requests:                 0
Total transferred:               41791.699 KB
Transfer Rate:                   3817.988 [KB/sec] received
Time per request:                1.095 [s](mean)
Time per request:                0.109 [s](mean, across all concurrent requests)
Requests per second:             9.136


Spend Time:                      10.946 [s]
```

#### Options
```
$ python ./test.py -h
```

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
