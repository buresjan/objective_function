import meshgen.geometry as gm
import shutil
import paramiko
import os
import time
import pandas as pd
import numpy as np


def generate_geometry(x):
    offset = x[0]
    lower_angle = x[1]
    upper_angle = x[2]
    upper_flare = x[3]
    lower_flare = x[4]

    geom = gm.Geometry(
        name="junction_2d",
        resolution=4,
        num_processes=4,
        expected_in_outs={"W", "E", "S", "N"},
        offset=offset,
        lower_angle=lower_angle,
        upper_angle=upper_angle,
        upper_flare=upper_flare,
        lower_flare=lower_flare,
        h=0.005,
    )

    name_hash = geom.name_hash
    geom.generate_voxel_mesh()
    geom.save_voxel_mesh_to_text(f"{name_hash}.txt")

    return name_hash


def move_files(filename):
    for directory, prefix in zip(
        ["angle", "dimensions", "tmp", "geometry"], ["angle", "dim", "val", "geom"]
    ):
        # Source path
        source_path = f"/home/jan/objective-function/output/{prefix}_{filename}.txt"

        # Destination path
        destination_path = f"/home/jan/gp/gp3/mnt/gp3/home/bures/tnl-lbm/sim_NSE/{directory}/{prefix}_{filename}.txt"

        shutil.move(source_path, destination_path)


def create_job_submission_script(filename):
    """
    Create a job submission script based on the provided filename and output path.

    Args:
        filename (str): The filename to be used in the script.
    """
    # Read the template from the root directory
    with open("/home/jan/objective-function/job_template.sh", "r") as template_file:
        script_template = template_file.read()

    # Replace the placeholders with the actual filename
    script_content = script_template.replace("FILENAME", filename)

    # Write the script to the specified output path
    with open(f"/home/jan/objective-function/job_{filename}.sh", "w") as script_file:
        script_file.write(script_content)

    shutil.move(
        f"/home/jan/objective-function/job_{filename}.sh",
        f"/home/jan/gp/gp3/mnt/gp3/home/bures/tnl-lbm/job_{filename}.sh",
    )


def run_job(filename):
    hostname = "gp3.fjfi.cvut.cz"
    username = "bures"
    key_path = "/home/jan/.ssh/id_rsa"

    command_to_run = f"sbatch tnl-lbm/job_{filename}.sh"

    try:
        # Create an SSH client
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Load the private key
        private_key = paramiko.RSAKey.from_private_key_file(key_path)

        # Connect to the remote server
        ssh.connect(hostname, username=username, pkey=private_key)
        print(f"Connected to {hostname}")

        command = f"cd tnl-lbm/"

        # Execute the screen command
        _, _, _ = ssh.exec_command(command)

        # Execute the screen command
        stdin, stdout, stderr = ssh.exec_command(command_to_run)

        # Print the output and errors (if any)
        print("Command output:", stdout.read().decode())
        print("Command errors:", stderr.read().decode())

    finally:
        # Close the connection
        ssh.close()
        print(f"Disconnected from {hostname}")


def monitor_directory(filename, directory="/home/jan/gp/gp3/mnt/gp3/home/bures/tnl-lbm/sim_NSE/results/"):
    """
    Monitors a directory until a specified .txt file appears, processes the file using the provided function, and ends.

    Parameters:
        filename (str): Name of the target .txt file to wait for.
        directory (str): Path to the directory to monitor.

    Returns:
        None
    """
    target_file = f"val_{filename}.txt"
    value = 0
    if not os.path.isdir(directory):
        raise ValueError(f"The directory '{directory}' does not exist.")

    print(f"Monitoring directory '{directory}' for file '{target_file}'...")

    while True:
        file_path = os.path.join(directory, target_file)

        if os.path.isfile(file_path):
            print(f"File '{target_file}' found! Processing...")
            try:
                data = pd.read_csv(
                    file_path,
                    delim_whitespace=True,
                    header=None,
                    names=[
                        "Time",
                        "Stress(1)",
                        "KE",
                        "TKE",
                        "Outflow LPA",
                        "Outflow RPA",
                        "Stress(2)",
                        "Stress(3)",
                        "Stress(Tot)",
                    ],
                )
                value = data[data["Time"] > 7.5]["Stress(2)"].mean()
            except Exception as e:
                print(f"An error occurred while processing the file: {e}")
            return value

        print(f"File '{target_file}' not found. Waiting for 1 minute...")
        time.sleep(60)


def objective_nd(x):
    offset = x[0]
    lower_angle = x[1]
    upper_angle = x[2]
    upper_flare = x[3]
    lower_flare = x[4]

    if offset > 1.0:
        return np.array([1e9])
    if offset < -1.0:
        return np.array([1e9])
    if lower_angle < -25.0:
        return np.array([1e9])
    if lower_angle > 25.0:
        return np.array([1e9])
    if upper_angle < -25.0:
        return np.array([1e9])
    if upper_angle > 25.0:
        return np.array([1e9])
    if upper_flare < 0.0:
        return np.array([1e9])
    if upper_flare > 0.0025:
        return np.array([1e9])
    if lower_flare < 0.0:
        return np.array([1e9])
    if lower_flare > 0.0025:
        return np.array([1e9])

    name_hash = generate_geometry(x)
    move_files(name_hash)
    create_job_submission_script(name_hash)
    run_job(name_hash)
    value = monitor_directory(name_hash)

    return np.array([value])


if __name__ == "__main__":
    pass
