# Simple Benchmark
A simple command line tool based on **Python** for benchmarking your Protocol (HTTP) server,
which supports multiple threads and simulate the HTTP requests and responses of the Web pages under test.
You can take it as a simplified version of the AB(Apache Benchmark)

## Basic Usage
```
 $ python ./test.py -n 100 -c 10 -s 10 -m post https://www.youtube.com/
```
```
Test starts at: Mon May 09 16:37:39 2016
Running 100 requests

Host Name: https://www.youtube.com
Server Software: Ytfe_Worker
Status Code: 200
Server Port: 443
[=================================================================>] 100%

--------------------Results--------------------
Request Method:                  POST
Concurrency Level:               10
Complete requests:               100
Failed requests:                 0
Total transferred:               39750.634 KB
Transfer Rate:                   1171.652 [KB/sec] received
Time per request:                3.393 [s](mean)
Time per request:                0.339 [s](mean, across all concurrent requests)
Requests per second:             2.948


Spend Time:                      33.927 [s]
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
  -k, --keep-alive     Use HTTP KeepAlive feature
  -n , --requests      Number of requests. Default is 1
  -c , --concurrency   Number of concurrency. Default is 1
  -H , --header        Add Arbitrary header line, eg. "Accept-Encoding: gzip"
                       Inserted after all normal header lines. (repeatable)
```
