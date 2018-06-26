#!/usr/bin/env python3
import argparse
import json

parser = argparse.ArgumentParser(description='Extract (tokenized) sentences from m2 gold json')
parser.add_argument('source_gold_json', type=str, help='path to source_gold json file')
parser.add_argument('--pretty', action='store_true', help='make the json more readable')
parser.add_argument('--dry', action='store_true', help='dump output to screen instead of writing to file')

args = parser.parse_args()

input_path = args.source_gold_json
ouput_path = '.'.join(input_path.split('.')[:-1])

data = json.load(open(input_path))
new_data = {}
for sid in data:
	new_data[sid] = data[sid]['sentence']

output = json.dumps(new_data, indent=2) if args.pretty else json.dumps(new_data)

if args.dry:
    print(output)
else:
	with open(ouput_path + '.sentences.json', 'w') as fp:
		fp.write(output)