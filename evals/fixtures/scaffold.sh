#!/usr/bin/env bash
# Copies the minimal Unity project into the case workspace (the current directory).
set -euo pipefail
here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -R "$here/minimal-project/." .
