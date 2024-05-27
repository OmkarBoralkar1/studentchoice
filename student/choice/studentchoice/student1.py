import pandas as pd
import matplotlib.pyplot as plt

def analyze_subject_choices(file_path, start_row, end_row, start_column, end_column):
    # Read the CSV file for the specified row and column range
    data = pd.read_csv(file_path, delimiter='\t|,', engine='python',
                       skiprows=lambda x: x not in range(start_row, end_row + 1),
                       usecols=range(start_column, end_column + 1))

    # Convert the data to a DataFrame
    df = pd.DataFrame(data)
    print("the student got is /n",df)
    # Get unique subjects excluding NaN
    unique_subjects = df['Subject'].dropna().unique()

    # Rename columns dynamically based on the number of unique subjects
    choice_columns = [f'choice{i + 1}' for i in range(len(unique_subjects))]
    df.columns = ['student_names', 'Marks'] + choice_columns + ['Subject']+['Email']

    # Initialize a dictionary to store the results
    result_dict = {}

    # Loop through each unique subject
    for subject_of_interest in unique_subjects:
        subject_results = {}
        for choice_number in range(1, len(unique_subjects) + 1):
            # Count the number of students who chose the subject for each choice
            subject_students_count = df[df[f'choice{choice_number}'].str.lower() == subject_of_interest.lower()].shape[0]
            subject_results[f'Choice {choice_number}'] = subject_students_count
        result_dict[subject_of_interest] = subject_results

    # Print the dictionary
    print(result_dict)

    # Create a color map for subjects
    colors = plt.cm.viridis(range(1, len(unique_subjects) + 1))

    # Loop through each choice to create bar plots
    fig, axes = plt.subplots(nrows=1, ncols=len(unique_subjects), figsize=(22, 4))

    # Define x_positions
    x_positions = range(len(unique_subjects))

    # Loop through each choice
    for choice_number, ax in zip(range(1, len(unique_subjects) + 1), axes):
        ax.set_title(f"Choice {choice_number}")

        # Use the range of the length of subjects as tick locations
        ax.set_xticks(range(len(unique_subjects)))

        # Set unique_subjects as x-labels
        ax.set_xticks(x_positions)
        ax.set_xticklabels(unique_subjects, rotation=45, ha="right")

        for i, subject_of_interest in enumerate(unique_subjects):
            # Count the number of students who chose the subject for each choice
            subject_students_count = df[df[f'choice{choice_number}'].str.lower() == subject_of_interest.lower()].shape[0]
            ax.bar(i, subject_students_count, color=colors[i])

        ax.set_xlabel("Subjects")
        ax.set_ylabel(f"Number of students who chose choice {choice_number}")

    plt.tight_layout()
    plt.show()

    # Return the DataFrame and result dictionary
    return df, result_dict