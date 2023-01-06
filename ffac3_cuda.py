import os
os.environ['OPENCV_CUDA_BACKEND'] = 'cuda'
import cv2
import numpy as np
import argparse
import subprocess
import tqdm

# Ensure that the GPU is initialized
cv2.cuda.setDevice(0)

# Get the active CUDA device
device = cv2.cuda.getDevice()

# Get the device properties
device_info = cv2.cuda.DeviceInfo(device)

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True, help="path to input video file")
ap.add_argument("-k", "--show_thumbnail", action="store_true",
                help="show a thumbnail image of the frame currently being processed")
ap.add_argument("-vv", "--verbose", action="store_true", help="Print verbose output")
ap.add_argument("-o", "--output", required=True, help="path to output video file")
ap.add_argument("-s", "--edit", required=True, help="path to output edit script file")
ap.add_argument("-f", "--ffmpeg", type=str, default="c:\ffmpeg\bin\ffmpeg.exe", help="path to ffmpeg executable")
ap.add_argument("-hh", "--hwaccel", type=str, default="cuda", help="hardware encoder to use")
ap.add_argument("-v", "--vcodec", type=str, default="h264", help="video codec to use")
ap.add_argument("-t", "--threshold", type=float, default=15.0, help="relative motion threshold (0-100)")
ap.add_argument("-b", "--box", type=int, default=10, help="Size of box blur filter applied in GPU")


args = vars(ap.parse_args())

# Set the verbose flag
verbose = (args["verbose"])
filepath = (args["input"])
rawfilepath = (f"\"{filepath}\"")
filename = os.path.basename(filepath)
# Open the video file
video = cv2.VideoCapture(args["input"])

# Initialize the box filter size

if args["box"]:
    box_size = (args["box"])
else:
    box_size = 10

# Get the video properties

fps = video.get(cv2.CAP_PROP_FPS)
width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# Calculate the absolute threshold based on the relative threshold specified by the user
relative_threshold = args["threshold"]
threshold = args["threshold"] / 10.0 * 570 * 320

print("\n\n************************************************************\n")
print(f"Starting nate's automagical motion detection editor program! https://YouTube.com/NathanaelNewton")
print("\n************************************************************\n")
# Print the GPU device properties
print("Active CUDA device:", device)
print("Total memory:", device_info.totalMemory() / (1024**2), "MB")
print("\n************************************************************\n")


print(f"Now processing {filepath}")
print(f"If the code worked this path has quotes on it! {rawfilepath}")
print(f"The input video is {fps} frames per second")
print(f"The resolution is {width}x{height}")
print(f"The total number of frames in the video is: {num_frames}")
print("\n************************************************************\n")
print(f"The relative threshold of {relative_threshold} is calculated to have an absolute value of {threshold} \n"
      f"Remember! A higher threshold number = less sensitivity and less total frames in the output video") 
print("\n************************************************************\n\n")
print("Box filter Size:")
print(f"{box_size} x {box_size}")
print("\n************************************************************\n\n")

# Initialize the edit script
edit_script = ""

# Initialize the previous frame
prev_frame = None

# Initialize the start and end times for the current section
start_time = 0
end_time = 0

# Initialize the flag for detecting motion
detect_motion = False

# Initialize the counter for the number of frames
frame_count = 0

# create a frame on GPU for images
gpu_frame = cv2.cuda_GpuMat()

# Create the progress bar
pbar = tqdm.tqdm(total=num_frames)

# Initialize the counters for motion and no motion frames (These should be 0 that makes a divide by 0 error, This is why I say Approx haha)

motion_count = 1
no_motion_count = 1

# Initialize variables to keep track of the average, minimum, and maximum values of calc_thresh
average_calc_thresh = 0
min_calc_thresh = float('inf')
max_calc_thresh = float('-inf')


