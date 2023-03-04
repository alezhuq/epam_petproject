# temporary : personal note


command for compose 
command: flask --debug run --host=0.0.0.0
    environment:
      - POSTGRES_NAME=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres


docker ps
docker exec -it x bash
flask db init
flask db migrate -m  "x"
flask db upgrade


# Service API
## Get all services
URL: /services

Method: GET

Response format: JSON

Response status codes: 200 OK, 404 Not Found

Description: Returns a list of all services.

Response example: 
[    
{        
"id": 1,        
"name": "Service 1",        
"description": "Description of service 1",       
"price": 100,        "company_id": 1    
},    
{        
"id": 2,        
"name": "Service 2",       
"description": "Description of service 2",        
"price": 200,        
"company_id": 1    
}]
# Create a new service
URL: /services

Method: POST

Request format: JSON

Request body:
{
    "name": "Service 3",
    "description": "Description of service 3",
    "price": 300,
    "company_id": 2
}
Response format: JSON

Response status codes: 200 OK

Description: Creates a new service.

Response example:

{
    "id": 3,
    "name": "Service 3",
    "description": "Description of service 3",
    "price": 300,
    "company_id": 2
}
## Get a service by ID
URL: /services/{id}

Method: GET

URL parameters:

id (integer): The ID of the service to get.
Response format: JSON

Response status codes: 200 OK, 404 Not Found

Description: Returns the service with the specified ID.

Response example:
{
    "id": 1,
    "name": "Service 1",
    "description": "Description of service 1",
    "price": 100,
    "company_id": 1
}

## Update a service by ID
URL: /services/{id}

Method: PUT

URL parameters:

id (integer): The ID of the service to update.
Request format: JSON

Request body:{
    "name": "Updated service name",
    "price": 150
}
Response format: JSON

Response status codes: 200 OK, 404 Not Found

Description: Updates the service with the specified ID.

Response example:
{
    "id": 1,
    "name": "Updated service name",
    "description": "Description of service 1",
    "price": 150,
    "company_id": 1
}

## Delete a service
URL: /services/:id

Method: DELETE

Response format: JSON

Response status codes: 204 No Content, 404 Not Found

Description: Deletes a service by its ID.

URL parameters:
id (integer): the ID of the service to delete.
Response example: {'result': True}