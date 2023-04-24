
sudo docker exec -it postgres psql -U postgres

sudo docker container cp postgresCreateTables.sql postgres:/

sudo docker exec -it postgres psql -U postgres -dbname:finance -f /Source/CashFlowLambda/DataAccess/src/main/resource/postgresCreateTables.sql

sudo docker exec -it postgres pg_dumpall -c -U postgres > dump_`date +%d-%m-%Y"_"%H_%M_%S`.sql

sudo cat dump.sql | sudo docker exec -it postgres psql -U postgres

