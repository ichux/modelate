#!/bin/sh
# chmod +x /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/echo.sh

# RUN with ". /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/echo.sh"
# RUN with "source /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/echo.sh"
# RUN with "bash /Users/chukwudinwachukwu/PycharmProjects/modplate/bash/dev/echo.sh"

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
