#!/bin/sh

# chmod +x /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/bootstrap.sh

# RUN with ". /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/bootstrap.sh"
# RUN with "source /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/bootstrap.sh"
# RUN with "bash /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/bootstrap.sh"

cd /Users/chukwudinwachukwu/PycharmProjects/modplate
source /Users/chukwudinwachukwu/PycharmProjects/modplate/.venv/bin/activate
source /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/variables.sh

printf "\033c"   # clear console
echo "Date is: `date`"
echo "You are login as: `whoami`"
echo ""
echo "BASH LOCATIONS"
find $PWD/bash/dev -type f -name "*.sh"  # ls -l bash/dev/
find . -name '*.pyc' -delete
echo ""
echo "PWD: `pwd`"
#python manage.py db current