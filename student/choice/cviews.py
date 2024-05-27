# yourapp/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from choice.studentchoice.student1 import analyze_subject_choices
from choice.studentchoice.filter import filter_subjects
from django.core.files.storage import default_storage
from django.conf import settings
import os
import pandas as pd
from django.shortcuts import redirect

def analyze_subject(request):
    # print('hii')
    if request.method == 'POST':
        # print('hello')
        file_upload = request.FILES.get('filename')
        start_row = str(request.POST.get('start_row'))
        end_row = str(request.POST.get('end_row'))
        start_column = str(request.POST.get('start_column'))
        end_column = str(request.POST.get('end_column'))
        min_students = request.POST.get('min_student')  # Rename the variable

        # Save the file to a temporary location
        file_path = default_storage.save('tmp/' + file_upload.name, file_upload)

        # Get the absolute file path using os.path.join
        absolute_file_path = os.path.join(settings.BASE_DIR, file_path)

        print('the absolute path is ',absolute_file_path, start_row, end_row, start_column, end_column,min_students)
        
        # Call your analysis function
        df_result, result_dict_result = analyze_subject_choices(
            absolute_file_path, int(start_row), int(end_row), int(start_column), int(end_column)
        )

        # Print the resulting DataFrame
        print('The data frame is \n', df_result)

        # Call the filter_subjects function with the resulting DataFrame and result dictionary
        min_students = int(min_students) if min_students is not None else None
        data1=filter_subjects(df_result, result_dict_result, min_students)

        # Store the data in the session
        request.session['df_result'] = df_result.to_dict(orient='records')
        request.session['result_dict_result'] = result_dict_result
        data1_dict = data1.to_dict(orient='records')
        request.session['data1'] = data1.to_dict(orient='records')
        # print('the data1_dict got is\n',data1_dict)

        return render(request, 'user.html', {'data1': data1_dict})
    # print('Cannot go inside if ')
    return render(request, 'user.html', {'data1': None})
def save_data1(request):
    if request.method == 'POST':
        # Retrieve data1 from the session
        data1 = request.session.get('data1')
        print('the data got to saved is', data1)

        # Check if data1 is a list
        if isinstance(data1, list):
            # Convert the list to a DataFrame
            data1_df = pd.DataFrame(data1)
        else:
            data1_df = data1  # If data1 is already a DataFrame, no conversion is needed
        
        # Save the result to a CSV file with user input for the filename
        filename = request.POST.get('file_name_save')
        filename_with_extension = f"{filename}.csv"
        
        if os.path.exists(filename_with_extension):
            status_message = f"The file '{filename_with_extension}' already exists. Please choose another filename."
        else:
            data1_df.to_csv(filename_with_extension, index=False)
            status_message = f"CSV file saved successfully named: {filename_with_extension}"

        # Pass status_message along with data1 to the template
        return render(request, 'user.html', {'data1': data1, 'status_message': status_message})

    return render(request, 'user.html', {'data1': None})