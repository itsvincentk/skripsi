import datetime
import subprocess

# get current date and time
now = datetime.datetime.now()

# format date and time as a string
date_string = now.strftime("%Y-%m-%d-%H-%M-%S")

# create output file with date and time in the name
filename = f"output_{date_string}.txt"

# open file for writing
with open(filename, "w") as file:
    # redirect output to file using subprocess
    subprocess.run(["python", "Main.py"], stdout=file, check=True)