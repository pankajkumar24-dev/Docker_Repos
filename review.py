import os
import subprocess
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_changed_files():
    subprocess.run("git fetch origin main", shell=True)
    result = subprocess.check_output(
        "git diff --name-only origin/main",
        shell=True
    ).decode("utf-8")
    return result.splitlines()

def read_code(files):
    code = ""
    for file in files:
        if file.endswith(".py"):
            try:
                with open(file, "r") as f:
                    code += f"\n\nFile: {file}\n{f.read()}"
            except:
                pass
    return code

files = get_changed_files()
code_content = read_code(files)

prompt = f"""
You are a senior DevOps engineer.

Review the following Python code and provide:
1. Bugs
2. Code improvements
3. Best practices
4. Security issues (if any)

Code:
{code_content}
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

review_text = response.choices[0].message.content

print(review_text)

with open("review.txt", "w") as f:
    f.write(review_text)
