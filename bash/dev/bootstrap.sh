#!/bin/sh

# chmod +x /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/bootstrap.sh

# RUN with ". /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/bootstrap.sh"
# RUN with "source /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/bootstrap.sh"
# RUN with "bash /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/bootstrap.sh"

cd /Users/chukwudinwachukwu/PycharmProjects/modplate
source /Users/chukwudinwachukwu/PycharmProjects/modplate/.venv/bin/activate

export SITE_NAME=site-1
export MODELATE_STATUS=development
export SECRET_KEY=a7f832fbf5926a9859270c13ea80a7e55c0801734d196b59b9a2495e90e05757
export DB_TYPE=POSTGRES  # MYSQL
export POSTGRES_DB=rensource
export POSTGRES_HOST=192.168.56.20
export POSTGRES_PORT=5432
export POSTGRES_PASSWORD=R3n50urc3
export POSTGRES_USERNAME=rensource

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