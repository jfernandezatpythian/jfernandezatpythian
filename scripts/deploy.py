import os
import sys
import subprocess

# --- Database Credentials (from GitHub Secrets) ---
DB_USER = os.environ.get('ORACLE_USER')
DB_PASSWORD = os.environ.get('ORACLE_PASSWORD')
DB_DSN = os.environ.get('ORACLE_DSN')

def run_deployment(scripts_to_run):
    """Executes a specific list of SQL scripts using SQL*Plus."""
    
    print("====================================================")
    print("      ORACLE MIGRATION (CHANGED FILES ONLY)       ")
    print("====================================================")

    # Validate that credentials are set
    if not all([DB_USER, DB_PASSWORD, DB_DSN]):
        print("❌ FATAL ERROR: Database environment variables are not set.")
        sys.exit(1)

    # Execute each script passed as an argument
    for script_path in scripts_to_run:
        script_name = os.path.basename(script_path)
        print(f"\n----------------------------------------------------")
        print(f"▶️ RUNNING: '{script_name}' from path '{script_path}'")
        print(f"----------------------------------------------------")
        
        command = [
            "sqlplus",
            "-L",
            f"{DB_USER}/{DB_PASSWORD}@{DB_DSN}",
            f"@{script_path}"
        ]

        try:
            result = subprocess.run(
                command, capture_output=True, text=True, check=False
            )

            if result.stdout:
                print("--- SQL*Plus Output ---")
                print(result.stdout.strip())
                print("-----------------------")

            if result.returncode != 0:
                print(f"❌ FAILED: Script '{script_name}' exited with an error.")
                if result.stderr:
                    print("--- Error Details (stderr) ---")
                    print(result.stderr.strip())
                    print("------------------------------")
                sys.exit(1)
            
            print(f"✅ SUCCESS: '{script_name}' executed successfully.")

        except FileNotFoundError:
            print("❌ FATAL ERROR: 'sqlplus' not found. Is Oracle Client installed and in the PATH?")
            sys.exit(1)
        except Exception as e:
            print(f"❌ An unexpected Python error occurred: {e}")
            sys.exit(1)

    print("\n====================================================")
    print("       ALL CHANGED SCRIPTS PROCESSED SUCCESSFULLY      ")
    print("====================================================")


if __name__ == "__main__":
    # The script now reads file paths from command-line arguments
    # sys.argv[0] is the script name itself, so we skip it.
    files_from_cli = sys.argv[1:]
    
    if not files_from_cli:
        print("🟡 No new or modified SQL files detected in this push. Nothing to deploy.")
        sys.exit(0)
    
    run_deployment(files_from_cli)
