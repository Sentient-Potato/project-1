import csv

def processing(name, id_num, vote):
    csv_file = 'voting_records'
    existing_ids = set()

    # Retrieves existing data in csv file
    try:
        with open(csv_file, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skips existing header
            for row in reader:
                if len(row) > 1:
                    existing_ids.add(row[1])
    except FileNotFoundError:
        pass  # Should the file not exist the first time, it will create one and use it onwards

    # Detects if an ID has already been entered into the system
    if id_num in existing_ids:
        return "Existing ID" # Error type 4

    # Adds the new data
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # To create the header in case a new file is made
        if file.tell() == 0:
            writer.writerow(['Name', 'ID', 'Vote'])

        writer.writerow([name, id_num, vote])

    processed_text = f"Name: {name}, ID: {id_num}, Vote: {vote}"
    return processed_text # Returns processed_text to indicate successful data processing
