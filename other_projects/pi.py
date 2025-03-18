# Let's find pi using nothing but Pythagoras!
import math

num_slices = 10000000

quarter_upper_bound = 0
quarter_lower_bound = 0

slice_thickness = 1.0 / num_slices
for i in range(num_slices):
    x = i * slice_thickness
    y = math.sqrt(1 - x ** 2)

    slice_area = slice_thickness * y
    quarter_upper_bound += slice_area

    if i > 0:
        quarter_lower_bound += slice_area

upper_bound = quarter_upper_bound * 4
lower_bound = quarter_lower_bound * 4

print(f'{lower_bound} <= pi <= {upper_bound}')

# 3.1415924535523594 <= pi <= 3.1415928535523587
# 3.14159245 <= pi <= 3.1415928

