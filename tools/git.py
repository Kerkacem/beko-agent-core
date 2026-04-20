def git_commit(message):
    """Safe git commit via subprocess"""
    import subprocess
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', message], check=True)
    return "Committed: " + message