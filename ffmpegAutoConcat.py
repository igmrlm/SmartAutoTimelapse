import os
import subprocess
import argparse

# Parse the command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputfolder", help="path to the input folder")
parser.add_argument("-f", "--filename", help="Output file name")
parser.add_argument("-s", "--speedup", help="amount to speed up the video")

# parser.add_argument("-y", "--yes", action="store_true", help="execute timelapse.bat without prompting")
args = parser.parse_args()

def concatenate_files(folder_path):
    # Create a list of all the file paths in the specified folder
    file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path)]

    # Write the list of file paths to the file mylist.txt, with each line prepended with "file " and the path wrapped in single quotes
    with open("mylist.txt", "w") as file:
        file.write("\n".join(['file \'' + path + '\'' for path in file_paths]))
  
    # Use ffmpeg to concatenate the files
    concat_command = (["c:\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-f", "concat", "-safe", "0", "-i", "mylist.txt", "-c:v", "copy", "-an", "temp_output_delete_me.mp4"])
    print("\n\n************\n")
    print("Starting nate's automagical automatica timelapse generator! https://YouTube.com/NathanaelNewton")
    print("NOW Executing the following ffmpeg command:\n")
    print(concat_command)
    if args.inputfolder:
       print(f"Input folder: {args.inputfolder}")
    if args.speedup:
       print(f"Speedup multiplier: {args.speedup}")
    
    print("\n\n************\n")
    
    subprocess.run(concat_command)


def create_time_lapse(input_path, output_path, speed):
    # Use ffmpeg to create a time lapse of the input video
    time_lapse_command = (["c:\\ffmpeg\\bin\\ffmpeg.exe", "-y", "-hwaccel", "dxva2", "-i", input_path, "-vf", f"setpts={1 / speed}*PTS", "-vcodec", "hevc_nvenc", "-rc", "vbr", "-cq", "10", "-qmin", "6", "-qmax", "14", "-r", "60", output_path])
    
    print("\n\n************\nNOW Executing the following ffmpeg command:\n")
    print(time_lapse_command)
    print("\n\n************\n")
    subprocess.run(time_lapse_command)

if __name__ == "__main__":
    if args.inputfolder:
      folder_path_response = args.inputfolder
    else:
      folder_path_response = input("Enter the path to the input folder: ")

    # Concatenate the files
    folder_path = folder_path_response
    concatenate_files(folder_path)
    
    # Set the default input and output paths to the current directory
    input_path = "temp_output_delete_me.mp4"
    
    # Ask the user the speedup value if not in the commandline execution options
    
    if args.speedup:
      speed = float(args.speedup)
    else:
      speed = float(input("Enter the speed at which to speed up the final timelapse (e.g. 2 for 2x speed) : "))

    if args.filename:
        print("Default Name:\n")
        print(args.filename)
        output_path = args.filename
    
    output_path_response = input("\n\n************\nEnter the path for the output video (press Enter for default): ")
    if output_path_response:
        output_path = output_path_response

    # Create the time lapse
    create_time_lapse(input_path, output_path, speed)