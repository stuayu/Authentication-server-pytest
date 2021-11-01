# Authentication-server-pytest
Learn about secure login authentication with fastapi.

## About this project
```
Authentication-server-pytest/
│   .gitignore
│   config.yml
│   config.yml.template
│   docker-compose.yml
│   LICENSE
│   main.py
│   Pipfile
│   Pipfile.lock
│   README.md
│   requirements.txt
│
├───db
│   │   acsess.py
│   │   auth.sqlite3
│   
├───functions
│   │   auth_func.py
│   │
│   └───__pycache__
│           auth_func.cpython-310.pyc
│
├───model
│   │   auth_m.py
│
├───routers
│   │   auth.py
│
├───static(abbreviation)
│   │   index.html

```

## Easy Start Guide
1. Copy config.yml.template to config.yml.
2. Execute the following command and copy it to config.yml.
    `openssl rand -hex 32`
3. Execute the following commands sequentially.
    ```bash
    $ sudo docker-compose pull
    $ sudo docker-compose up -d
    ```
## Getting Started Guide
0. Follow steps 1 and 2 in the Easy Start Guide.
1. Prepare the execution environment.  
    ```powershell
    $ pip install pipenv
    $ pipenv install
    ```
2. Connect to the shell of the virtual environment.
    ```powershell
    $ pipenv shell
    ```
3. Activate the system.
    ```powershell
    $ uvicorn main:app --reload
    ```

## LISENSE
The static directory is licensed by CC BY 3.0.  
The author is Colorlib. [Distribution source](https://colorlib.com/wp/template/login-form-v16/)   
The rest of the program is under the [MIT license](./LICENSE).