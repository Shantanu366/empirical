from fastapi import FastAPI
from subprocess import check_output, CalledProcessError
import os
import re

app = FastAPI(title="Test Impact Engine")

def extract_tests(content: str):
    return set(re.findall(r'test\s*\(\s*[\'"](.*?)[\'"]', content))

def get_file(commit, path):
    try:
        return check_output(
            ["git", "show", f"{commit}:{path}"],
            text=True
        )
    except CalledProcessError:
        return ""

@app.get("/impact")
def impact(commit: str, repo: str):
    os.chdir(repo)

    files = check_output(
        ["git", "show", commit, "--name-status"],
        text=True
    ).splitlines()

    results = []

    for line in files:
        status, path = line.split("\t")

        if not path.endswith(".spec.ts"):
            continue

        before = get_file(f"{commit}^", path)
        after = get_file(commit, path)

        before_tests = extract_tests(before)
        after_tests = extract_tests(after)

        for t in after_tests - before_tests:
            results.append({"test": t, "file": path, "type": "added"})

        for t in before_tests - after_tests:
            results.append({"test": t, "file": path, "type": "removed"})

        for t in before_tests & after_tests:
            results.append({"test": t, "file": path, "type": "modified"})

    return results
