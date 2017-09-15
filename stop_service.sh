supervisorctl -c $HOME/supervisor/supervisord.conf stop easy-flask:
cp ./supervisor/supervisor.ini $HOME/supervisor/supervisord.conf.d/easy-flask.conf
supervisorctl -c $HOME/supervisor/supervisord.conf add easy-flask
supervisorctl -c $HOME/supervisor/supervisord.conf update easy-flask
true
