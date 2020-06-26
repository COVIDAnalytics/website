# This workflow will install Python dependencies, run tests and lint with a single version of Python
# For more information see: https://help.github.com/actions/language-and-framework-guides/using-python-with-github-actions

name: Python application

on:
  pull_request:
    branches: [ master ]

jobs:
  build:

    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python 3.8
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    - name: Install dependencies
      run: |
        ls
        #python -m pip install --upgrade pip
        #if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Print Hello
      run: |
        python3 -c "print('Hello from Python')"
        python3 ./CI/check_csv.py
        cat test.csv
        git branch
        git describe --always


