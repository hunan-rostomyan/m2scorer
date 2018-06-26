#!/usr/bin/env python3
import argparse
import json
import os

parser = argparse.ArgumentParser(description='M2 gold to json converter')
parser.add_argument('source_gold', type=str, help='path to source_gold file')
parser.add_argument('-o', type=str, help='export to this directory under the same file name')
parser.add_argument('--pretty', action='store_true', help='make the json more readable')
parser.add_argument('--dry', action='store_true', help='dump output to screen instead of writing to file')

args = parser.parse_args()

path = args.source_gold

SENTENCE, ANNOTATION = 'S', 'A'

def Empty(line):
    return (line.strip()) == ''

def get_kind(line):
    return line[0]

def get_sentence(line):
    return line[1:].strip()

def get_annotation(line, sep='|||'):
    prefix, etype, edits, required, comment, anid = line.split(sep)
    _, start, end = prefix.split()
    edits = edits.split('||')
    return {
        'start': int(start),
        'end': int(end),
        'error': etype,
        'edits': edits,
        'annotator': int(anid)
    }

try:
    with open(path) as fp:
        gold = {}
        sent, sid = '', 0
        for line in fp:
            if not Empty(line):
                if get_kind(line) == SENTENCE:
                    sent = get_sentence(line)
                    sid += 1
                else:
                    if sid not in gold:
                        gold[sid] = {'sentence': sent, 'annotations': []}
                    annotation = get_annotation(line)
                    gold[sid]['annotations'].append(annotation)

    # prepare output
    output = json.dumps(gold, indent=2) if args.pretty else json.dumps(gold)

    # prepare export path
    if args.o:
        path = os.path.join(args.o, path.split('/')[-1])

    if args.dry:
        print(output)
    else:
        with open(path + '.json', 'w') as fp:
            fp.write(output)
except FileNotFoundError as e:
    print('Unable to write to: {}'.format(path))
