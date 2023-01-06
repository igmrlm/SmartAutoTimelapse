import os
import subprocess
import argparse

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfolder", help="path to the input folder")
parser.add_argument("-t", "--tvalue", help="Motion detection threshold, Numeric value 1-100")
parser.add_argument("-b", "--box", type=int, help="Size of box blur filter applied in GPU")
parser.add_argument("-y", "--yes", action="store_true", help="execute timelapse.bat without prompting")
parser.add_argument("-s", "--speedup", help="Numerical speedup multiplier for the final timelapse video, E.G. 1=1x, 10=10x")


args = parser.parse_args()

# Get the input folder from the command-line argument or ask the user for it
if args.inputfolder:
  input_folder = args.inputfolder
else:
  input_folder = input("Enter the path to the input folder: ")

# Get the -t value from the command-line argument or ask the user for it
if args.tvalue:
  t_value = args.tvalue
else:
  t_value = input("Enter a numeric value for the motion detection threshold from 1-100: ")
  
if args.speedup:
    speedx = args.speedup
else:
    speedx = float(input("Enter the speed at which to speed up the final timelapse (e.g. 2 for 2x speed) : "))
    
if args.box:
    box = args.box
else:
    box = int(input("Enter size of the desired box blur filterm E.g. 10 for 10x10: "))    

print("\nCreate Batch: speedx (Timelapse Speed Multiplier setting)")
print(speedx)

# Get a list of all the mp4 files in the input folder
mp4_files = [f for f in os.listdir(input_folder) if f.lower().endswith('.mp4')]

# Write the list of files  and the input folder to the console for debugging purposes
print("\n")
print(mp4_files)

print("\nCreate Batch: input_folder")
print(input_folder)

# Set the output path to the base directory of the input folder with spaces replaced with underscores

# Get the directory portion of the path
base_dir = os.path.basename(input_folder)

print("\nCreate Batch: base_dir:\n")
print(base_dir)

output_filename = base_dir.replace(" ", "_") + "_Timelapse_" + "Threshold_" + t_value + "_Speedup_" + speedx + "x.mp4"    

print("\nCreate Batch: Default output timelapse filename:\n")
print(output_filename)
  
# Open a text file for writing
with open('./timelapse.bat', 'w') as f:
  # Write the commands to the text file
  for file in mp4_files:
    f.write(f'python .\\ffac3_cuda.py -i "{input_folder}\\{file}" -o .\\work\\{file}_AutoTimeLapse_t{t_value}.MP4 -s .\\edit.txt -hh dxva2 -v "hevc_nvenc -rc vbr -cq 10 -qmin 6 -qmax 14" -f C:\\ffmpeg\\bin\\ffmpeg.exe -t {t_value} -k -b {box}\n')

  # Write the additional command to the text file
  f.write('python.exe .\\ffmpegAutoConcat.py -i .\work\ -f ' + output_filename + ' -s ' + speedx +'\n')

# Execute the file "timelapse.bat" if the user wants to
if args.yes or input("Execute timelapse.bat? [Y/n] ").lower() == "y":
  subprocess.run(['timelapse.bat'])
  print("Commands written to output.txt and timelapse.bat executed")
else:
  print("Commands written to output.txt")
  
  
  
  