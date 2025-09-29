import os
import sys
import subprocess

# --- Configuration ---
DB_USER = os.environ.get('ORACLE_USER')
DB_PASSWORD = os.environ.get('ORACLE_PASSWORD')
DB_DSN = os.environ.get('ORACLE_DSN')

def run_deployment(scripts_to_run):
    """
    Executes a specific list of SQL scripts using SQL*Plus,
    with detailed error reporting for only the provided files.
    """
    
    print("====================================================")
    print("   ORACLE DEPLOYMENT (MODIFIED FILES ONLY)        ")
    print("====================================================")

    if not all([DB_USER, DB_PASSWORD, DB_DSN]):
        print("❌ FATAL ERROR: Database environment variables (ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN) are not set.")
        sys.exit(1)

    # Ensure the provided scripts are sorted by name for dependency order
    # (e.g., 01_table.sql before 02_package.sql)
    sorted_scripts = sorted(scripts_to_run)
    
    if not sorted_scripts:
        print("🟡 No SQL files provided to the deployment script. Nothing to do.")
        sys.exit(0)

    print(f"Detected {len(sorted_scripts)} modified/new scripts to process in execution order:")
    for script in sorted_scripts:
        print(f"  - {script}")
    
    # Execute each script
    for script_path in sorted_scripts:
        # Validate that the file actually exists (security/robustness check)
        if not os.path.exists(script_path):
            print(f"❌ FATAL ERROR: Script path '{script_path}' provided but file not found. Exiting.")
            sys.exit(1)

        script_name = os.path.basename(script_path)
        print(f"\n----------------------------------------------------")
        print(f"▶️ RUNNING: '{script_name}' from path '{script_path}'")
        print(f"----------------------------------------------------")
        
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

            if result.stdout:
                print("--- SQL*Plus Output ---")
                print(result.stdout.strip())
                print("-----------------------")

            # Robust Error Checking
            has_errors = False
            stdout_lower = result.stdout.lower()

            if result.returncode != 0:
                print(f"❌ FAILED: SQL*Plus exited with a non-zero status code ({result.returncode}).")
                has_errors = True
            
            # Look for specific phrases that indicate errors, while explicitly excluding "No errors."
            if (
                "warning: package created with compilation errors." in stdout_lower or
                "errors for" in stdout_lower # This covers packages, procedures, functions, views, etc.
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
    print("       ALL MODIFIED SCRIPTS PROCESSED SUCCESSFULLY      ")
    print("====================================================")


if __name__ == "__main__":
    # Get the list of files passed as command-line arguments
    # sys.argv[0] is the script name itself, so we slice from index 1.
    files_from_cli = sys.argv[1:]
    
    if not files_from_cli:
        print("🟡 No SQL files were passed to the deployment script. This means no relevant changes were detected by Git.")
        sys.exit(0)
    
    run_deployment(files_from_cli)
