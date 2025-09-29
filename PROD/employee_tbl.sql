CREATE TABLE employees5 (
    employee_id NUMBER PRIMARY KEY,
    first_name VARCHAR2(50),
    job_title VARCHAR2(50)
);

--changeset yourname:2
CREATE VIEW vw_dummy_data5 AS
SELECT 
    'Hello World' AS message,
    123           AS sample_number,
    SYSDATE       AS current_timestamp
FROM 
    dual;
