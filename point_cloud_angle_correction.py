import pyrealsense2 as rs
import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression


def main():
    # Load .bag file
    # bag_file = "participant_data/20241113_175819.bag" # bag1: -50.5
    # bag_file = "participant_data/20241113_181610.bag" # bag2: -51
    # bag_file = "participant_data/20241113_183313.bag" # bag3: -51.5
    # bag_file = "participant_data/20241113_191456.bag" # bag4: -51.5
    # bag_file = "participant_data/20241113_192808.bag" # bag5: -52
    # bag_file = "participant_data/20241115_180246.bag" # bag6: -51
    # bag_file = "participant_data/20241115_181326.bag" # bag7: -51
    # bag_file = "participant_data/20241118_180111.bag" # bag8: -54
    # bag_file = "participant_data/20241118_180905.bag" # bag9: -52.5
    # bag_file = "participant_data/20241118_182149.bag" # bag10: -52.5
    # bag_file = "participant_data/20241118_183813.bag" # bag11: -52.5
    # bag_file = "participant_data/20241118_184933.bag" # bag12: -53
    # bag_file = "participant_data/20241120_174026.bag" # bag13: -46
    # bag_file = "participant_data/20241120_181350.bag" # bag15: -46
    # bag_file = "participant_data/20241120_182323.bag" # bag16: -45
    # bag_file = "participant_data/20241120_183511.bag" # bag17: -46
    # bag_file = "participant_data/20241120_184630.bag" # bag18: -47    


    vertices, colors = get_points(bag_file, target_frame=20)
    print("got vertices")
    show_pc_and_get_anlge(vertices)
    return



def get_points(bag_file, target_frame=1):
    cur_frame=0
    pipeline = rs.pipeline()
    config = rs.config()
    rs.config.enable_device_from_file(config, bag_file, repeat_playback=False)
    pipeline.start(config)
    align = rs.align(rs.stream.color)
    while True:
        print(cur_frame, ' / ', target_frame)
        cur_frame+=1

        frames = pipeline.wait_for_frames()
        
        if (cur_frame == target_frame):
            # Get depth and color frames
            aligned_frames = align.process(frames)
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            # if not depth_frame or not color_frame:
            #     continue

            # Intrinsics & 3D points
            depth_intrinsics = depth_frame.profile.as_video_stream_profile().intrinsics
            color_intrinsics = color_frame.profile.as_video_stream_profile().intrinsics

            # Convert depth and color to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            pc = rs.pointcloud()
            pc.map_to(color_frame)
            points = pc.calculate(depth_frame)

            # Convert point cloud to numpy array
            vertices = np.asanyarray(points.get_vertices()).view(np.float32).reshape(-1, 3)
            colors = np.asanyarray(points.get_texture_coordinates()).view(np.float32).reshape(-1, 2)
            pipeline.stop()
            break
        else:
            continue
    
         
    
    return(vertices, colors)

def fit_line_and_find_rotation(vertices):
    # Project points onto the X-Z plane (ignore Y-coordinate)
    x = vertices[:, 0].reshape(-1, 1)  # X values (as 2D array for sklearn)
    z = vertices[:, 2].reshape(-1, 1)  # Z values (as 2D array for sklearn)

    # Fit a line to the points in the X-Z plane
    model = LinearRegression()
    model.fit(x, z)

    # Extract the slope of the fitted line
    slope = model.coef_[0][0]

    # Calculate the rotation angle needed to make the line parallel to the X-axis
    rotation_angle = np.arctan(slope)  # Angle in radians
    rotation_angle_deg = np.degrees(rotation_angle)  # Convert to degrees

    # Print the results
    print(f"Slope of fitted line: {slope}")
    print(f"Rotation angle to make line parallel to X-axis: {rotation_angle_deg:.2f} degrees")

    return rotation_angle_deg



def show_pc_and_get_anlge(vertices):
    
    # Plot with Matplotlib
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Downsample points for better visualization
    sampled_indices = np.random.choice(vertices.shape[0], size=50000, replace=False)
    sampled_vertices = vertices [sampled_indices]

    # Filter sampled vertices within bounds
    x_bounds = (-5, 1.5)
    y_bounds = (0.25, 0.5)
    z_bounds = (0, 5)

    # Filter original points
    filtered_sampled_vertices = sampled_vertices[
        (sampled_vertices[:, 0] >= x_bounds[0]) & (sampled_vertices[:, 0] <= x_bounds[1]) &
        (sampled_vertices[:, 1] >= y_bounds[0]) & (sampled_vertices[:, 1] <= y_bounds[1]) &
        (sampled_vertices[:, 2] >= z_bounds[0]) & (sampled_vertices[:, 2] <= z_bounds[1])
    ]

    rot_angle = fit_line_and_find_rotation(filtered_sampled_vertices); # deg
    theta = np.radians(rot_angle)

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

    # Set labels and view
    ax.set_title(f"Point Cloud Visualization,  Rotation Angle: {rot_angle:.2f}°")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")

    ax.set_xlim(x_bounds)
    ax.set_ylim(y_bounds)
    ax.set_zlim(z_bounds)

    ax.view_init(elev=0, azim=-90)  # Y-axis up
    ax.legend()

    plt.show()


if __name__ == '__main__':
    main()


