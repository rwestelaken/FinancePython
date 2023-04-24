
sudo docker container cp /home/westy/Source/FinancePython/src/postgresCreateTables.sql postgres:/

sudo docker exec -it postgres psql -U postgres -d finance -f postgresCreateTables.sql
