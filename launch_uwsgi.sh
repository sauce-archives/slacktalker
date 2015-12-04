uwsgi -s /tmp/uwsgi.sock --module webapp --callable app --chmod-socket=666
