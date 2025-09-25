#!/bin/bash
# Exit immediately if a command exits with a non-zero status.
set -e

# --- Database Credentials ---
# In GitHub Actions, these will be set as environment variables from secrets.
DB_USER="${ORACLE_USER}"
DB_PASSWORD="${ORACLE_PASSWORD}"
DB_CONNECT_STRING="${ORACLE_CONN_STRING}" # e.g., your_db_host:1521/YOUR_SID

# --- SQL Script Directory ---
SQL_DIR="sql"

echo "Starting database deployment..."

# Loop through all .sql files in the specified directory
for SCRIPT in $(ls ${SQL_DIR}/*.sql | sort -V); do
    
    SCRIPT_NAME=$(basename ${SCRIPT})
    echo "----------------------------------------------------"
    echo "Processing script: ${SCRIPT_NAME}"

    # Check if the script has already been run by querying our history table
    # The 'SET' commands ensure we only get the count number as output
    COUNT=$(sqlplus -S "${DB_USER}/${DB_PASSWORD}@${DB_CONNECT_STRING}" <<EOF
        SET HEADING OFF FEEDBACK OFF PAGESIZE 0;
        SELECT count(*) FROM system.deployment_history WHERE script_name = '${SCRIPT_NAME}';
        exit;
EOF
    )

    # Trim whitespace from the COUNT variable
    COUNT=$(echo ${COUNT} | xargs)

    # If the count is 0, the script has not been run yet
    if [ "${COUNT}" -eq "0" ]; then
        echo "-> New script. Executing..."

        # Execute the script using SQL*Plus.
        # "WHENEVER SQLERROR" ensures the script will exit on any error.
        sqlplus -S "${DB_USER}/${DB_PASSWORD}@${DB_CONNECT_STRING}" <<EOF
            WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK;
            @${SCRIPT}
            INSERT INTO system.deployment_history (script_name) VALUES ('${SCRIPT_NAME}');
            COMMIT;
            exit;
EOF
        echo "-> SUCCESS: ${SCRIPT_NAME} applied and recorded."
    else
        echo "-> SKIPPED: ${SCRIPT_NAME} has already been applied."
    fi
done

echo "----------------------------------------------------"
echo "Database deployment finished successfully."
