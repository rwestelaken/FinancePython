#set +x
docker exec -it postgres pg_dumpall -c -U postgres > ./dump_`date +%Y-%m-%d"_"%H_%M_%S`.sql
