Deployment Files
----------------

 * `launch_uwsgi.sh` - Creates a socket for nginx to make requests to the application.
 * `iptables.rules` - Prevents access from baddies.  Can be loaded via `sudo iptables-restore < iptables.rules`
 * `nginx-sites-enabled-default` - Should be copied as `/etc/nginx/sites-enabled/default`

Data-loading Files
------------------

 * `parse_users.py` - takes the `users.json` file from the slack export and loads up the users into the users table
 * `parse_words.py` - loads up words from the various channels and puts them into the database
 * `model.py` - the models for interacting with the DB.  If run directly, this will build the tables needed for loading data
