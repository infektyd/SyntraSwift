import subprocess

def query_mistral(prompt):
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode("utf-8"),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=60
        )
        output = result.stdout.decode("utf-8").strip()
        return output
    except Exception as e:
        return f"[MISTRAL_ERROR] {e}"
