This code is a Python script that creates a batch file called "timelapse.bat". The batch file will contain a series of commands that can be used to create a timelapse video from a series of input video files.
The script begins by importing three libraries: os, subprocess, and argparse. These libraries are used for working with the operating system, running external programs, and parsing command-line arguments, respectively.
Next, the script sets up an ArgumentParser object to parse command-line arguments that can be passed to the script. There are five possible arguments that can be passed:
-i or --inputfolder: the path to the input folder containing the video files that will be used to create the timelapse.
-t or --tvalue: the motion detection threshold for the timelapse, which should be a numeric value between 1 and 100.
-b or --box: the size of the box blur filter applied to the video files in the GPU. This should be an integer value.
-y or --yes: a flag that tells the script to execute the timelapse.bat file without prompting the user for confirmation.
-s or --speedup: a numerical multiplier for the speed at which the final timelapse video will play. For example, a value of 10 would result in a timelapse video that plays 10 times faster than normal.
The script then uses the parse_args() method of the ArgumentParser object to parse the command-line arguments and store them in a variable called "args".
The script then checks if the -i or --inputfolder argument was passed. If it was, the input folder is set to the value of the argument. If not, the script prompts the user to enter the path to the input folder.
Similarly, the script checks for the -t or --tvalue argument and prompts the user for a value if it was not passed. The same process is repeated for the -s or --speedup and -b or --box arguments.
The script then prints the value of the speedup multiplier to the console for debugging purposes.
Next, the script uses a list comprehension to get a list of all the mp4 files in the input folder. It then prints the list of files and the input folder to the console for debugging purposes.
The script then sets the output path for the timelapse video to the base directory of the input folder, with spaces replaced with underscores. It also creates a default output filename for the timelapse video based on the motion detection threshold, speedup multiplier, and input folder name.
The script then opens a text file called "timelapse.bat" for writing and writes a series of commands to the file. These commands use the Python script "ffac3_cuda.py" to process the input video files and create timelapse versions of them. The commands also use the Python script "ffmpegAutoConcat.py" to concatenate the timelapse videos into a single timelapse video.
Finally, the script checks if the -y or --yes argument was passed or if the user confirms that they want to execute the timelapse.bat file. If either of these conditions is true, the script uses the subprocess library to run the timelapse.bat file.
To use this code, you would need to pass the appropriate command-line arguments to the script. For example, you could run the script with the following command:
python create_batch.py -i "C:\input_folder" -t 50 -b 10 -y -s 2
This would run the script with the input folder set to "C:\input_folder", the motion detection threshold set to 50, the box blur filter size set to 10, the yes flag set to true (so the timelapse.bat file will be executed without prompting), and the speedup multiplier set to 2. The script would then create the timelapse.bat file and execute it, creating a timelapse video from the input video files in the specified input folder with a motion detection threshold of 50, a box blur filter size of 10, and a speedup multiplier of 2.
 
 
 
 
 
