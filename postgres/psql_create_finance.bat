
docker container cp postgresCreateTables.sql postgres:/

docker exec -it postgres psql -U postgres -d finance -f postgresCreateTables.sql
