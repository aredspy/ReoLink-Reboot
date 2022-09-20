# ReoLink IP Camera Unauthenticated Reboot Tester

A Python script that tests if a ReoLink IP camera is vulnerable to a broken API request that will 
cause the camera to reboot without authentication leading to a Denial of Service (DoS) condition.

## Usage

Download `script.py` and execute with `python` or `python3`

```bash
$ python script.py    
Script to test API reboot against a Reolink IP camera device

Usage: python test.py IP_ADDRESS
```

## Associated CVEs

- CVE-2021-40404
- TALOS-2021-1421 (CVE-2021-40405)
