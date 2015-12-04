Deployment Files
----------------

 * `launch_uwsgi.sh` - Creates a socket for nginx to make requests to the application.
 * `iptables.rules` - Prevents access from baddies.  Can be loaded via `sudo iptables-restore < iptables.rules`
 * `nginx-sites-enabled-default` - Should be copied as `/etc/nginx/sites-enabled/default`
