#!/usr/bin/bash

cd ../

source venv/bin/activate
if [ -z "${1}" ]; then
    python3 observe.py -d ./save/PerDuelingDoubleDQNAgent_lr0.001_model.pack
else
    python3 observe.py "${@}"
fi
deactivate

exit
