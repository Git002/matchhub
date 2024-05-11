# How to setup this project?

### 1.) Create a virtual environment:
Use venv, to create a virtual environment:

```
python -m venv venv
```

This will create a virtual environment named venv in your current directory.

### 2.) Activate the virtual environment:
Before installing packages, you need to activate the virtual environment.

- On Windows:
```
.\venv\Scripts\activate
```

- On Unix or MacOS:
```
source venv/bin/activate
```

### 3.) Install dependencies from requirements.txt:
Once the virtual environment is activated, you can install the dependencies listed in `requirements.txt` using pip.

```
pip install -r requirements.txt
```

This command will install all the packages listed in the requirements.txt file

# How to run this?
```
python app.py
```

# How to test this project?

```
pip install pytest
```

Then do:

```
pytest -v
```
