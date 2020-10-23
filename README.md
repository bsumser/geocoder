## Installation

Create a Virtual Environment in the project folder

```bash
mkdir <venv_name>
python3 -m venv <venv_name>
```

Activate the Virtual Environment 

```bash
. <venv_name>/bin/activate
```

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the requirements to run this project.

```bash
pip install -e . 
```

Setup Environment Variables and run the project

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Your project will be available at http://127.0.0.1:5000/