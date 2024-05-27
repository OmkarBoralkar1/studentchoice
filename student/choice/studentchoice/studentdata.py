import pandas as pd
import matplotlib.pyplot as plt
from filter import filter_subjects
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.cluster import KMeans
# from sklearn.preprocessing import LabelEncoder

# file_path = input("Enter the file path: ")
#
# # Specify the range of rows you want to read
# start_row = int(input("Enter the start row(number-2)(eg 3 so start as 1): "))
# end_row = int(input("Enter the end row: "))
# row_range = range(start_row, end_row + 1)
#
# # Specify the range of columns you want to keep
# start_column = int(input("Enter the start column(start from 0): "))
# end_column = int(input("Enter the end column(number+1)(eg 6 so end coloumn as 7): "))  # Note: The end column is inclusive
# column_range = range(start_column, end_column + 1)
file_path = 'C:/Users/Omkar/OneDrive - somaiya.edu/Documents/homeprices.csv'

# Specify the range of rows you want to read (rows 76 to 97)
start_row = 189
end_row = 211
row_range = range(start_row, end_row)

# Read the CSV file for the specified row range
data1 = pd.read_csv(file_path, delimiter='\t', skiprows=lambda x: x not in row_range)

# Specify the range of columns you want to keep (columns 1 to 3)
start_column = 0
end_column = 8  # Use end_column + 1 since Python slicing is exclusive on the end
column_range = range(start_column, end_column)
# Read the CSV file for the specified row and column range
data = pd.read_csv(file_path, delimiter='\t', skiprows=lambda x: x not in row_range, usecols=column_range)

# Display the resulting data
print(data)
df = pd.DataFrame(data)
print('the data frame is \n',df)
# Loop through each unique subject
unique_subjects = df['Subject'].unique()
non_nan_subjects = df['Subject'].dropna().unique()
print("the non_nan_subjects are ", non_nan_subjects)
# Rename columns dynamically based on the number of unique subjects
choice_columns = [f'choice{i + 1}' for i in range(len(unique_subjects))]
df.columns = ['student_names', 'Marks'] + choice_columns + ['Subject']
for choice_number in range(1, len(non_nan_subjects) + 1):
    # print(f"\nNumber of students who chose subjects in Choice {choice_number}:")
    for subject_of_interest in unique_subjects:
        if pd.notna(subject_of_interest):  # Skip NaN values in 'Subject'
            subject_students_count = df[df[f'Choice{choice_number}'] == subject_of_interest].shape[0]
            # print(f"  {subject_of_interest}: {subject_students_count} students")

            # Pass the information to the function
            choice_column_name = f'Choice{choice_number}'.replace(" ", "")  # Remove spaces
            subject_column_name = subject_of_interest.replace(" ", "")  # Remove spaces
            print('the choice_column_name and the subject_column_name is',choice_column_name,subject_column_name)
            # filter_subjects(df, choice_number, subject_of_interest, subject_students_count, threshold=5)

# Create a color map for subjects
colors = plt.cm.viridis(range(1, len(unique_subjects)))

# # Loop through each choice (starting from Choice1)
# fig, axes = plt.subplots(nrows=len(non_nan_subjects), ncols=2,  figsize=(20, 3 * len(non_nan_subjects)), sharex=True, sharey=True,
#                          gridspec_kw={'height_ratios': [1] * len(non_nan_subjects)})
#
# # Define x_positions
# x_positions = range(len(unique_subjects))
#
# # Loop through each choice (starting from Choice1)
# for choice_number, (ax_row1, ax_row2) in zip(range(1, len(non_nan_subjects) + 1), axes):
#     ax_row1.set_title(f"Choice {choice_number}")
#     ax_row2.set_title(f"Choice {choice_number}")
#
#     # Use the range of the length of subjects as tick locations
#     ax_row1.set_xticks(range(len(non_nan_subjects)))
#     ax_row2.set_xticks(range(len(non_nan_subjects)))
#
#     # Set unique_subjects as x-labels
#     ax_row1.set_xticks(x_positions)
#     ax_row1.set_xticklabels(unique_subjects, rotation=80, ha="right")
#     ax_row2.set_xticks(x_positions)
#     ax_row2.set_xticklabels(unique_subjects, rotation=80, ha="right")
#
#     for i, subject_of_interest in enumerate(unique_subjects):
#         if pd.notna(subject_of_interest):
#             subject_students_count = df[df[f'Choice{choice_number}'] == subject_of_interest].shape[0]
#             ax_row1.scatter([i], [subject_students_count], color=colors[i], s=100)
#             ax_row2.scatter([i], [subject_students_count], color=colors[i], s=100)
#
#     ax_row1.set_xlabel("Subjects")
#     ax_row1.set_ylabel(f"Number of students who chose choice {choice_number}")
#     ax_row2.set_xlabel("Subjects")
#     ax_row2.set_ylabel(f"Number of students who chose choice {choice_number}")
#
# plt.tight_layout()
# plt.show()
# Loop through each choice (starting from Choice1)
fig, axes = plt.subplots(nrows=1, ncols=len(non_nan_subjects), figsize=(20, 4))

# Define x_positions
x_positions = range(len(unique_subjects))

# Loop through each choice (starting from Choice1)
for choice_number, ax in zip(range(1, len(non_nan_subjects) + 1), axes):
    ax.set_title(f"Choice {choice_number}")

    # Use the range of the length of subjects as tick locations
    ax.set_xticks(range(len(non_nan_subjects)))

    # Set unique_subjects as x-labels
    ax.set_xticks(x_positions)
    ax.set_xticklabels(unique_subjects, rotation=45, ha="right")

    for i, subject_of_interest in enumerate(unique_subjects):
        if pd.notna(subject_of_interest):
            subject_students_count = df[df[f'Choice{choice_number}'] == subject_of_interest].shape[0]
            ax.scatter([i], [subject_students_count], color=colors[i], s=100)

    ax.set_xlabel("Subjects")
    ax.set_ylabel(f"Number of students who chose choice {choice_number}")

plt.tight_layout()
plt.show()
# # Use the filter_subjects function
# filtered_df = filter_subjects(df, f"Choice {choice_number}", f"  {subject_of_interest}: {subject_students_count}", threshold=5)
# print("Filtered DataFrame:")
# print(filtered_df)