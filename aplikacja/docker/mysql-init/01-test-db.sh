#!/bin/sh
mysql --protocol=socket -uroot -p"$MYSQL_ROOT_PASSWORD" \
	-e "GRANT ALL PRIVILEGES ON \`test_${MYSQL_DATABASE}\`.* TO '${MYSQL_USER}'@'%';"
