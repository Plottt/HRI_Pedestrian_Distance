import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Circle



def main():
    # Load data from CSV file
    all_frames = []
    fig = plt.figure(figsize=(10, 6))
    # control
    p1_data = np.loadtxt("participant_data/trajectories2/pc_traj_1.csv", delimiter=',', skiprows=1)
    frames1 = process_frame(p1_data)
    all_frames.append(frames1)
    # control
    p2_data = np.loadtxt("participant_data/trajectories2/pc_traj_2.csv", delimiter=',', skiprows=1)
    frames2 = process_frame(p2_data)
    all_frames.append(frames2)
    # control
    p3_data = np.loadtxt("participant_data/trajectories2/pc_traj_3.csv", delimiter=',', skiprows=1)
    frames3 = process_frame(p3_data)
    all_frames.append(frames3)
    # light sound
    p4_data = np.loadtxt("participant_data/trajectories2/pc_traj_4.csv", delimiter=',', skiprows=1)
    frames4 = process_frame(p4_data)
    all_frames.append(frames4)
    # light sound
    p5_data = np.loadtxt("participant_data/trajectories2/pc_traj_5.csv", delimiter=',', skiprows=1)
    frames5 = process_frame(p5_data)
    all_frames.append(frames5)
    # light sound
    p6_data = np.loadtxt("participant_data/trajectories2/pc_traj_6.csv", delimiter=',', skiprows=1)
    frames6 = process_frame(p6_data)
    all_frames.append(frames6)
    # harsh sound
    p7_data = np.loadtxt("participant_data/trajectories2/pc_traj_7.csv", delimiter=',', skiprows=1)
    frames7 = process_frame(p7_data)
    all_frames.append(frames7)
    # harsh sound
    p8_data = np.loadtxt("participant_data/trajectories2/pc_traj_8.csv", delimiter=',', skiprows=1)
    frames8 = process_frame(p8_data)
    all_frames.append(frames8)
    # harsh sound
    p9_data = np.loadtxt("participant_data/trajectories2/pc_traj_9.csv", delimiter=',', skiprows=1)
    frames9 = process_frame(p9_data)
    all_frames.append(frames9)
    # blue light
    p10_data = np.loadtxt("participant_data/trajectories2/pc_traj_10.csv", delimiter=',', skiprows=1)
    frames10 = process_frame(p10_data)
    all_frames.append(frames10)
    # blue light
    p11_data = np.loadtxt("participant_data/trajectories2/pc_traj_11.csv", delimiter=',', skiprows=1)
    frames11 = process_frame(p11_data)
    all_frames.append(frames11)
    # blue light
    p12_data = np.loadtxt("participant_data/trajectories2/pc_traj_12.csv", delimiter=',', skiprows=1)
    frames12 = process_frame(p12_data)
    all_frames.append(frames12)
    # red light
    p13_data = np.loadtxt("participant_data/trajectories2/pc_traj_13.csv", delimiter=',', skiprows=1)
    frames13 = process_frame(p13_data)
    all_frames.append(frames13)
    # red light
    p15_data = np.loadtxt("participant_data/trajectories2/pc_traj_15.csv", delimiter=',', skiprows=1)
    frames15 = process_frame(p15_data)
    all_frames.append(frames15)
    # red light + harsh sound
    p16_data = np.loadtxt("participant_data/trajectories2/pc_traj_16.csv", delimiter=',', skiprows=1)
    frames16 = process_frame(p16_data)
    all_frames.append(frames16)
    # red light + harsh sound
    p17_data = np.loadtxt("participant_data/trajectories2/pc_traj_17.csv", delimiter=',', skiprows=1)
    frames17 = process_frame(p17_data)
    all_frames.append(frames17)
    # red light + harsh sound
    p18_data = np.loadtxt("participant_data/trajectories2/pc_traj_18.csv", delimiter=',', skiprows=1)
    frames18 = process_frame(p18_data)
    all_frames.append(frames18)
    plot_all_frames(all_frames)

    x_c, z_c = get_average_line([frames1, frames2, frames3], -2, -.4)
    x_s, z_s = get_average_line([frames4, frames5, frames6], -3, -.6)
    x_h, z_h = get_average_line([frames7, frames8, frames9], -3, -.55)
    x_b, z_b = get_average_line([frames10, frames11, frames12], -3, -.5)
    x_r, z_r = get_average_line([frames13, frames15], -3, -.5)
    x_t, z_t = get_average_line([frames16, frames17], -3, -.55)

    # # print z-distance at -0.6 meters
    # c_idx = np.argmin(abs(x_c + 0.6))
    # print(f"control: {z_c[c_idx]}")
    # s_idx = np.argmin(abs(x_s + 0.6))
    # print(f"soft: {z_s[s_idx]}")
    # h_idx = np.argmin(abs(x_h + 0.6))
    # print(f"harsh: {z_h[h_idx]}")
    # b_idx = np.argmin(abs(x_b + 0.6))
    # print(f"blue: {z_b[b_idx]}")
    # r_idx = np.argmin(abs(x_r + 0.6))
    # print(f"red: {z_r[r_idx]}")
    # t_idx = np.argmin(abs(x_t + 0.6))
    # print(f"combined: {z_t[t_idx]}")


    plt.figure()
    plt.plot(x_c, z_c, 'k', linewidth=3, label='control')
    plt.plot(x_s, z_s, ':k', linewidth=2, label='soft sound')
    plt.plot(x_h, z_h, '--k', linewidth=2, label='aggressive sound')
    plt.plot(x_b, z_b, 'b', linewidth=2, label='blue light')
    plt.plot(x_r, z_r, 'r', linewidth=2, label='blinking red light')
    plt.plot(x_t, z_t, '--r', linewidth=2, label='aggressive and red')
    circle = Circle((0,0), 0.28, facecolor='lightgrey', edgecolor='black',linestyle='--', linewidth=1.5)
    plt.gca().add_patch(circle)
    plt.text(0, 0, 'Robot', fontsize=12, color='black', ha='center', va='center')  # Add text
    plt.legend()
    plt.ylim([-0.3, 2])
    plt.xlim([-3.1, 0.3])
    plt.title('Averaged Pedestrian Path')
    plt.xlabel('Distance Parallel to Hallway [m]')
    plt.ylabel('Distance Perpendicular to Hallway [m]')
    plt.gca().set_aspect('equal', adjustable='box') 

    plt.show()


