# AirBnB clone - The console

This school project is the first step in building an AirBnB clone. It uses
Python classes to represent users, places, states, cities, amenities, and
reviews. Objects have unique IDs and timestamps and can be saved to a JSON
file and loaded again.

The command interpreter uses Python's `cmd` module. At this stage, it supports
`help`, `quit`, `EOF`, and commands to create, view, update, and delete
objects of every supported class: `BaseModel`, `User`, `State`, `City`,
`Amenity`, `Place`, and `Review`.

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
| `create <class>` | Saves a new object and prints its ID. |
| `show <class> <id>` | Displays one object. |
| `destroy <class> <id>` | Deletes an object and saves the change. |
| `all [class]` | Lists all objects, optionally filtered by class. |
| `update <class> <id> <attribute> <value>` | Changes one attribute and saves. |

An empty line does nothing.

### Interactive example

```text
$ ./console.py
(hbnb) help

Documented commands (type help <topic>):
========================================
EOF  all  create  destroy  help  quit  show  update

(hbnb) help quit
Quit the command interpreter.
(hbnb) quit
$
```

### Managing an object

Run `create BaseModel` and use its printed ID in place of `<id>` below:

```text
create BaseModel
show BaseModel <id>
update BaseModel <id> name "My First Model"
all BaseModel
destroy BaseModel <id>
```

Put values containing spaces in double quotes. Updates keep an existing
attribute's string, integer, or float type; new attributes are strings.
Only the first attribute/value pair is used. IDs and timestamps cannot be
set through `update`.

The same commands work with the other classes. For example, run `create User`
and replace `<user-id>` with the printed ID:

```text
create User
update User <user-id> first_name "Betty"
update User <user-id> email "airbnb@mail.com"
show User <user-id>
all User
```

For a `Place`, updates such as `number_rooms 2` and `latitude -1.95` are stored
as an integer and a float. Fields such as `city_id`, `user_id`, and `place_id`
hold the IDs of related objects.

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
