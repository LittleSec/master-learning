PYTHON3=$(which python3)
LOGIN_PY=/path/to/login_nju_wlan_py3.py

LOG_FILE=/tmp/login_nju_wlan.log

nohup $PYTHON3 $LOGIN_PY >>$LOG_FILE 2>&1 &
