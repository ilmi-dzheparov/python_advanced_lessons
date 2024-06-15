import subprocess

import wc


def process_count(username: str) -> int:
    result = subprocess.run(
        ["pgrep", "-u", username, "-c"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.stderr:
        print(f"Error: {result.stderr}")
        return 0

    return int(result.stdout)


def total_memory_usage(root_pid: int) -> float:
    result = subprocess.run(
        ["ps", "-p", str(root_pid), "--ppid", str(root_pid), "-o", "pmem"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print(result.stdout)

    if result.stderr:
        print(f"Error: {result.stderr}")
        return 0

    pmems = [float(item) for item in result.stdout.strip().split("\n ")[1:]]
    memory_usage = round(sum(pmems), 2)
    # print(memory_usage)

    return memory_usage
