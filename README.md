See README for the original description.

# Introduction

There are two concepts introduced here. **System** is any python program that exposes a `/correct` endpoint over HTTP and has this signature:

**input:**

```json
{"sentence": "[sentence to be corrected]"}
```

**output:**

```json
{"correction": "[corrected version of sentence]"}
```

The **exerciser** "exercises" these systems: loops over sentences, makes requests to a system to get corrections, and shells out to the M2 scorer to measure the performance of the system. The details are below.

# Systems

Systems expose APIs to allow their outputs to be scored. There are three examples under **systems/**. The exerciser expects them to be running, so do this:

```bash
# Run three "systems", each on its own port
$ FLASK_APP=example_system.py flask run --port 5001
$ FLASK_APP=example_system2.py flask run --port 5002
$ FLASK_APP=example_system3.py flask run --port 5003
```

# Exerciser

The exerciser takes sentences (`exports/source_gold.sentences.json`), gold annotations (`example/source_gold`), a system API endpoint (`http://localhost:5001`) and makes POST requests to get corrections for each sentence.

### Output

To get the results without exporting to a file:

```
./scripts/exercise.py \
    exports/source_gold.sentences.json \
    example/source_gold \
    http://localhost:5001 \
    --dry \
    --pretty
```

This will display something like this:

```json
{
  "precision": 0.8,
  "recall": 0.8,
  "f_0.5": 0.8,
  "api": "localhost_5003",
  "duration(s)": 0.024756193161010742,
  "time": "2018-06-26 15:58:43.547668"
}
```

### Export

To export to a file, omit the `--dry` option:

```
./scripts/exercise.py \
    exports/source_gold.sentences.json \
    example/source_gold \
    http://localhost:5001 \
    --pretty
```

This will create a file **results/localhost_5001.metrics.json**, containing the json above.

## Disable pretty-printing

If you want a one-line json instead of the indented one, omit the `--pretty` flag to get:

```json
{"precision": 0.8, "recall": 0.8, "f_0.5": 0.8, "api": "localhost_5001", "duration(s)": 0.019103050231933594, "time": "2018-06-26 16:04:06.745932"}
```

# Utilities

### Gold to Json

```
$ ./scripts/get_gold.py example/source_gold -o exports/ --pretty
```

This will convert this:

```
S The cat sat at mat .
A 3 4|||Prep|||on|||REQUIRED|||-NONE-|||0
A 4 4|||ArtOrDet|||the||a|||REQUIRED|||-NONE-|||0

S The dog .
A 1 2|||NN|||dogs|||REQUIRED|||-NONE-|||0
A -1 -1|||noop|||-NONE-|||-NONE-|||-NONE-|||1

S Giant otters is an apex predator .
A 2 3|||SVA|||are|||REQUIRED|||-NONE-|||0
A 3 4|||ArtOrDet|||-NONE-|||REQUIRED|||-NONE-|||0
A 5 6|||NN|||predators|||REQUIRED|||-NONE-|||0
A 1 2|||NN|||otter|||REQUIRED|||-NONE-|||1
```

into:

```json
{
  "1": {
    "sentence": "The cat sat at mat .",
    "annotations": [
      {
        "start": 3,
        "end": 4,
        "error": "Prep",
        "edits": [
          "on"
        ],
        "annotator": 0
      },
      {
        "start": 4,
        "end": 4,
        "error": "ArtOrDet",
        "edits": [
          "the",
          "a"
        ],
        "annotator": 0
      }
    ]
  },
  "2": {
    "sentence": "The dog .",
    "annotations": [
      {
        "start": 1,
        "end": 2,
        "error": "NN",
        "edits": [
          "dogs"
        ],
        "annotator": 0
      },
      {
        "start": -1,
        "end": -1,
        "error": "noop",
        "edits": [
          "-NONE-"
        ],
        "annotator": 1
      }
    ]
  },
  "3": {
    "sentence": "Giant otters is an apex predator .",
    "annotations": [
      {
        "start": 2,
        "end": 3,
        "error": "SVA",
        "edits": [
          "are"
        ],
        "annotator": 0
      },
      {
        "start": 3,
        "end": 4,
        "error": "ArtOrDet",
        "edits": [
          "-NONE-"
        ],
        "annotator": 0
      },
      {
        "start": 5,
        "end": 6,
        "error": "NN",
        "edits": [
          "predators"
        ],
        "annotator": 0
      },
      {
        "start": 1,
        "end": 2,
        "error": "NN",
        "edits": [
          "otter"
        ],
        "annotator": 1
      }
    ]
  }
}
```

### Gold json to sentences

```
$ ./scripts/get_sentences.py exports/source_gold.json --dry --pretty
```

```json
{
  "1": "The cat sat at mat .",
  "2": "The dog .",
  "3": "Giant otters is an apex predator ."
}
```

This can then be passed to the exerciser.
