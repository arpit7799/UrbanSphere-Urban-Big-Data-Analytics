
"""
UrbanSphere - HDFS Setup via Snakebite/Subprocess
Demonstrates programmatic Hadoop interaction in Python.
"""
import subprocess

def run_cmd(cmd):
    print(f"Running: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print(f"Hadoop not found or not running. Command skipped: {cmd}")

if __name__ == "__main__":
    print("UrbanSphere programmatic HDFS initialization...")
    run_cmd("hdfs dfs -mkdir -p /urbansphere/data/processed")
    run_cmd("hdfs dfs -put data/processed/* /urbansphere/data/processed/")
    print("Done.")
