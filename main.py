import os
import subprocess
import sys
import traceback

from dotenv import load_dotenv
from google import genai

# Create a log file in the same directory as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(SCRIPT_DIR, "sioyek_llm_log.txt")

def log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(str(message) + "\n")

def load_env():
    env_path = os.path.join(SCRIPT_DIR, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value
        return True
    return False

if __name__ == "__main__":
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("--- SCRIPT STARTED ---\n")
    log(f"Arguments: {sys.argv}")

    try:
        if len(sys.argv) < 3:
            log("Error: Not enough arguments.")
            sys.exit(1)

        SIOYEK_PATH = sys.argv[1]
        TEXT = sys.argv[2]
        log(f"Sioyek Path: {SIOYEK_PATH}")
        log(f"Selected Text: {TEXT}")

        if not load_env():
            log("Warning: .env file not found.")

        KEY = os.getenv("GEMINI_API_KEY")
        if not KEY:
            log("CRITICAL ERROR: GEMINI_API_KEY is missing.")
            sys.exit(1)
        
        log("Gemini client initializing...")
        client = genai.Client(api_key=KEY)
        
        log("Generating content...")
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=TEXT,
        )
        
        #result_text = response.text.replace("\n", " ").strip()
        log(f"Response: {response}")
	
        # send llm output to new text file
        with open("llm_output.md", 'w') as f:
            if response:
                f.write(str(response.text))
            else:
                f.write("No response from LLM.")

        # Send result back to Sioyek status bar
        # Note: set_status_string might have a length limit, but let's try.
        log("Sending result to Sioyek status bar...")
        subprocess.run(
                [SIOYEK_PATH, '--execute-command', 'set_status_string', '--execute-command-data', "Check llm_output.txt"],
            capture_output=True, 
            text=True
        )
        log("Done.")

    except Exception as e:
        log("--- CRASH REPORT ---")
        log(traceback.format_exc())
