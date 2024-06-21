#!/usr/bin/env python
import matplotlib.pyplot as plt

# Sample data from your input
data = [
    (1, 1.84110, 11.03347),
    (2, -0.78538, 6.98951),
    (3, -2.83208, 7.37793),
    (4, -3.77914, 5.44918),
    (5, -3.33757, 4.70180),
    (6, -3.56853, 3.68136),
    (7, -4.27011, 4.75714),
    (8, -3.32821, 2.38562),
    (9, -4.77076, 3.83770),
    (10, -4.37176, 2.45899),
    (11, -3.45676, 2.37715),
    (12, -3.12197, 2.01705),
    (13, -4.69321, 6.07627),
    (14, -2.81889, 2.31386),
    (15, -2.97587, 6.26391),
    (16, -4.16927, 5.31570),
    (17, -3.36303, 2.82405),
    (18, -4.96310, 4.45560),
    (19, -4.26897, 2.58652),
    (20, -4.16515, 3.87143),
    (21, -3.23894, 3.06149),
    (22, -3.31289, 7.44865),
    (23, -2.45679, 2.57112),
    (24, -2.66921, 5.17006),
]

# Extract the data columns
x_data, curvature_data, angle_data = zip(*data)

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(x_data, curvature_data, label='Curvature', marker='o', linestyle='-', color='b')
plt.plot(x_data, angle_data, label='Angle', marker='x', linestyle='--', color='r')
plt.xlabel('Ionic Step Size')
plt.ylabel('Value')
plt.title('Curvature and Angle vs Ionic Step Size')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

