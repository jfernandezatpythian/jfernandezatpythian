import os
import sys
import subprocess

# --- Database Credentials (from GitHub Secrets) ---
DB_USER = os.environ.get('ORACLE_USER')
DB_PASSWORD = os.environ.get('ORACLE_PASSWORD')
DB_DSN = os.environ.get('ORACLE_DSN')  # e.g., your_db_host:1521/YOUR_SID

# --- SQL Script Directory ---
SQL_DIR = "sql"

def run_deployment():
    """Finds and executes all SQL scripts using SQL*Plus, capturing output."""
    
    print("====================================================")
    print("  STARTING ORACLE DEPLOYMENT (UNCONDITIONAL RUN)  ")
    print("====================================================")

    # Validate that credentials are set
    if not all([DB_USER, DB_PASSWORD, DB_DSN]):
        print("❌ FATAL ERROR: Database environment variables (ORACLE_USER, ORACLE_PASSWORD, ORACLE_DSN) are not set.")
        sys.exit(1)

    # Find all .sql files and sort them to ensure a consistent execution order
    try:
        local_scripts = sorted([f for f in os.listdir(SQL_DIR) if f.endswith('.sql')])
        if not local_scripts:
            print(f"🟡 WARNING: No .sql files found in './{SQL_DIR}/'. Nothing to do.")
            sys.exit(0)
    except FileNotFoundError:
        print(f"❌ FATAL ERROR: SQL directory './{SQL_DIR}' not found.")
        sys.exit(1)

    # Execute each script
    for script_name in local_scripts:
        script_path = os.path.join(SQL_DIR, script_name)
        print(f"\n----------------------------------------------------")
        print(f"▶️ RUNNING: '{script_name}'")
        print(f"----------------------------------------------------")
        
        # Construct the command to execute. The @ tells SQL*Plus to run a script.
        command = [
            "sqlplus",
            "-L",  # Prevents re-prompting for password on connection failure
            f"{DB_USER}/{DB_PASSWORD}@{DB_DSN}",
            f"@{script_path}"
        ]

        try:
            # Execute the command, capturing all output
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=False  # We check the return code manually for better error reporting
            )

            # Always print the standard output for full visibility
            if result.stdout:
                print("--- SQL*Plus Output ---")
                print(result.stdout.strip())
                print("-----------------------")

            # Check if the command failed
            if result.returncode != 0:
                print(f"❌ FAILED: Script '{script_name}' exited with an error.")
                # The detailed Oracle error is usually in stderr or stdout
                if result.stderr:
                    print("--- Error Details (stderr) ---")
                    print(result.stderr.strip())
                    print("------------------------------")
                sys.exit(1)  # Stop the entire deployment
            
            print(f"✅ SUCCESS: '{script_name}' executed successfully.")

        except FileNotFoundError:
            print("❌ FATAL ERROR: 'sqlplus' command not found. Is the Oracle Client installed and in the PATH?")
            sys.exit(1)
        except Exception as e:
            print(f"❌ An unexpected Python error occurred: {e}")
            sys.exit(1)

    print("\n====================================================")
    print("       ALL SCRIPTS PROCESSED SUCCESSFULLY       ")
    print("====================================================")


if __name__ == "__main__":
    run_deployment()
