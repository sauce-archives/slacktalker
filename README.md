About
-----

This runs on `slacktalker.dev.saucelabs.net`.  The main web application is running via nginx and uwsgi.  All code is deployed under the sauce user.  There's no fancy upstart script for uwsgi -- it's just running as a background job.

Deploying
---------

Run `update_repo.sh` to change to the sauce user and pull down the latest git commit.  You'll need to have SSH agent forwarding enabled when connecting to the box.

Files
-----

Deployment Files
================

 * `launch_uwsgi.sh` - Creates a socket for nginx to make requests to the application.
 * `iptables.rules` - Prevents access from baddies.  Can be loaded via `sudo iptables-restore < iptables.rules`
 * `nginx-sites-enabled-default` - Should be copied as `/etc/nginx/sites-enabled/default`

Data-loading Files
==================

 * `parse_users.py` - takes the `users.json` file from the slack export and loads up the users into the users table
 * `parse_words.py` - loads up words from the various channels and puts them into the database
 * `model.py` - the models for interacting with the DB.  If run directly, this will build the tables needed for loading data
