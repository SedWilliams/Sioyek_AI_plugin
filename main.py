import os
import subprocess
import sys

from google import genai

if __name__=="__main__":
    SIOYEK_PATH = sys.argv[1]
    KEY = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=KEY)
    TEXT = sys.argv[2]
    
    response = client.models.generate_content(
            model="gemini-3.1-pro",
            contents=TEXT,
    )

    subprocess.run([sioyek_path, '--execute-command', 'set_status_string', '--execute-command-data', response.text])

