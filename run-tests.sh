#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2019-2020 CERN.
# SPDX-FileCopyrightText: 2019-2020 Northwestern University.
# SPDX-FileCopyrightText: 2020-2026 Graz University of Technology.
# SPDX-License-Identifier: MIT

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

ruff check .

python -m pytest
