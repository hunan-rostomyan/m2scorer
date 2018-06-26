#!/usr/bin/env python3
import argparse
import datetime
import json
import os
import re
import requests
import subprocess
import time

parser = argparse.ArgumentParser(description='Apply a gec system to a set of sentences')
parser.add_argument('sentences', type=str, help='path to sentences json file')
parser.add_argument('gold', type=str, help='path to gold m2 file')
parser.add_argument('api', type=str, help='address of the gec api (including http://)')
parser.add_argument('--pretty', action='store_true', help='make the metrics more readable')
parser.add_argument('--dry', action='store_true', help='dump output to screen instead of writing to file')

args = parser.parse_args()


# Get the sentences
# -----------------
with open(args.sentences) as fp:
	sentences = json.load(fp)


# Get the corrections
# -------------------
corrections = []
start = time.time()
for sid in sentences:
	sentence = sentences[sid]
	resp = requests.post(args.api + '/correct', json={'sentence': sentence}) 
	correction = resp.json()['correction']
	corrections.append(correction)
duration = time.time() - start

# write the corrections to a /tmp file
with open('/tmp/corrections', 'w') as fp:
	for correction in corrections:
		fp.write(correction + '\n')


# Score
# -----
p = subprocess.Popen('./m2scorer /tmp/corrections {}'.format(args.gold), shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)


# Read the results from stdout
# ----------------------------
metrics = {}
for line in p.stdout.readlines():
    line = line.decode('utf-8').strip()
    parts = [part.strip() for part in line.split(':')]
    metric, score = parts
    metrics[metric.lower()] = float(score)
#retval = p.wait()


# Export the results
# ------------------
# convert api to filename
name = '_'.join(re.match('.*://([a-zA-Z0-9]+):([0-9]+)', args.api).groups())

# add useful meta
metrics['api'] = name
metrics['duration(s)'] = duration
metrics['time'] = str(datetime.datetime.now())

output = json.dumps(metrics, indent=2) if args.pretty else json.dumps(metrics)

if args.dry:
    print(output)
else:
	with open(os.path.join('results', name) + '.metrics.json', 'w') as fp:
		fp.write(output)
