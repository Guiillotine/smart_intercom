#!/usr/bin/env bash

alembic upgrade head

python3 scripts/initializer.py

python3 run.py
