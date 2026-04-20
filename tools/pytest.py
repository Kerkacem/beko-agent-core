def run_pytest():
    """Run pytest and return results"""
    import subprocess
    result = subprocess.run(['pytest', '-v'], 
                          capture_output=True, text=True)
    return {
        "passed": "PASS" in result.stdout,
        "output": result.stdout,
        "errors": result.stderr
    }