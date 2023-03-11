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
URL: /service/

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
"price": 100,        
"company_id": 1    
},    
{        
"id": 2,        
"name": "Service 2",       
"description": "Description of service 2",        
"price": 200,        
"company_id": 1    
}]
# Create a new service
URL: /service/

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
URL: /service/{id}/

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
URL: /service/{id}/

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
URL: /service/{id}/

Method: DELETE

Response format: JSON

Response status codes: 204 No Content, 404 Not Found

Description: Deletes a service by its ID.

URL parameters:
id (integer): the ID of the service to delete.
Response example: {'result': True}


# Company API
### This API provides endpoints for retrieving, updating, and deleting a specific company and adding a new company to the database.

## GET /company/<int:pk>/
This endpoint retrieves the details of a specific company and a list of its services. The company is identified by its ID (pk).

## Request parameters:

pk (int): The ID of the company to retrieve.
Returns:

#### A list containing the details of the requested company and its services, in JSON format. The fields returned for the company are:
#### id (int): The ID of the company.
#### name (str): The name of the company.
#### description (str): The description of the company.
#### website (str): The website of the company.
#### email (str): The email of the company.
#### phonenum (str): The phone number of the company.
#### photo (str): The filename of the company's photo.
#### cities (list): A list of dictionaries, each containing the ID and name of a city associated with the company.
#### services (list): A list of dictionaries, each containing the name, description, and price of a service offered by the company.
#### companies_mean (float): The average price of all services offered by the company.
If the requested company is not found, a 404 Not Found error is returned.

## PUT /company/<int:pk>/
#### This endpoint updates the details of a specific company. The company is identified by its ID (pk).

Request parameters:

#### pk (int): The ID of the company to update.
#### Request body: A JSON object containing the fields to update for the company. The following fields are available for update:
#### name (str): The name of the company.
#### description (str): The description of the company.
#### website (str): The website of the company.
#### email (str): The email of the company.
#### phonenum (str): The phone number of the company.
#### photo (file): The photo of the company. (optional)
#### cities (list): A list of city IDs associated with the company.
### Returns:

A list containing the updated details of the company, in JSON format. The fields returned are the same as for the GET method.
If the requested company is not found, a 404 Not Found error is returned. If the update is unsuccessful, a 400 Bad Request error is returned.

## DELETE /company/<int:pk>/
### This endpoint deletes a specific company. The company is identified by its ID (pk).

Request parameters:

#### pk (int): The ID of the company to delete.
### Returns:

A JSON object with a "result" field set to True if the company was successfully deleted.
If the requested company is not found, a 404 Not Found error is returned.

## GET /company/
### This endpoint retrieves a list of companies and their associated cities, based on optional query parameters.

Query parameters:

#### city (list of ints): A list of city IDs to filter the results by.
Returns:

A list containing the details of the requested companies and their cities, in JSON format. The fields returned for each company are the same as for the GET method.
If no companies match the query parameters, an empty list is returned.

## POST /company/
### Adds a new company to the database with the provided information and associated cities, and returns the newly created company in JSON format.

Request Body Parameters
#### name (required): the name of the company.
#### description (optional): the description of the company.
#### website (optional): the website URL of the company.
#### email (optional): the email address of the company.
#### phonenum (optional): the phone number of the company.
#### photo (optional): the photo of the company.
#### cities (required): a list of integers representing the city IDs associated with the company.
### Response
Returns a JSON object containing the newly created company object with its associated cities. The company object has the same fields as the response of the GET /company/ endpoint.

# Get all cities
URL: /city/

Method: GET

Response format: JSON

Response status codes: 200 OK

### Description: Returns a list of all cities in the database.

#### Response example: [
#### {
#### "id": 1,
#### "name": "City 1"
#### },
#### {
#### "id": 2,
#### "name": "City 2"
#### }]

## Add new city
### URL: /city/

### Method: POST

Request format: JSON

### JSON Parameters:

#### name (str): The name of the city.
Response format: JSON

Response status codes: 200 OK, 400 Bad Request

Description: Adds a new city to the database and returns the newly created city.

#### Response example: {
#### "id": 3,
#### "name": "City 3"
#### }

## Get a single city
### URL: /city/int:pk/

### Method: GET

### Response format: JSON

### Response status codes: 200 OK, 404 Not Found

### Parameters:

#### pk (int): The primary key of the city to get.
### Description: Returns a JSON object representing the city with the specified primary key.

#### Response example: {
#### "id": 1,
#### "name": "City 1"
#### }

## Update a single city
### URL: /city/int:pk/

### Method: PUT

### Request format: JSON

#### JSON Parameters (optional):

#### name (str): The new name of the city.
Response format: JSON

#### Response status codes: 200 OK, 404 Not Found

Parameters:

#### pk (int): The primary key of the city to update.
#### Description: Updates the city with the specified primary key and returns a JSON object representing the updated city.

#### Response example: {
#### "id": 1,
#### "name": "New City Name"
#### }

## Delete a single city
### URL: /city/int:pk/

### Method: DELETE

### Response format: JSON

#### Response status codes: 200 OK, 404 Not Found

#### Parameters:

#### pk (int): The primary key of the city to delete.
#### Description: Deletes the city with the specified primary key and returns a JSON object indicating success.

#### Response example: {"result": true}