# Loop through the frames of the video
while True:
    # Read the next frame
    ret, frame = video.read()

    # Check if we have reached the end of the video
    if not ret:
        break

    gpu_frame.upload(frame)

    # Convert the frame to grayscale
    gpu_frame_small = cv2.cuda.resize(gpu_frame, (570, 320))
    gray = cv2.cuda.cvtColor(gpu_frame_small, cv2.COLOR_BGR2GRAY)
    filter = cv2.cuda.createBoxFilter(gray.type(), -1, (box_size, box_size))

    # Apply the filter to the GpuMat
    gpu_blurred = filter.apply(gray)
    
    # Calculate the absolute difference between the current frame and the previous frame
    gpu_diff = cv2.cuda.absdiff(gpu_blurred, prev_frame) if prev_frame is not None else gpu_blurred
    
    if args["show_thumbnail"]:
            gputhumbnail = gpu_diff
            gthumb = gputhumbnail.download()
            cv2.imshow('Difference Calculation 2', gthumb)
            cv2.waitKey(1)
    
    diff = gpu_diff.download()
     
    # Calculate the sum of the absolute differences
    sum_diff = np.sum(diff)

    overage = round(sum_diff / threshold, 3)
    overage = (f'{overage:.3f}')
    calc_thresh = round(sum_diff * 10.0 / 570 / 320,4)
    
    # Update the running average, minimum, and maximum values of calc_thresh
    average_calc_thresh = (average_calc_thresh * 49 + calc_thresh) / 50

    # Check if the sum is above the threshold
    if sum_diff > threshold:
        # Motion has been detected
        motion_count += 1

        # Check if we were previously detecting motion

        if detect_motion:
            # Update the end time
            end_time = frame_count / fps
        else:
            # Start a new section
            start_time = frame_count / fps
            end_time = start_time
            detect_motion = True

        # Display a thumbnail image of the frame being currently processed if the user specifies the -k flag
        if args["show_thumbnail"]:
            thumbnail = cv2.resize(frame, (570, 320))
            cv2.imshow('Frames being included 2', thumbnail)
            cv2.waitKey(1)

        # Calculate the ratio and percentile of frames with motion to frames with no motion
        motion_ratio = round(motion_count / (motion_count + no_motion_count), 4)
        motion_percent = round(100 * motion_count / (frame_count + 1), 1)

        # Updated the rounded versions of the averages
        
        ave_round = round(average_calc_thresh,4)

        # Print a message indicating that motion has been detected
 
        print(
            f"\033[F\033[0K\u001b[42;1m***** Motion\u001b[0m in frame: {frame_count} \tFrames in {filename} at threshold of {relative_threshold} with motion: {motion_count}  \t "
            f"Without: {no_motion_count} \t Approx. \u001b[40;1m{motion_percent} %\u001b[0m of the frames have motion \t Detected: {sum_diff}\t\tRelative multiplier {overage}\t\tCalculated threshold is {calc_thresh}\t\tAverage of last 50 frames: {ave_round}") 
    else:
        # No motion has been detected
        no_motion_count += 1

        # Check if we were previously detecting motion

        if detect_motion:
            # Motion has stopped, so add the current section to the edit script
            edit_script += f"between(t,{start_time},{end_time})+"
            detect_motion = False
        else:

            if args["show_thumbnail"]:
                thumbnail2 = cv2.resize(frame, (570, 320))
                cv2.imshow('Frames being disguarded 2', thumbnail2)
                cv2.waitKey(1)

        motion_ratio = round(motion_count / (motion_count + no_motion_count), 4)
        motion_percent = round(100 * motion_count / (frame_count), 1)
        # Updated the rounded versions of the averages
        
        ave_round = round(average_calc_thresh,4)
        
        print(
            f"\033[F\033[0K\u001b[41;1m** No motion\u001b[0m in frame: {frame_count} \tFrames in {filename} at threshold of {relative_threshold} with motion: {motion_count} \t "
            f"Without: {no_motion_count} \t Approx. \u001b[40;1m{motion_percent} %\u001b[0m of the frames have motion \t Detected: {sum_diff}\t\tRelative multiplier {overage}\t\tCalculated threshold is {calc_thresh}\t\tAverage of last 50 frames: {ave_round}") 

    # Update the previous frame
    prev_frame = gpu_blurred

    # Increment the frame counter
    frame_count += 1

    # Update the progress bar
    pbar.update(1)

# Close the progress bar
pbar.close()

# Print the total number of frames with motion and no motion
print(f"Total number of frames with motion: {motion_count}")
print(f"Total number of frames with no motion: {no_motion_count}")

# Calculate the ratio of frames with motion to frames with no motion

motion_ratio = motion_count / (motion_count + no_motion_count)

print(f"Ratio of frames with motion to frames with no motion: {motion_ratio:.2f}")

# Check if we were still detecting motion at the end of the video
if detect_motion:
    # Add the final section to the edit script
    edit_script += f"between(t,{start_time},{end_time})"

# Add the trailing code to the edit command

edit_video = f"[0:v]select=\'{edit_script}"
edit_audio = f"[0:a]aselect=\'{edit_script}"

# Remove the extra '+' sign at the end of the edit script, if any
edit_video = edit_video.rstrip("+")
edit_audio = edit_audio.rstrip("+")

edit_video += f"\',setpts=N/FRAME_RATE/TB[v];\n"
edit_audio += f"\',asetpts=N/SR/TB[a]"

filter_complex = edit_video + edit_audio
if verbose:
    print("Printing the complex filter\n************\n")
    print(filter_complex)

# Close the video file
video.release()

# Print the Edit scripts for debugging purposes

if verbose:
    print("\n\n************\nVideo script \n")
    print(edit_video)
    print("\n\n************\nAudio script \n")
    print(edit_audio)

# Check if the edit script is not empty
if edit_video:
    # Create a temporary file to store the edit script
    with open("filter_complex.txt", "w") as f:
        f.write(filter_complex)

    # Get the path of the temporary file
    edit_video = f.name

    # Create the command for ffmpeg

    command = f"{args['ffmpeg']} -hwaccel {args['hwaccel']} -i {rawfilepath} -filter_complex_script .\\{edit_video} -vcodec {args['vcodec']} -map [v] -map [a] {args['output']} "

    print("\n\n************\nNOW Executing the following ffmpeg command:\n")
    print(command)
    print("\n\n************\n")
    # Execute the command
    subprocess.run(command)
    