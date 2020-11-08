#!/bin/bash

set -xe

cd /tmp/deps/src/core
./install.sh

cd /tmp/src
./install.sh
./start.sh
