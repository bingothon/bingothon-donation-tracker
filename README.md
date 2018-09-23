# donation-tracker-toplevel

This is the top level of my fork of the GamesDoneQuick donation tracker.  This version has been updated for Python 3 and Django 2.0+, as well as adding some new functionality we wanted for our marathons such as Horaro schedule syncing for events, the option to automatically count eligible donations towards ticketed prizes, and an optional revamped donation page layout with responsive styling.

As a result of the upgrades, I found the old migrations were incompatible at least for PostgreSQL due to one of the previous migrations changing a foreign key on an existing field.  The migrations have been regenerated from scratch for Django 2.0+ so if you're running some version of the GDQ tracker and you want to upgrade to this, you'll need to basically do a fresh install and dump/migrate your database records if you want to maintain them.  Sorry for the inconvenience!

In order to deploy the tracker, some boilerplate code is neccessary for configuration and management. The goal of this repository is to make doing so as simple as possible for any given user to get started developing on the tracker.

## Getting a Working Copy of the Tracker

1. [Install Git](http://www.git-scm.com/download). I'm assuming if you're here, you know enough about git and version control to get started. You can check if you have git with the command `which git`, and which version you have with `git --version`.
1. [Install Python](https://www.python.org/downloads/). This version of the tracker requires Python 3.4+ and Django 2.0+.  You can determine if Python is installed with the command `which python`, and which version of Python you have with the command `python -V`.  It may be installed as `python3` depending on your system.
1. [Install pip](https://pip.pypa.io/en/stable/installing/) This is the package management system we use with the tracker, and its generally the best option for getting Python packages.
1. [Install node](https://nodejs.org/en/download/). *Optional* If you want to use or develop on the fancy new Javascript UI (which right now only supports the schedule editor) you'll need this. Right now only v5.x is supported, but others may work.
1. [Install direnv](https://github.com/direnv/direnv). *Optional, Linux/OSX only* This will help set up an isolated development environment.
1. Clone this repository, typically I put it in a folder called `donations`, which is the path to which this repo will be referred for the remainder of these instructions:
    ```> git clone https://github.com/DorkmasterFlek/donation-tracker-toplevel.git donations```
1. Make a copy of `example_local.py` under `donations`, and call it `local.py`. This is where you will enter any deployment-specific settings for your instance of the website.
    ```> cp example_local.py local.py```
    1. (optional) Change the `NAME` field under the `DATABASES` variable to point at a different location if you wish.
    2. There are some other config variables related to timezone, e-mail, google docs, and giantbomb's API. None of these are neccessary to get started, and mostly can be ignored unless you are interested in that specific feature. Documentation on these fields is lacking, but it shouldn't be too diffficult to figure out how they work if you take a look at `settings.py`.
1. Clone the submodules.
    ```> git submodule update --init```
    1. This will clone `tracker` (the main backend and the classic frontend), `tracker_ui` (the fancy new experimental Javascript UI).
1. Download the requirements in using pip:
    ```> pip install -r tracker/requirements.txt```
    ```> pip install -r tracker_ui/requirements.txt```
    1. If you are using Windows, you may need to delete the lines containing `psycopg2` and `chromium-compact-language-detector` from `tracker/requirements.txt` (both are optional, and require compilation of C code, which is typically a hassle for people in a Windows environment).
    2. If you are under 'nix or Mac, you'll probably need to `sudo` this/run as administrator, unless you're using `direnv` as suggested above.
    3. The default pip configuration performs a fresh install of all packages, meaning that previously installed packages will be uninstalled before being reinstalled. If you get any exceptions during uninstallation, you can try the flag `--ignore-installed` to leave those packages alone and continue with other packages.
1. Initialize the database. This app, and all the apps it depends on, can be initialized into the database using django's migrate command, `python manage.py migrate`. Notes:
    1. This is the actual command that will create the `db/testdb` file on your machine (if it does not exist already).
    2. If you are using a different location, or a different database type, you will need to make sure the permissions and settings are set up correctly.
    3. This is the general command to migrate all changes in the app. If you ever update any of the dependent libraries, or the tracker itself, you should run this command again.
1. Create a superuser account for the admin with the command `python manage.py createsuperuser` and follow the prompts. This is the account you'll use to access your testing instance of the app.
1. Install the required npm packages. *Optional*
    ```> cd tracker_ui && npm i```
    Only needed if you want to use or develop the fancy new experimental UI.

## Running the test server (see below on how to launch the UI)

You can run the test server, using the command `python manage.py runserver [port]`. The `port` argument is optional; the default is 8000.

You can navigate to the tracker at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) (where `8000` is the the port specified). To view the admin site, go to: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/) and log in using the username/password you set up with `createsuperuser`.

## Building the UI package (release mode)

Simply run the build command in the `tracker_ui` directory:
```> webpack --config tracker_admin.release.webpack.js```

This does two things:

1. Builds the UI Javascript and CSS bundles and puts them in `tracker_ui/static/gen`.
1. Outputs a manifest file to `ui_admin.manifest.json` so that Django knows where to find the resulting bundles.

This will allow the tracker UI to function, though if you want to develop with it you'll want to use the development proxy below, otherwise you'll not only have a minified build (difficult to debug!) but you'll have to rerun the command every time you make a change.

## Running the UI development server

Webpack has a development server that can proxy requests to the backend. Once you've installed the required packages, you can run the server with the following command while in the `tracker_ui` folder:
```> ./dev.sh```

It defaults to port 8080, so simply visit [http://127.0.0.1:8080/](http://127.0.0.1:8080) and you should be able to view the site just like the Django development server.

Note that if you change the port that the server is running on you'll need to edit `shared.webpack.js` to point to the correct port in the proxy section.

## Server deployment

There are far too many different ways to deploy the server to go over every possibility here, so you should start with [Deploying Django](https://docs.djangoproject.com/en/dev/howto/deployment/).

Note that node is NOT required to run the server in a production environment, it is ONLY needed to build the Javascript UI package. You can build it locally and simply copy the necessary files to your server. *Don't forget the manifest file!*

## Docker (experimental, development environments only)

I haven't tested the Docker deployment at all with this, as we don't use Docker for our deployment.  This was experimental in the GDQ version, so if you want to mess with it, do so at your own risk.
