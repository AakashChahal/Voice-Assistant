#!/usr/bin/env python3

import sys
import subprocess


def check_speed():
    try:
        import speedtest
    except:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'speedtest-cli'])
    finally:
        import speedtest
        test = speedtest.Speedtest()
        print("Checking your download speed...")
        down = test.download()  # tests download speed
        print("Done...")
        print("Now checking your upload speed...")
        up = test.upload()  # tests upload speed
        print("Done...")
        return (
            "your Download Speed is {:.2f} MB PS and your Upload Speed is {:.2f} MB PS".format(down / 1024 * 0.0009765625,
                                                                                           up / 1024 * 0.0009765625))


if __name__ == '__main__':
    check_speed()
