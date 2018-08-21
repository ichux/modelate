#!/bin/sh
# chmod +x /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/reset.sh

# RUN with ". /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/reset.sh"
# RUN with "source /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/reset.sh"
# RUN with "bash /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/reset.sh"

cd /Users/chukwudinwachukwu/PycharmProjects/modplate

echo 'SITE_NAME =' $SITE_NAME
echo 'MODELATE_STATUS =' $MODELATE_STATUS
echo 'SECRET_KEY =' $SECRET_KEY
echo 'DB_TYPE =' $DB_TYPE
echo 'POSTGRES_DB =' $POSTGRES_DB
echo 'POSTGRES_HOST =' $POSTGRES_HOST
echo 'POSTGRES_PORT =' $POSTGRES_PORT
echo 'POSTGRES_PASSWORD =' $POSTGRES_PASSWORD
echo 'POSTGRES_USERNAME =' $POSTGRES_USERNAME

# remove all the variables
unset SITE_NAME MODELATE_STATUS SECRET_KEY DB_TYPE POSTGRES_DB POSTGRES_HOST
unset POSTGRES_PORT POSTGRES_PASSWORD POSTGRES_USERNAME

echo ""
echo 'SITE_NAME =' $SITE_NAME
echo 'MODELATE_STATUS =' $MODELATE_STATUS
echo 'SECRET_KEY =' $SECRET_KEY
echo 'DB_TYPE =' $DB_TYPE
echo 'POSTGRES_DB =' $POSTGRES_DB
echo 'POSTGRES_HOST =' $POSTGRES_HOST
echo 'POSTGRES_PORT =' $POSTGRES_PORT
echo 'POSTGRES_PASSWORD =' $POSTGRES_PASSWORD
echo 'POSTGRES_USERNAME =' $POSTGRES_USERNAME