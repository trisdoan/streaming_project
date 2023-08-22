up:
	docker compose up --build -d

down:
	docker compose down --volumes --rmi all 

sleep:
	sleep 20 


####################################################################################################################
# Run ETL
run-main-job:
	docker exec jobmanager ./bin/flink run --python ./src/run_checkout_attrs.py

run: down up sleep run-main-job


####################################################################################################################
# Monitoring
viz:
	open http://localhost:3000

flink-ui:
	open http://localhost:8081/

postgres:
	docker exec -ti postgres psql postgres://postgres:postgres@localhost:5432/postgres