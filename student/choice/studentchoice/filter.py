import pandas as pd
import os
import random

def filter_subjects(data, result_dict, min_students):
    # Print information about the received data and result dictionary
    # print('the result dict is', result_dict)
    # print('the data received is \n', data)
    data3=data
    data2=data.Email
    data = data.drop(['Email'], axis=1)

    # print('the new data is',data)
    # print('the data2 is\n',data2)
    # print('the datalength',max_choices )
    # Get the minimum number of students for a batch from the user
    # min_students = int(input('Enter the minimum students for a batch'))
    max_choices = len(data['Subject'].dropna().unique())
    # Lists to store information about dropped students and subjects
    dropped_students_info = []
    dropped_subjects = []

    # List to store information about selected students
    selected_data1 = []

    # Iterate over subjects in the result_dict
    for subject in result_dict.keys():
        # print('the datalength', len(data['Subject'].dropna().unique()))
        # Get the count of students who chose the subject as Choice 1
        total_students = result_dict[subject]['Choice 1']

        # Check if the total count is less than the specified minimum
        if total_students < (min_students - 2):
            print(f"Dropping subject '{subject}' as total students ({total_students}) is less than {min_students}")
            dropped_subjects.append(subject)
        else:
            print(f"Keeping subject '{subject}' with total students: {total_students}")

    # Drop subjects and collect information about dropped students
    for subject in dropped_subjects:
        # Use boolean indexing to get rows where choice1 is the subject
        dropped_students = data[(data['choice1'] == subject)]

        # Append information about dropped students to the list
        dropped_students_info.extend(dropped_students.values.tolist())

        # Drop rows where choice1 is the dropped subject
        data = data[~((data['choice1'] == subject))]

    # Assign subjects to dropped students
    dropped_students_assignments = []
    for student_info in dropped_students_info:
        student_name = student_info[0]

        # Initialize chosen_choice and next_choice_subject
        chosen_choice = None
        next_choice_subject = None

        # Iterate through choices (choice1, choice2, choice3)
        for choice_num in range(1, max_choices + 1):
            choice_subject = student_info[choice_num + 2]  # Adjust index based on the structure of the data

            # Check if the choice is not the dropped subject
            if choice_subject not in dropped_subjects:
                chosen_choice = f'Choice{choice_num + 1}'
                next_choice_subject = choice_subject
                break  # Exit the loop if a valid choice is found

        # If no valid choice is found, handle it (you can modify this part based on your requirements)
        if not chosen_choice:
            print(f"No valid choice found for student '{student_name}'. Assigning to a default subject.")
            chosen_choice = 'Choice1'  # Assign to the first choice by default
            next_choice_subject = student_info[2]  # Assign to the first choice by default

        # Append the assignment information to the list
        dropped_students_assignments.append([student_name, next_choice_subject, chosen_choice])

    # Assign subjects for students who have not been in dropped_students_assignments
    students_not_dropped = data[~data['student_names'].isin([row[0] for row in dropped_students_assignments])]
    selected_data1.extend(
        students_not_dropped[['student_names', 'choice1']].assign(Chosen_Choice='Choice1').values.tolist())

    # Print information about the dropped students and selected data
    As = pd.DataFrame(dropped_students_assignments, columns=['student_names', 'Assigned_Subject', 'Chosen_Choice'])
    SS = pd.DataFrame(selected_data1, columns=['student_names', 'Assigned_Subject', 'Chosen_Choice'])
    combined_data = pd.concat([As, SS], ignore_index=False)

    # Fill NaN values with remaining subjects randomly
    remaining_subjects = data[~data['Subject'].isin(dropped_subjects)]['Subject'].dropna().unique()
    # Assuming 'student_name' is the column you are checking for not being NaN
    combined_data['Assigned_Subject'] = combined_data.apply(
        lambda row: random.choice(remaining_subjects) if pd.isna(row['Assigned_Subject']) and not pd.isna(
            row['student_names']) else row['Assigned_Subject'],
        axis=1
    )

    # Group by "Assigned_Subject" and count the number of students in each group
    subject_clusters = combined_data.groupby('Assigned_Subject').size().reset_index(name='Number_of_Students')

    # Print the subject clusters
    data1 = pd.concat([combined_data, subject_clusters], ignore_index=False)
    # print('the final data is\n',data1)
    data2=email_merge(data3,data1)
    print('the final data is data2\n',data2)
    return data2
def email_merge(data3, data1):
    print('the data got is in the merge function', data3, '\n', data1)

    # Select only 'student_names' and 'Email' columns from data3
    selected_data3 = data3[['student_names', 'Email']]

    # Merge data1 and selected_data3 based on the student names
    merged_data = pd.merge(data1, selected_data3, on='student_names', how='outer')

    # Print the final merged data
    # print('The merged data is:')
    # print(merged_data)
    return merged_data
