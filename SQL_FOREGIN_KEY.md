# Foreign key constraint

In SQL, you can specify the relationship between two tables when you create a foreign key constraint. 
The relationship can be either ON DELETE or ON UPDATE, 
and it determines what happens to the rows in the child table when the corresponding rows in the parent table are deleted or updated.

- Here are the different options for the ON DELETE and ON UPDATE clauses:

    `NO ACTION`: This is the default behavior. If you delete or update a row in the parent table, an error will be raised if there are any rows in the child table that reference the deleted or updated row.

    `CASCADE`: If you delete or update a row in the parent table, the corresponding rows in the child table will also be deleted or updated.

    `SET NULL`: If you delete a row in the parent table, the foreign key columns in the child table will be set to NULL. If you update a row in the parent table, the foreign key columns in the child table will be updated with the new values.

    `SET DEFAULT`: If you delete a row in the parent table, the foreign key columns in the child table will be set to the default values. If you update a row in the parent table, the foreign key columns in the child table will be updated with the new values.