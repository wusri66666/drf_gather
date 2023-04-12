#本地部署
#mkdir /opt/homebrew/etc/supervisord.d && echo_supervisord_conf > /opt/homebrew/etc/supervisord.conf
#cat <<EOF >> /opt/homebrew/etc/supervisord.conf
#[include]
#files = /opt/homebrew/etc/supervisord.d/*.conf
#EOF
#
#cat <<EOF >> /opt/homebrew/etc/supervisord.d/django.conf
#[program:drf_gather]
#command=/Users/wzj/.virtualenvs/wzj/bin/gunicorn -c gunicorn.py drf_gather.wsgi:application
#directory=/Users/wzj/project_python/Django/drf_gather
#user=wzj
#
#EOF

#docker部署
mkdir /etc/supervisord.d && echo_supervisord_conf > /etc/supervisord.conf
cat <<EOF >> /etc/supervisord.conf
[include]
files = /etc/supervisord.d/*.conf
EOF

cat <<EOF >> /etc/supervisord.d/django.conf
[program:drf_gather]
command=daphne drf_gather.asgi:application -b 0.0.0.0 -p 8000
directory=/app
autostart=true
autorestart=true
user=root
stdout_logfile=/var/log/supervisor_info.log
stderr_logfile=/var/log/supervisor_error.log

EOF