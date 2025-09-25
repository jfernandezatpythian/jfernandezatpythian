CREATE OR REPLACE PACKAGE BODY emp_pkg AS

  -- dfsbdssddkdsk
  PROCEDURE hire_employee (
      p_employee_id   IN  employees.employee_id%TYPE,
      p_first_name    IN  employees.first_name%TYPE,
      p_job_title     IN  employees.job_title%TYPE,
      p_salary        IN  employees.salary%TYPE
  ) IS
  BEGIN
    INSERT INTO employees (employee_id, first_name, job_title, salary)
    VALUES (p_employee_id, p_first_name, p_job_title, p_salary);
    
    DBMS_OUTPUT.PUT_LINE('Successfully hired ' || p_first_name);
    COMMIT;
  END hire_employee;


  -- Implementation of the get_annual_salary function
  FUNCTION get_annual_salary (
      p_employee_id   IN  employees.employee_id%TYPE
  ) RETURN NUMBER IS
    v_monthly_salary  employees.salary%TYPE;
  BEGIN
    -- Select the monthly salary from the table
    SELECT salary
    INTO v_monthly_salary
    FROM employees
    WHERE employee_id = p_employee_id;

    -- Return the calculated annual salary
    RETURN v_monthly_salary * 12;

  EXCEPTION
    -- Handle cases where the employee is not found
    WHEN NO_DATA_FOUND THEN
      RETURN NULL;
  END get_annual_salary;

END emp_pkg;
/
