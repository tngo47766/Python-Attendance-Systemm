import csv

def read_csv_to_dict(filename):
    user_dict = {}

    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            email = row['Email']
            user_info = {
                'name': row['Name'],
                'password': row['Password'],
                'role': 'user'
            }
            user_dict[email] = user_info

    return user_dict
