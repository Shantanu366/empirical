from fastapi import FastAPI
from subprocess import check_output, CalledProcessError
import os
import re

app = FastAPI(title="Test Impact Engine")


# Match test names
TEST_NAME_REGEX = re.compile(
    r'^\s*(?:it|test)\s*\(\s*[\'"]([^\'"]+)[\'"]',
    re.MULTILINE
)

# for modified detection
TEST_BLOCK_REGEX = re.compile(
    r'^\s*(?:it|test)\s*\(\s*[\'"]([^\'"]+)[\'"][\s\S]*?\n\s*\)',
    re.MULTILINE
)

# ---Helper Functions----

def extract_tests(content: str):
    """Extract test names only"""
    return set(TEST_NAME_REGEX.findall(content))


def extract_test_blocks(content: str):
    """
    Extract full test blocks:
    {
        "test name": "entire test body"
    }
    """
    tests = {}
    for match in TEST_BLOCK_REGEX.finditer(content):
        name = match.group(1)
        body = match.group(0)
        tests[name] = body.strip()
    return tests


def get_file(commit: str, path: str):
    """Safely get file content from a git commit"""
    try:
        return check_output(
            ["git", "show", f"{commit}:{path}"],
            text=True
        )
    except CalledProcessError:
        return ""


# ----- API ------

@app.get("/impact")
def impact(commit: str, repo: str):
    """
    Returns a list of impacted tests for a given commit.
    """
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

        before_blocks = extract_test_blocks(before)
        after_blocks = extract_test_blocks(after)

        before_names = set(before_blocks.keys())
        after_names = set(after_blocks.keys())

        # Added tests
        for test in after_names - before_names:
            results.append({
                "test": test,
                "file": path,
                "type": "added"
            })

        # Removed tests
        for test in before_names - after_names:
            results.append({
                "test": test,
                "file": path,
                "type": "removed"
            })

        # Modified tests (same name, different body)
        for test in before_names & after_names:
            if before_blocks[test] != after_blocks[test]:
                results.append({
                    "test": test,
                    "file": path,
                    "type": "modified"
                })

    return results
