#!/usr/bin/env python

import argparse
import os
import subprocess
import re
import json

def r128Stats(filePath, stream=0):
    """ takes a path to an audio file, returns a dict with the loudness
    stats computed by the ffmpeg ebur128 filter """
    ffargs = ["ffmpeg",
              '-nostats',
              '-i',
              filePath,
              '-filter_complex',
              '[a:%s]ebur128' % stream,
              '-f',
              'null',
              '-']
    proc = subprocess.Popen(ffargs, stderr=subprocess.PIPE)
    stats = proc.communicate()[1]
    summaryIndex = stats.rfind('Summary:')
    summaryList = stats[summaryIndex:].split()

    ILufs = float(summaryList[summaryList.index('I:') + 1])
    IThresh = float(summaryList[summaryList.index('I:') + 4])
    LRA = float(summaryList[summaryList.index('LRA:') + 1])
    LRAThresh = float(summaryList[summaryList.index('LRA:') + 4])
    LRALow = float(summaryList[summaryList.index('low:') + 1])
    LRAHigh = float(summaryList[summaryList.index('high:') + 1])
    statsDict = {'I': ILufs, 'I Threshold': IThresh, 'LRA': LRA,
                 'LRA Threshold': LRAThresh, 'LRA Low': LRALow,
                 'LRA High': LRAHigh}
    return statsDict


def linearGain(iLUFS, goalLUFS=-16):
    """ takes a floating point value for iLUFS, returns the necessary
    multiplier for audio gain to get to the goalLUFS value """
    gainLog = -(iLUFS - goalLUFS)
    return 10 ** (gainLog / 20)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Loudness Analyser.')
	parser.add_argument("-i", "--input", help="The video or audio filename ie /path/to/file/filename.mp4", required=True)
	parser.add_argument("-s", "--stream", help="The audio stream index", required=False, default=0)
	parser.add_argument("-t", "--target", help="The audio stream index", required=False, default=-16)
	args = parser.parse_args()

	if os.path.isfile(args.input):
		statsDict = r128Stats(args.input, args.stream)
		statsDict["gain"] = linearGain(statsDict["I"], float(args.target));
		print(statsDict)
	else:
		print "%s not found" % args.input



