from influxdb import InfluxDBClient
import pyping
import time
import sys
import datetime


def spinning_wheel():
    wheel = '|/-\\'
    while True:
        for cursor in wheel:
            yield cursor

def latency_metrics(host):

    r = pyping.ping(host['ip'])
    return [
        {
            "measurement": "icmp_latency_{}".format(latency_value),
            "tags": {
                'host': host['hostname']
            },
            "time": time.strftime ("%Y-%m-%d %H:%M:%S"), 
            "fields": {
                'Float_value': getattr(r, latency_value)
            }

        } for latency_value in ['max_rtt']
    ]

def main(host, db_conn):

    try:

        
        # executes once per second
        execution_count = 0

        spinner = spinning_wheel()

        print 'Starting Network Latency'
        while True:
            sys.stdout.write(spinner.next())
            sys.stdout.flush()
            sys.stdout.write('\b')
            
            if execution_count > 120: 
                metrics = latency_metrics(host)
                db_conn.write_points(metrics)
                execution_count = 0

            execution_count += 1 
            time.sleep(.5)
    except KeyboardInterrupt:
        print 'Quiting Network Latency'

if __name__ == '__main__':

    check_hosts = {
        'ip': '8.8.8.8',
        'hostname': 'google.com'
    }

    influx_client = InfluxDBClient('localhost', 8086, 'root', 'root', 'mydb')

    main(check_hosts, influx_client)
