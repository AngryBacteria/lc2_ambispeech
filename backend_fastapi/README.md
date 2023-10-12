# How to install and run

Requirements:
- Python Version 3.11.5

For the following commands you may need either the `python` or `python3` and 
`pip` or `pip3` prefix. Test out what is installed on your system.

Clone the Repo and cd into the folder

```python -m venv env```

Install the python virtual environment (venc). Restart your IDE after this

```python -m venv env```

Install the requirements

```pip install -r requirements.txt```

Start the app with uvicorn

```uvicorn app/main:app --reload```