# installationbot

Looking for work?

Just now realizing you're a programmer?

Just now realizing that you can customize a script to do the boring part so you
can study up and improve your skills?

Well, look no further (for now)!

This script will help with anxiety about applying to places with "senior" in the
job description. It makes it so easy that you won't have time for "second
thoughts!" Who knows? Maybe you'll get the job!

## Installation

Setting up a virtual environment (ideally), installing dependencies, and gaining
credentials.

### Virtual Environment

I would recommend running this in a virtual environment to keep your
dependencies in check. If you'd like to do that, run:

`sudo pip install virtualenv`

Followed by:

`virtualenv venv`

This will create an empty virtualenv in your project directory in a folder
called "venv." To enable it, run:

`source venv/bin/activate`

and your console window will be in that virtualenv state. To deactivate, run:

`deactivate`

### Dependencies

To install all dependencies locally (preferably inside your activated
virtualenv), run:

`pip install -r requirements.txt`

### Gmail

For more information, follow Google's Python Quickstart at:

https://developers.google.com/gmail/api/quickstart/python

There's a helpful wizard for setting up authentication for GMail's API at:

https://console.developers.google.com/flows/enableapi?apiid=gmail

### Trello

You will also need to attain Trello credentials by following these steps:

Apply for an API key at:

https://developers.trello.com/

To get your Trello Token, go here in a browser and replace YOURAPIKEY:

https://trello.com/1/authorize?key=YOURAPIKEY&name=My+App&expiration=30days&response_type=token&scope=read,write

Once authorized, you'll be able to grab your token from the address bar

### Mac Notes

There's an issue with Matplotlib installed as a service on Mac. Simply do the
following to eliminate the issue:

In your home directory, there is a directory called ~/.matplotlib. Create a file
called "matplotlibrc" inside the folder "~/.matplotlib/":

`touch ~/.matplotlib/matplotlibrc`

and add the following line and save:

`backend: TkAgg`

## To Run

Once you have all the boring stuff out of the way and your Google account is
authenticated, it's time to start emailing employers!

Run

`cp config_example.py config.py`

to create the configuration file that will be used (and omitted from git,
should you choose to improve on the code yourself) for the project. Edit the new
config file and format your fancy new cover letter however you'd like.

Finally, run

`./bot.py`

## To-do

Think of other cool stuff to implement
