# AirBnB clone - The console

This school project is the first step in building an AirBnB clone. It uses
Python classes to represent users, places, states, cities, amenities, and
reviews. Objects have unique IDs and timestamps and can be saved to a JSON
file and loaded again.

The command interpreter uses Python's `cmd` module. At this stage, it supports
`help`, `quit`, and `EOF`. Commands to create, view, update, and delete objects
will be added in later tasks.

## Starting the console

Use Python 3.8 or later. From the repository directory, run:

```bash
./console.py
```

You can also start it with `python3 console.py`.

## Using the console

Type a command at the `(hbnb)` prompt and press Enter.

| Command | What it does |
| --- | --- |
| `help` | Lists available commands. |
| `help quit` | Shows help for the quit command. |
| `quit` | Closes the console. |
| `EOF` | Closes the console; Ctrl-D also works. |

An empty line does nothing.

### Interactive example

```text
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  help  quit

(hbnb) help quit
Quit the command interpreter.
(hbnb) quit
$
```

### Non-interactive example

You can pipe commands into the console:

```bash
echo "help" | ./console.py
printf 'help quit\nquit\n' | ./console.py
```

## Project files

- `console.py`: the command interpreter.
- `models/base_model.py`: shared IDs, timestamps, and model methods.
- `models/`: the User, Place, State, City, Amenity, and Review classes.
- `models/engine/file_storage.py`: saves and loads objects using JSON.
- `tests/`: unit tests arranged to match the project folders.
- `AUTHORS`: project contributors.

Storage writes to `file.json` in the current working directory when an object
or the storage instance is saved. The models package loads that file if it
exists.

## Running tests

Run all tests from the repository directory:

```bash
python3 -m unittest discover tests
```

Run a single test file:

```bash
python3 -m unittest tests/test_models/test_base_model.py
```

Tests also work in non-interactive mode:

```bash
echo "python3 -m unittest discover tests" | bash
```

Storage tests use temporary files so they do not change saved project data.

## Checking code style

Install the version required by the project and run the style check:

```bash
python3 -m pip install 'pycodestyle==2.7.0'
pycodestyle console.py models tests
```
