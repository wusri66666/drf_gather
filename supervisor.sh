#!/bin/bash

bash supervisor_init.sh

#本地部署
#supervisord -c /opt/homebrew/etc/supervisord.conf
#docker部署
supervisord -c /etc/supervisord.conf

tail -f  /dev/null