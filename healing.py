import subprocess

def fix_failed_script(script_path):
    error = subprocess.run(f"python {script_path}", capture_output=True).stderr
    fix_prompt = f"Fix this Python script: {error}\n{open(script_path).read()}"
    fixed_code = think(fix_prompt)
    with open(script_path, "w") as f:
        f.write(fixed_code)