# alu-AirBnB_clone_v2

Fork maintained by [owizdom](https://github.com/owizdom/alu-AirBnB_clone_v2).

This repository contains the second iteration of the AirBnB clone project. It extends the original console and models by:
- adding a database storage engine using SQLAlchemy (DBStorage)
- keeping support for JSON file storage (FileStorage) via an environment switch
- improving the console `create` command to accept key=value parameters
- providing MySQL setup scripts for dev and test databases
- maintaining unit tests for both storage engines (with skips where appropriate)

## Command Interpreter (console)

The command interpreter (CLI) lets you create, read, update and delete objects stored either in `file.json` (FileStorage)
or in MySQL (DBStorage).

### How to start

```bash
./console.py
```

Or run non-interactively:

```bash
echo 'all State' | ./console.py
```

### Storage selection

**FileStorage (default):**

```bash
./console.py
```

**DBStorage:**

```bash
HBNB_MYSQL_USER=hbnb_dev HBNB_MYSQL_PWD=hbnb_dev_pwd \
HBNB_MYSQL_HOST=localhost HBNB_MYSQL_DB=hbnb_dev_db \
HBNB_TYPE_STORAGE=db ./console.py
```

### Usage examples

```bash
(hbnb) create State name="California"
(hbnb) create City state_id="<STATE_ID>" name="San_Francisco"
(hbnb) all State
(hbnb) show State <STATE_ID>
(hbnb) update State <STATE_ID> name "Nevada"
(hbnb) destroy State <STATE_ID>
(hbnb) quit
```

Parameterized create (FileStorage only for this feature test):

```bash
(hbnb) create Place city_id="0001" user_id="0001" name="My_little_house" number_rooms=4 price_by_night=300
```

## Authors

See the `AUTHORS` file for contributors. Do not remove existing authors; append new contributors.
