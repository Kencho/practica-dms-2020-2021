#!/bin/bash

SUCCESS=0

echo "[dms2021core]"
mypy components/dms2021core/dms2021core
SUCCESS=$((${SUCCESS}+$?))
echo "[dms2021auth]"
mypy components/dms2021core/dms2021core components/dms2021auth/dms2021auth
SUCCESS=$((${SUCCESS}+$?))
echo "[dms2021sensor]"
mypy components/dms2021core/dms2021core components/dms2021sensor/dms2021sensor
SUCCESS=$((${SUCCESS}+$?))
echo "[dms2021client]"
mypy components/dms2021core/dms2021core components/dms2021client/dms2021client
SUCCESS=$((${SUCCESS}+$?))

exit ${SUCCESS}
