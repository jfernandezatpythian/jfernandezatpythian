import os
import sys
import subprocess

# --- Configuration ---
DB_USER = os.environ.get('ORACLE_USER')
DB_PASSWORD = os.environ.get('ORACLE_PASSWORD')
DB_DSN = os.environ.get('ORACLE_DSN')
SQL_DIR = "sql"

def run_deployment():
    """
    Finds all .sql files, sorts them, and executes them unconditionally
    using SQL*Plus, with detailed error reporting.
    """
    
    print("====================================================")
    print("   ORACLE DEPLOYMENT (STATELESS - RUN ALL FILES)  ")
    print("====================================================")

    if not all([DB_USER, DB_PASSWORD, DB_DSN]):
        print("❌ FATAL ERROR: Database environment variables are not set.")
        sys.exit(1)

    # 1. Get ALL files from the directory and SORT them alphabetically
    try:
        local_scripts = sorted([f for f in os.listdir(SQL_DIR) if f.endswith('.sql')])
        if not local_scripts:
            print(f"🟡 WARNING: No .sql files found in './{SQL_DIR}/'. Nothing to do.")
            sys.exit(0)
    except FileNotFoundError:
        print(f"❌ FATAL ERROR: SQL directory './{SQL_DIR}' not found.")
        sys.exit(1)

    print(f"Found {len(local_scripts)} scripts to process in execution order.")
    
    # 2. Execute each script
    for script_name in local_scripts:
        script_path = os.path.join(SQL_DIR, script_name)
        print(f"\n----------------------------------------------------")
        print(f"▶️ RUNNING: '{script_name}'")
        print(f"----------------------------------------------------")
        
        # This wrapper script runs the user's file and then checks for compilation errors
        sqlplus_script_input = f"""
            WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK;
            SET ECHO ON;
            PROMPT Executing {script_name}...
            @{script_path}
            PROMPT Checking for compilation errors...
            SHOW ERRORS;
            COMMIT;
            exit;
        """

        try:
            command = ["sqlplus", "-L", f"{DB_USER}/{DB_PASSWORD}@{DB_DSN}"]
            
            result = subprocess.run(
                command,
                input=sqlplus_script_input,
                capture_output=True,
                text=True,
                check=False
            )

            # Always print the full output for complete logs
            if result.stdout:
                print("--- SQL*Plus Output ---")
                print(result.stdout.strip())
                print("-----------------------")

            # 3. Robust Error Checking
            has_errors = False
            stdout_lower = result.stdout.lower()

            # Check for a non-zero exit code from SQL*Plus (e.g., for DDL errors)
            if result.returncode != 0:
                print(f"❌ FAILED: SQL*Plus exited with a non-zero status code ({result.returncode}).")
                has_errors = True
            
            # --- IMPROVED ERROR DETECTION LOGIC ---
            # Look for specific phrases that indicate errors, while explicitly excluding "No errors."
            if (
                "warning: package created with compilation errors." in stdout_lower or
                "errors for" in stdout_lower
            ) and "no errors." not in stdout_lower:
                print("❌ FAILED: Detected compilation errors in the SQL*Plus output.")
                has_errors = True
                
            if has_errors:
                if result.stderr:
                    print("--- Error Details (stderr) ---")
                    print(result.stderr.strip())
                    print("------------------------------")
                sys.exit(1) # Stop the entire deployment
            
            print(f"✅ SUCCESS: '{script_name}' processed.")

        except Exception as e:
            print(f"❌ An unexpected Python error occurred: {e}")
            sys.exit(1)

    print("\n====================================================")
    print("       ALL SCRIPTS PROCESSED SUCCESSFULLY      ")
    print("====================================================")


if __name__ == "__main__":
    run_deployment()
