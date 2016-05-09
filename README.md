# Simple Benchmark
A simple command line tool based on **Python** for benchmarking your Protocol (HTTP) server,
which supports multiple threads and simulate the HTTP requests and responses of the Web pages under test.
You can take it as a simplified version of the AB(Apache Benchmark)

## Basic Usage
```
 $ python ./test.py -n 100 -c 10 -s 10 -m post https://www.youtube.com/
```
```
Test starts at: Mon May 09 20:15:01 2016

Host Name: https://www.youtube.com
Server IP: 2404:6800:4008:c02::11
Server Software: Ytfe_Worker
Status Code: 200
Server Port: 443

Running 100 requests

[=================================================================>] 100%

--------------------Results--------------------
Request Method:                  POST
Concurrency Level:               10
Complete requests:               100
Failed requests:                 0
Total transferred:               41220.686 KB
Transfer Rate:                   1884.116 [KB/sec] received
Time per request:                2.188 [s](mean)
Time per request:                0.219 [s](mean, across all concurrent requests)
Requests per second:             4.571

Spend Time:                      21.878 [s]
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
