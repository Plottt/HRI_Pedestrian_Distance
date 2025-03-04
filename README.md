# HRI_Pedestrian_Distance
Code for HRI Pedestrian Distance Project

Goal: Improve Human-Robot Interaction (HRI) design by quantifying impact of robot lights and sounds on pedestrian distance and comfort.
Question: How does varying robot lights and sounds impact how far away pedestrians will keep from the robot? How do the lights and sounds impact the pedestrian state (e.g., scary vs pleasant?)
Result: subtle lighting and sounds can effectively cause pedestrians to keep distance without causing excessive distress. Aggressive lights and sounds offer limited additional separation from the robot, but induce a lot of stress in participants.

**HRI_LIGHTS_CODE.ino**: Run the LED lightstrip: off, constant blue, variable frequency red blinking

**point_cloud_angle_correction.py** : Correct camera yaw misalignment. Projects wall onto ground plane and calculates rotation

**pc_anim_and_trajectories.py**: Animate point cloud and get person trajectory

**pc_anim_for_video.py**: Display a nicely formatted animated pointcloud for sharing

**plot_survey_and_pc_data.py** : code to plot pedestrian final position vs survey results

**traj_plotter2.py**: plot trjaectories and averaged trajectories

**video_framestamps.txt** : framestamps for realsense videos for when people pass
