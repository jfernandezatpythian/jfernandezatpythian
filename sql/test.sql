CREATE OR REPLACE PACKAGE emp_pkg2 AS

  /*TmodifMODIFICATION OF THIS TEXT NOWdd
   * Adds a new employee to the employees table.
   * @param p_employee_id The new employee's ID.
   * @param p_first_name  The new employee's first name.
   * @param p_job_title   The new employee's job title.
   * @param p_salary      The new employee's monthly salary.
   */
  PROCEDURE hire_employee (
      p_employee_id   IN  system.employees.employee_id%TYPE,
      p_first_name    IN  system.employees.first_name%TYPE,
      p_job_title     IN  system.employees.job_title%TYPE,
      p_salary        IN  system.employees.salary%TYPE
  );

  /**
   * Calculates the annual salary for a given employee.
   * @param p_employee_id The ID of the employee.
   * @return The calculated annual salary (salary * 12).
   */
  FUNCTION get_annual_salary (
      p_employee_id   IN  system.employees.employee_id%TYPE
  ) RETURN NUMBER;

END emp_pkg2;
/
