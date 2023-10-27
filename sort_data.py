import os
import re
import pandas as pd
from shutil import copyfile

def run():
    # Duong dan toi Attendance
    source_directory = "Attendance"

    # Duong dan toi Sorted-Attendance
    sorted_directory = "static\Sorted_Attendance"
    os.makedirs(sorted_directory, exist_ok=True)

    # Lay date cua fike
    def extract_date(filename):
        match = re.search(r'Attendance_(\d{2}-\d{2}-\d{2})\.csv', filename)
        if match:
            date_str = match.group(1)
            return pd.to_datetime(date_str, format='%d-%m-%y')
        else:
            return pd.NaT  # Tra ve khong phai date time 

    # Liet ke cac file co duoi csv trong attendance
    csv_files = [file for file in os.listdir(source_directory) if file.endswith(".csv")]

    # Sort by date
    csv_files.sort(key=extract_date)


    for csv_file in csv_files:
        file_path = os.path.join(source_directory, csv_file)
        df = pd.read_csv(file_path)
        date = extract_date(csv_file)

        # Tao folder thang nam neu khong ton tai
        year_directory = os.path.join(sorted_directory, str(date.year))
        month_directory = os.path.join(year_directory, date.strftime("%B"))

        os.makedirs(year_directory, exist_ok=True)
        os.makedirs(month_directory, exist_ok=True)

        # Copy cac file phu hop vao dung vi tri
        output_file = os.path.join(month_directory, csv_file)
        copyfile(file_path, output_file)

    print("The Attendance Files Have Been Sorted")
run()