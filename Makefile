up:
	docker compose up --build -d

down:
	docker compose down --volumes --rmi all 

sleep:
	sleep 20 


####################################################################################################################
# Run ETL



####################################################################################################################
# Monitoring
viz:
	open http://localhost:3000

ui:
	open http://localhost:8081/

# postgres:
# 	docker exec -ti postgres psql postgres://postgres:postgres@localhost:5432/postgres