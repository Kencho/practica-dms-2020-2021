#!/bin/bash

pylint --fail-under=7.0 -f text components/dms2021core/dms2021core components/dms2021auth/dms2021auth components/dms2021sensor/dms2021sensor components/dms2021client/dms2021client
