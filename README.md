# Invoice app

1. invoice number
1. client contact information
1. invoice contact information
1. invoice items(name, description, quantity, price)
1. total price
1. notes

## Project Setup
1. Create databse
    ```sql
    mysql> CREATE DATABASE invoice_db;
    ```

2. Create `dev.env` file in `envs` directory and set variables as in `dev.example.env` file

3. Run app using this make command
    ```shell
    make run
    ```
