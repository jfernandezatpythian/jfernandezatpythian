#!/bin/bash
# Exit immediately if a command fails, ensuring the workflow stops on any error.
set -e

# --- Database Credentials (from GitHub Secrets) ---
DB_USER="${ORACLE_USER}"
DB_PASSWORD="${ORACLE_PASSWORD}"
DB_CONNECT_STRING="${ORACLE_CONN_STRING}" # e.g., your_db_host:1521/YOUR_SID

# --- SQL Script Directory ---
SQL_DIR="sql"

# --- Verbose Header ---
echo "===================================================="
echo "  STARTING ORACLE DEPLOYMENT (NO VERSION CHECK)   "
echo "===================================================="
echo "Connecting as user: ${DB_USER}"
echo "Executing all scripts in: ./${SQL_DIR}/"
echo ""

# Check if the SQL directory exists
if [ ! -d "$SQL_DIR" ]; then
    echo "❌ ERROR: SQL directory './${SQL_DIR}' not found. Exiting."
    exit 1
fi

# Loop through all .sql files in the directory and execute them unconditionally
# The 'sort -V' command ensures a natural sort order (e.g., V2 comes before V10)
for SCRIPT in $(ls ${SQL_DIR}/*.sql | sort -V); do
    
    SCRIPT_NAME=$(basename ${SCRIPT})
    echo "----------------------------------------------------"
    echo "▶️ [RUNNING] -> Executing script: ${SCRIPT_NAME}"
    echo "----------------------------------------------------"

    # Execute the script using SQL*Plus.
    # -L: Prevents re-prompting for password on connection failure.
    # -S: Silent mode, but we will control output with SET commands.
    # WHENEVER SQLERROR: This is critical. It ensures the process stops if any SQL fails.
    sqlplus -L -S "${DB_USER}/${DB_PASSWORD}@${DB_CONNECT_STRING}" <<EOF
        WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK;
        SET ECHO ON; -- This will print each SQL statement as it is executed.
        SET SERVEROUTPUT ON; -- This enables output from DBMS_OUTPUT.
        PROMPT Executing &SCRIPT_NAME...
        @${SCRIPT}
        COMMIT;
        exit;
EOF
    
    # The 'set -e' at the top of the script handles the exit on error.
    # If sqlplus returns a non-zero exit code, the script will stop here.
    
    echo ""
    echo "✅ [SUCCESS] -> Finished script: ${SCRIPT_NAME}"
done

echo ""
echo "===================================================="
echo "    ALL SCRIPTS EXECUTED SUCCESSFULLY          "
echo "===================================================="
