# SimpleLogsApp

#### Create virtual environment

`python3 -m venv logsapp-env`

#### Activate environment

`source logsapp-env/bin/activate`

#### Clone the repository

`git clone git@jazbec-projekti.si:timotejd/SimpleLogsApp.git`

#### Install requirements

`cd SimpleLogsApp/myapp && pip3 install -r requirements.txt`

#### Create tables

`python3 manage.py migrate --run-syncdb`

#### Create admin user

`python3 manage.py createsuperuser`

#### Run

`python3 manage.py runserver`

and visit [127.0.0.1:8000](http://127.0.0.1:8000/)

### Api logs post testing

In another terminal instance activate venv and navigate to tests folder

`cd SimpleLogsApp/myapp/tests`

Logs can only be added to existing projects. Add project "example-project" via app UI and run:

`python3 api_post_test.py --username "your_username" --password "your_password" --severity "0" --timestamp "2022-01-11T10:53:00" --projectname "example-project" --content "system explosion"`

This will authenticate the request via obtained JWT and post the example log. 
Projects and logs can be overviewed via app UI.
For site administration and regular user creation visit the [admin page](http://127.0.0.1:8000/admin/)


