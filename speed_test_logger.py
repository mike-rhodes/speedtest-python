#!/usr/bin/python
import os
import sys
import csv
import datetime
import time
import tweepy
import subprocess
 
def main():
    print "======================================"
    print " Starting Speed Complainer!           "
    print " Lets get noisy!                      "
    print "======================================"

    monitor = Monitor()

    stopProgram = False

    while not stopProgram:

		try:

			monitor.run()

		except Exception as e:
			print 'Error: %s' % e
			sys.exit(1)


class Monitor():
    def __init__(self):
        self.lastPingCheck = None
        self.lastSpeedTest = None
        self.timeToPassBetweenTests = 5*60

    def run(self):
        if not self.lastSpeedTest or (datetime.datetime.now() - self.lastSpeedTest).total_seconds() >= self.timeToPassBetweenTests:
            self.runSpeedTest()
            self.lastSpeedTest = datetime.datetime.now()

    def runSpeedTest(self):
        speedThread = SpeedTest()
        speedThread.run()

class SpeedTest():
	def __init__(self):
		pass

	def run(self):
		speedTestResults = self.doSpeedTest()
		self.logSpeedTestResults(speedTestResults)

	def doSpeedTest(self):
		# run a speed test
		#run speedtest-cli
		speed_test = subprocess.check_output(["/home/mrhodes/.anaconda2/bin/speedtest-cli --simple"], shell = True)
		print datetime.datetime.now()
		print speed_test
		print '-' * 20

		if 'Cannot' in speed_test:
			pingResult = 1000
			downloadResult = 0
			uploadResult = 0
		else:
			resultSet = speed_test.split('\n')
			pingResult = resultSet[0]
			downloadResult = resultSet[1]
			uploadResult = resultSet[2]

			pingResult = float(pingResult.replace('Ping: ', '').replace(' ms', ''))
			downloadResult = float(downloadResult.replace('Download: ', '').replace(' Mbit/s', ''))
			uploadResult = float(uploadResult.replace('Upload: ', '').replace(' Mbit/s', ''))

			return { 'date': datetime.datetime.now(), 'uploadResult': uploadResult, 'downloadResult': downloadResult, 'ping': pingResult }

	def logSpeedTestResults(self, speedTestResults):
		out_file = open('speedtest_results.csv', 'a')
		writer = csv.writer(out_file)
		writer.writerow((speedTestResults['date'].strftime('%Y-%m-%d %H:%M:%S'), str(speedTestResults['ping']), str(speedTestResults['uploadResult']), str(speedTestResults['downloadResult'])))
		out_file.close()
		print "Test successful"

if __name__ == '__main__':
    main()