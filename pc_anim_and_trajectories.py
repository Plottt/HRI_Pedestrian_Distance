import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
from matplotlib.animation import FuncAnimation
import csv
from tqdm import tqdm
import cv2


def process_raw_frame(frames, align):
    # Align the depth and color frames
    aligned_frames = align.process(frames)
    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    # if not depth_frame or not color_frame:
    #     raise ValueError("Depth or color frame is missing.")

    # Generate point cloud
    pc = rs.pointcloud()
    pc.map_to(color_frame)
    points = pc.calculate(depth_frame)
    vertices = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, 3)

    # color_img = np.asanyarray(color_frame.get_data())
    return vertices #, color_img

def save_trajectories_to_csv(trajectory):
    try:
        with open(csv_fileName, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write header:
            # csv_writer.writerow(['frame_index', 'time (s)', 'x (m)', 'y (m)', 'z (m)'])
            csv_writer.writerow(trajectory)
        print(f"Trajectories saved to {csv_fileName}")
    except Exception as e:
        print(f"Error saving trajectories to CSV: {e}")


def get_all_frames(bag_file, start_frame, end_frame):
    pipeline = rs.pipeline()
    config = rs.config()
    rs.config.enable_device_from_file(config, bag_file, repeat_playback=False)
    pipeline.start(config)
    align = rs.align(rs.stream.color)

    all_vertices = []
    all_timestamps = []
    # all_color_frames = []
    prev_time = -1
    frame_cnt = 0
    with tqdm(total=end_frame, desc="Processing Frames") as pbar:
        while frame_cnt <= end_frame:
            try:
                frames = pipeline.wait_for_frames()
            except RuntimeError:
                print("End of frames")
                pipeline.stop()
                break

            time = frames.get_timestamp()
            if (prev_time != time):
                frame_cnt+=1
                prev_time = time
                pbar.update(1)

                if (frame_cnt >= start_frame and frame_cnt <= end_frame):
                    # Extract point cloud data
                        vertices = process_raw_frame(frames, align)
                        all_vertices.append(vertices)
                        # all_color_frames.append(color_frame)
                        all_timestamps.append(frames.get_timestamp())


    print(f"processed {frame_cnt} frames")
    return(all_vertices, all_timestamps) #, all_color_frames)

def get_frame_vertices(frame_num, num_vertices):
    vertices = all_vertices[frame_num]
    sampled_indices = np.random.choice(vertices.shape[0], size=min(num_vertices, vertices.shape[0]), replace=False)
    sampled_vertices = vertices[sampled_indices]
    return(sampled_vertices)

    

def animate_point_cloud():

    # Initialize Matplotlib figure
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    def update(frame_idx):
        # Clear the axis for the new frame
        ax.clear()

        sampled_vertices = get_frame_vertices(frame_idx, 20000)
        if (frame_idx == 0):
            global start_time
            start_time = all_timestamps[frame_idx]
        timestamp = all_timestamps[frame_idx] 
        timestamp_sec = np.round((timestamp - start_time)/1000, 3)


       # Filter sampled vertices within bounds
        x_bounds = (-5, 1.5)
        y_bounds = (-0.25, -.01)
        z_bounds = (-2, 5)

        filtered_sampled_vertices = sampled_vertices[
            (sampled_vertices[:, 0] >= x_bounds[0]) & (sampled_vertices[:, 0] <= x_bounds[1]) &
            (sampled_vertices[:, 1] >= y_bounds[0]) & (sampled_vertices[:, 1] <= y_bounds[1]) &
            (sampled_vertices[:, 2] >= z_bounds[0]) & (sampled_vertices[:, 2] <= z_bounds[1])
        ]
        # Calculate rotation angle
        rot_angle = rotation_angle_deg
        theta = np.radians(rot_angle)

        # Rotate points
        rot_vertices = filtered_sampled_vertices.copy()
        rot_vertices[:, 0] = filtered_sampled_vertices[:, 0] * np.cos(theta) + filtered_sampled_vertices[:, 2] * np.sin(theta)
        rot_vertices[:, 2] = -filtered_sampled_vertices[:, 0] * np.sin(theta) + filtered_sampled_vertices[:, 2] * np.cos(theta)

        # Scatter plot of filtered points
        ax.scatter(
            filtered_sampled_vertices[:, 0],
            filtered_sampled_vertices[:, 1],
            filtered_sampled_vertices[:, 2],
            c='b',  # Blue for original points
            s=1,
            label='Original Points',
        )

        ax.scatter(
            rot_vertices[:, 0],
            rot_vertices[:, 1],
            rot_vertices[:, 2],
            c='r',  # Red for rotated points
            s=1,
            label='Rotated Points',
        )


        close_idxs = rot_vertices[:,2] < cutoff_dist
        if sum(close_idxs) > 20:
        # find the average of the 10 next closest (second group of 10), record it and a timestamp
        # Then, plot these trajectories
            close_points = rot_vertices[close_idxs]
            z_distances = close_points[:, 2]

            # Sort the points by Z-coordinate in ascending order
            sorted_indices = np.argsort(z_distances)
            sorted_points = close_points[sorted_indices]

            second_group = sorted_points[10:20]

            # Calculate the average X, Y, and Z coordinates
            average_xyz = np.mean(second_group, axis=0)  # Mean of X, Y, and Z

            # Record the average and timestamp
            save_trajectories_to_csv((frame_idx, timestamp, average_xyz[0], average_xyz[1], average_xyz[2]))

            print(f"Frame {frame_idx}: Average X, Y, Z of second group: {average_xyz}, Timestamp: {timestamp}")

            ax.scatter(
                average_xyz[0],
                average_xyz[1],
                average_xyz[2],
                c='g',  # Red for rotated points
                s=75,
                label='person',
            )


        # Set labels, axis limits, and view
        ax.set_title(f"Frame {frame_idx}, Time {timestamp_sec}, Rotation Angle: {rot_angle:.2f}°")
        ax.set_xlabel("X (m)")
        ax.set_ylabel("Y (m)")
        ax.set_zlabel("Z (m)")
        ax.set_xlim(x_bounds)
        ax.set_ylim(y_bounds)
        ax.set_zlim(z_bounds)
        ax.view_init(elev=0, azim=-90)
        ax.legend()

    ani = FuncAnimation(fig, update, frames=(end_frame-start_frame), repeat=True)
    plt.show()


def save_video(frames, timestamps, output_file):
    height, width, channels = frames[0].shape

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_file, fourcc, 15, (width, height))

    for idx, frame in enumerate(frames):
        if frame.dtype != np.uint8:
            frame = (frame * 255).astype(np.uint8)
        video_writer.write(frame)

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_color = (0, 255, 0)  # Green
        thickness = 2
        position = (50, 50)  # X, Y position
        frame_text = f"frame {idx}: {timestamps[idx]}s"
        frame = cv2.putText(frame, frame_text, position, font, font_scale, font_color, thickness, cv2.LINE_AA)


    video_writer.release()
    print(f"video saved to {output_file}")


rotation_angle_deg = -47
start_frame = 1020
end_frame = 1140
cutoff_dist = 1.5 # meters
csv_fileName = 'participant_data/trajectories2/pc_traj_18.csv'
# video_fimeName = 'participant_data/videos2/person1.mp4'

if __name__ == '__main__':
    bag_file = "participant_data/20241120_184630.bag"  # Replace with your .bag file path
    global all_vertices
    global all_timestamps
    all_vertices, all_timestamps = get_all_frames(bag_file, start_frame, end_frame)
    # save_video(all_color_frames, all_timestamps, video_fimeName)
    animate_point_cloud()
