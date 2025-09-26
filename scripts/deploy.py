import os
import sys
import subprocess

# --- Database Credentials (from GitHub Secrets) ---
DB_USER = os.environ.get('ORACLE_USER')
DB_PASSWORD = os.environ.get('ORACLE_PASSWORD')
DB_DSN = os.environ.get('ORACLE_DSN')  # e.g., your_db_host:1521/YOUR_SID

def run_deployment(scripts_to_run):
    """Executes a specific list of SQL scripts and shows compilation errors."""
    
    print("====================================================")
    print("      ORACLE MIGRATION (WITH DEBUGGING)         ")
    print("====================================================")

    if not all([DB_USER, DB_PASSWORD, DB_DSN]):
        print("❌ FATAL ERROR: Database environment variables are not set.")
        sys.exit(1)

    for script_path in scripts_to_run:
        script_name = os.path.basename(script_path)
        print(f"\n----------------------------------------------------")
        print(f"▶️ RUNNING: '{script_name}' from path '{script_path}'")
        print(f"----------------------------------------------------")
        
        # We now pass a multi-line script to SQL*Plus's standard input
        # This includes the original script execution AND the SHOW ERRORS command
        sqlplus_script_input = f"""
            WHENEVER SQLERROR EXIT SQL.SQLCODE ROLLBACK;
            PROMPT Executing {script_name}...
            @{script_path}
            PROMPT Checking for compilation errors...
            SHOW ERRORS;
            COMMIT;
            exit;
        """

        try:
            # The command no longer includes the @script, as we are piping the commands in
            command = ["sqlplus", "-L", f"{DB_USER}/{DB_PASSWORD}@{DB_DSN}"]
            
            result = subprocess.run(
                command,
                input=sqlplus_script_input, # Pass our wrapper script via standard input
                capture_output=True,
                text=True,
                check=False
            )

            # Print all output so you see both the execution and the errors
            if result.stdout:
                print("--- SQL*Plus Output ---")
                print(result.stdout.strip())
                print("-----------------------")

            # Check for SQL*Plus returning an error code OR if the output contains "compilation errors"
            if result.returncode != 0 or "errors" in result.stdout.lower():
                print(f"❌ FAILED: Script '{script_name}' likely has compilation errors.")
                # The detailed error should already be in the stdout from SHOW ERRORS
                if result.stderr:
                    print("--- Error Details (stderr) ---")
                    print(result.stderr.strip())
                    print("------------------------------")
                sys.exit(1)
            
            print(f"✅ SUCCESS: '{script_name}' executed successfully.")

        except Exception as e:
            print(f"❌ An unexpected Python error occurred: {e}")
            sys.exit(1)

    print("\n====================================================")
    print("       ALL CHANGED SCRIPTS PROCESSED SUCCESSFULLY      ")
    print("====================================================")


if __name__ == "__main__":
    files_from_cli = sys.argv[1:]
    if not files_from_cli:
        print("🟡 No new or modified SQL files detected. Nothing to deploy.")
        sys.exit(0)
    run_deployment(files_from_cli)