ffac3_cuda.py
This code is a Python script that processes a video file and creates a timelapse version of it based on motion detection. It uses the OpenCV library and the CUDA hardware acceleration API to process the video file in parallel on a GPU.
The script begins by setting the environment variable "OPENCV_CUDA_BACKEND" to "cuda" and importing several libraries, including os, cv2, numpy, argparse, subprocess, and tqdm. These libraries are used for working with the operating system, performing image processing with OpenCV, working with numerical data in Python, parsing command-line arguments, running external programs, and displaying progress bars, respectively.
The script then initializes the GPU and sets the active CUDA device to the first device on the system. It also gets the device properties and stores them in a variable called "device_info".
Next, the script sets up an ArgumentParser object to parse command-line arguments that can be passed to the script. There are nine possible arguments that can be passed:
-i or --input: the path to the input video file that will be processed. This argument is required.
-k or --show_thumbnail: a flag that tells the script to show a thumbnail image of the frame currently being processed.
-vv or --verbose: a flag that tells the script to print verbose output to the console.
-o or --output: the path to the output video file. This argument is required.
-s or --edit: the path to the output edit script file. This argument is required.
-f or --ffmpeg: the path to the ffmpeg executable. The default value is "c:\ffmpeg\bin\ffmpeg.exe".
-hh or --hwaccel: the hardware encoder to use. The default value is "cuda".
-v or --vcodec: the video codec to use. The default value is "h264".
-t or --threshold: the relative motion threshold for the timelapse, which should be a numeric value between 0 and 100. The default value is 15.
-b or --box: the size of the box blur filter applied to the video file in the GPU. This should be an integer value. The default value is 10.
The script then uses the parse_args() method of the ArgumentParser object to parse the command-line arguments and store them in a variable called "args". It also sets a flag called "verbose" based on the value of the -vv or --verbose argument.
The script then opens the input video file using the cv2.VideoCapture() function and gets the video properties, including the frame rate, resolution, and number of frames.
Next, the script calculates the absolute motion threshold based on the relative threshold specified by the user. It then prints the GPU device properties, input video properties, and motion threshold to the console for debugging purposes.
The script then creates an empty list called "timestamps" that will be used to store the timestamps of the frames that are selected for the timelapse.
The script then enters a loop to process each frame of the video file. It uses the cv2.cuda_GpuMat() function to create a GPU memory buffer for the current frame and the cv2.cuda_GpuMat() function to create a GPU memory buffer for the previous frame. The script then calculates the absolute difference between the current frame and the previous frame using the cv2.cuda.absdiff() function and stores the result in a GPU memory buffer called "delta".
The script then converts the delta frame to grayscale using the cv2.cuda.cvtColor() function and applies a box blur filter to it using the cv2.cuda.boxFilter() function. It then calculates the total motion in the frame by summing the pixel values of the filtered frame and compares it to the motion threshold. If the total motion is above the threshold, the script stores the current timestamp in the "timestamps" list and increments a counter called "num_frames_selected".
If the -k or --show_thumbnail flag is set, the script displays a thumbnail image of the current frame.
The script then updates the "previous_frame" buffer with the current frame using the cv2.cuda.copy() function and increments the frame counter.
After the loop is finished, the script calculates the elapsed time of the video by dividing the total number of frames by the frame rate. It then calculates the desired frame rate for the timelapse video based on the number of selected frames and the elapsed time of the video.
The script then opens a text file for writing and writes the commands to create the timelapse video using ffmpeg. The commands include using the -ss and -t options to specify the start and end times of each selected frame, and the -r option to set the frame rate of the output video.
Finally, the script closes the video file, the text file, and the GUI window (if it was opened). It then runs the ffmpeg command using the subprocess.run() function to create the timelapse video.
 
 
 
 
Ffmpegautoconcat.py
The script starts by parsing the command-line arguments using the argparse module. It has three arguments:
-i or --inputfolder: The path to the input folder containing the video files to be concatenated.
-f or --filename: The name of the output file.
-s or --speedup: The speedup multiplier for the timelapse video.
The script then defines a function called concatenate_files() that takes in a folder path and concatenates the video files in that folder using ffmpeg. It first creates a list of file paths for all the files in the specified folder using the os.listdir() function and the os.path.join() function. It then writes the list of file paths to a file called "mylist.txt", with each line prepended with "file " and the path wrapped in single quotes.
The script then uses ffmpeg to concatenate the files using the -f, -i, and -c:v options and stores the result in a temporary file called "temp_output_delete_me.mp4".
The script then defines a function called create_time_lapse() that takes in an input path, an output path, and a speedup multiplier and creates a timelapse video of the input video using ffmpeg. It uses the -i, -vf, -vcodec, and -r options to specify the input file, the video filter, the video codec, and the frame rate, respectively.
In the main block of the script, the script asks the user for the input folder path if it was not passed as a command-line argument and calls the concatenate_files() function with the folder path. It then sets the default input and output paths to the current directory and asks the user for the speedup multiplier if it was not passed as a command-line argument.
If the user specified an output file name as a command-line argument, the script sets the output path to that file name. If not, it asks the user for an output file path. It then calls the create_time_lapse() function with the input path, output path, and speedup multiplier.
Finally, the script deletes the temporary file "temp_output_delete_me.mp4" and the file "mylist.txt".
To use this code, you would need to pass the appropriate command-line arguments to the script. For example, you could run the script with the following command:
python ffmpegAutoConcat.py -i path/to/input/folder -f output_filename -s speedup_multiplier
This would concatenate the video files in the specified input folder, create a timelapse video of the concatenated video with the specified speedup multiplier, and save the result to a file with the specified output file name.
