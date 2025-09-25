#!/bin/bash
# Exit immediately if a command fails.
set -e

# --- Database Credentials (from GitHub Secrets) ---
DB_USER="${ORACLE_USER}"
DB_PASSWORD="${ORACLE_PASSWORD}"
DB_CONNECT_STRING="${ORACLE_CONN_STRING}"

# --- SQL Script Directory ---
SQL_DIR="sql"

# --- Verbose Header ---
echo "===================================================="
echo "  STARTING ORACLE DEPLOYMENT (VERBOSE MODE)       "
echo "===================================================="
echo "Connecting as user: ${DB_USER}"
echo "Executing all scripts in: ./${SQL_DIR}/"
echo ""

# Check if the SQL directory exists
if [ ! -d "$SQL_DIR" ]; then
    echo "❌ ERROR: SQL directory './${SQL_DIR}' not found. Exiting."
    exit 1
fi

# Loop through all .sql files and execute them
for SCRIPT in $(ls ${SQL_DIR}/*.sql | sort -V); do
    
    SCRIPT_NAME=$(basename ${SCRIPT})
    echo "----------------------------------------------------"
    echo "▶️ [RUNNING] -> Executing script: ${SCRIPT_NAME}"
    echo "----------------------------------------------------"

    # Execute the script using SQL*Plus.
    # The "-S" (silent) flag has been REMOVED to allow error reporting.
    sqlplus -L "${DB_USER}/${DB_PASSWORD}@${DB_CONNECT_STRING}" <<EOF
        -- This command is critical. It stops the script on any SQL error.
        WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK;
        
        -- These SET commands ensure maximum verbosity.
        SET ECHO ON         -- Prints the SQL code being executed.
        SET FEEDBACK ON     -- Shows results like "Table created." or "1 row selected."
        SET SERVEROUTPUT ON -- Allows you to see DBMS_OUTPUT.PUT_LINE messages.

        PROMPT Executing &SCRIPT_NAME...
        @${SCRIPT}
        COMMIT;
        exit;
EOF
    
    echo ""
    echo "✅ [SUCCESS] -> Finished script: ${SCRIPT_NAME}"
done

echo ""
echo "===================================================="
echo "    ALL SCRIPTS EXECUTED SUCCESSFULLY          "
echo "===================================================="
