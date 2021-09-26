# IP Database

Create IP database which is stored in a SQLite3 database.

## Performance benchmark

Run `pyinstrument <python-script.py>`

For example, this is result for `check_geoip2.py`

```bash

  _     ._   __/__   _ _  _  _ _/_   Recorded: 20:23:02  Samples:  29
 /_//_/// /_\ / //_// / //_'/ //     Duration: 0.042     CPU time: 0.021
/   _/                      v4.0.3

Program: check_geoip2.py

0.041 <module>  <string>:1
   [4 frames hidden]  <string>, runpy
      0.041 _run_code  runpy.py:64
      └─ 0.041 <module>  check_geoip2.py:1
         ├─ 0.014 <module>  utils.py:1
         │  ├─ 0.012 <module>  geoip2/database.py:1
         │  │     [33 frames hidden]  geoip2, maxminddb, multiprocessing, s...
         │  ├─ 0.001 loads  <built-in>:0
         │  │     [2 frames hidden]  <built-in>
         │  └─ 0.001 <module>  ipaddress.py:4
         │        [7 frames hidden]  ipaddress, <built-in>
         ├─ 0.013 get_city  utils.py:10
         │  ├─ 0.009 city  geoip2/database.py:133
         │  │     [18 frames hidden]  geoip2, maxminddb
         │  └─ 0.004 __init__  geoip2/database.py:62
         │        [7 frames hidden]  geoip2, maxminddb, <built-in>
         ├─ 0.013 get_isp  utils.py:23
         │  ├─ 0.007 isp  geoip2/database.py:211
         │  │     [18 frames hidden]  geoip2, maxminddb
         │  └─ 0.006 __init__  geoip2/database.py:62
         │        [5 frames hidden]  geoip2, maxminddb, <built-in>
         └─ 0.001 BufferedReader.read  <built-in>:0
               [2 frames hidden]  <built-in>
```