#!/usr/bin/bash

function run () {

python3 observe.py -d ./save/PerDuelingDoubleDQNAgent_lr0.001_model.pack -max_steps 0

}

cd ..

source venv/bin/activate

run

deactivate

exit
