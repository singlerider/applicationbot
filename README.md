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

Follow Google's Python Quickstart at:
https://developers.google.com/gmail/api/quickstart/python

Make sure to run

`pip install --upgrade google-api-python-client`

in order to download the dependencies. There's a helpful wizard for setting up
authentication at:
https://console.developers.google.com/flows/enableapi?apiid=gmail

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
