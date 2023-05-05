# Invoice app
This is an invoice demo project template that uses FastAPI, Alembic and async SQLModel as ORM.
It shows a complete async CRUD template with multiple relationships between one table.

## Database design
![Database Design](https://user-images.githubusercontent.com/48521608/236441859-75ebd98d-3e4c-421b-b435-eee04a785188.png)

## FastAPI Swagger UI
![FastAPI Swagger UI](https://user-images.githubusercontent.com/48521608/236441920-81341e69-c6e6-439c-9439-77ca96ba585c.png)

## Features
1. invoice number
1. client contact information
1. invoice contact information
1. invoice items(name, description, quantity, price)
1. total price
1. multiple notes on each invoice

## Project Setup
1. Create database
    ```sql
    mysql> CREATE DATABASE invoice_db;
    ```

1. Create a `dev.env` file in the `envs` directory and set variables as in the `dev.example.env` file

1. Run the app using this make command
    ```shell
    make run
    ```
1. Run Super admin APIs
    - Create database
    - Upgrade migration to head

1. Done!, give a try to call APIs right from swagger

