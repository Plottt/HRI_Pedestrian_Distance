import matplotlib.pyplot as plt
import numpy as np

# z-distances 0.6 meters before robot 
control_pc = 0.45477643925318373
soft_pc = 0.9473053401224147
harsh_pc = 0.7949707514289176
blue_pc = 0.7020615935809219
red_pc = 0.9447816554958983
combined_pc = 0.9532528674666967

# survey responses
control_survey = 1.333333333
soft_survey = 2.666666667
harsh_survey = 2
blue_survey = 3.333333333
red_survey = 2.666666667
combined_survey = 3.333333333
pc_data = [control_pc, soft_pc, harsh_pc, blue_pc, red_pc, combined_pc]
survey_data = [control_survey, soft_survey, harsh_survey, blue_survey, red_survey, combined_survey]
colors = ['black', 'green', 'yellow', 'blue', 'red', 'brown']
labels = ['control', 'soft sounds', 'aggressive sounds', 'blue light', 'blinking red light', 'aggressive and red']

plt.figure()

# Loop through data, colors, and labels to create separate scatter plots
for survey, pc, color, label in zip(survey_data, pc_data, colors, labels):
    plt.scatter(survey, pc, c=color, s=100, label=label)

# Add annotations to indicate x-axis meaning
# plt.text(1, 0.05, "Very Relaxed", fontsize=10, color='black', ha='center', va='center')
# plt.text(5, 0.05, "Very Tense", fontsize=10, color='black', ha='center', va='center')

# Add the legend
plt.legend(loc='lower right')

# Set axis limits
plt.xlim([0.5, 5.5])
plt.ylim([0, 1])

# Add labels and title
plt.title("Pedestrian Distance from Robot vs. Perception of Environment")
plt.xlabel("Survey Score of Hallway Envinronment (1=Very Relaxed, 5=Very Tense)")
plt.ylabel("Distance from Robot Perpendicular to Hallway, \n 0.6m Before Passing the Robot [m]")

plt.show()


