#!/bin/bash

INVOCATION_DIR=$(dirname "$0")

SUCCESS=0

"${INVOCATION_DIR}/verify-type-correctness.sh"
SUCCESS=$((${SUCCESS}+$?))

exit ${SUCCESS}