def process_frame(data):
    # Extract columns and adjust time to start from 0
    time = np.round((data[:, 1] - data[0, 1]), 3)
    x_data = data[:, 2]
    y_data = data[:, 3]
    z_data = data[:, 4]

    # Rotate degrees about the y-axis
    theta = np.radians(-2)
    x_rotated = x_data * np.cos(theta) + z_data * np.sin(theta)
    y_rotated = y_data  # y remains the same
    z_rotated = -x_data * np.sin(theta) + z_data * np.cos(theta)

    frames = {}
    frames['xdata'] = x_rotated
    frames['zdata'] = z_rotated
    frames['time'] = time

    return frames


def plot_all_frames(all_frames):
    

    fig, ax = plt.subplots(figsize=(10, 6))
    for idx, frames in enumerate(all_frames):
        if idx < 3: clr = 'black'; 
        elif idx < 6: clr = 'yellow'
        elif idx < 9: clr = 'green'; 
        elif idx < 12: clr = 'blue'; 
        elif idx < 14: clr = 'red'; 
        else: clr = 'magenta'; 

        ax.plot(frames['xdata'], frames['zdata'], color=clr)

        # Add color markers based on time
        sc = ax.scatter(frames['xdata'], frames['zdata'], color='black') #c=frames['time'], cmap='viridis')
        

    # Set labels and title for 2D plot
    plt.xlabel('X (meters)')
    plt.ylabel('Z (meters)')
    plt.title('X vs Z Trajectory Plot Colored by Time')
    plt.ylim([0,2])
    # plt.xlim([-6.5,0.5])
    plt.show()

def get_average_line(series, min, max):

    interp_points = np.linspace(min, max, 100)
    avg_z = np.zeros(len(interp_points))
    for pt_idx, pt in enumerate(interp_points):
        z_pt_sum = 0
        valid_series_count = 0
        for s in series:
            xs = np.array(s['xdata'])
            zs = np.array(s['zdata'])
            below_idx = np.where(xs <= pt)[0]
            above_idx = np.where(xs >= pt)[0]

            if len(below_idx) == 0 or len(above_idx) == 0:
                continue

            idx1 = below_idx[-1]
            idx2 = above_idx[0]
            x_small, x_large = xs[idx1], xs[idx2]
            z_small, z_large = zs[idx1], zs[idx2]
            weight = (pt - x_small) / (x_large - x_small)
            z_pt = z_small + weight * (z_large - z_small)
            z_pt_sum += z_pt
            valid_series_count += 1
        try:
            avg_z[pt_idx] = z_pt_sum / valid_series_count
        except:
            print("error", pt)

    return(interp_points, avg_z)




if __name__ == "__main__":
    main()
