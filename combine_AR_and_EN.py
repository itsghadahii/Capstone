import json
import csv
from datetime import datetime
from collections import OrderedDict

# Load the JSON data
with open('Jsons/bootcamps_data.json', 'r', encoding='utf-8') as json_file:
    programs = json.load(json_file)

# Load the CSV translations
translations = []
with open('Translation/bootcamps.csv', 'r', encoding='utf-8') as csv_file:
    reader = csv.DictReader(csv_file)
    for row in reader:
        translations.append(row)

# Function to split pipe-separated values from CSV into lists
def split_pipe_separated(value):
    return [item.strip() for item in value.split('|')] if value else []
# Fields that don't need translation (will be added at the end)
NON_TRANSLATABLE_FIELDS = [
    'isRegistrationOpen', 'isRegistrationClosed', 'registrationEndDate', 'language', 'video',
    'initiativeProCertificate', 'slug',
    'minimumAge', 'maximumAge', 'faqs'
]

# Mapping of original fields to their translation keys in CSV
FIELD_TRANSLATION_MAP = {
    'title': 'Title',
    'description': 'Description',
    # 'startDate': 'Start Date',
    # 'endDate': 'End Date',
    'initiativeCategoryName': 'Category',
    'initiativeScopeName': 'Scope',
    'goals': 'Goals',
    'features': 'Features',
    'requirements': 'Requirements',
    'locationName': 'Location',
    'locationText': 'Location',
    # 'startDateText': 'Start Date',
    # 'endDateText': 'End Date',
    'startTimeText': 'Start Time',
    'endTimeText': 'End Time',
    'durationText': 'Duration'
}

# Update each program with translations
for i, program in enumerate(programs):
    if i < len(translations):
        trans = translations[i]
        
        # Create a new ordered dictionary to maintain key order
        new_program = OrderedDict()
        
        # 1. Add each field with its translation
        for field, trans_key in FIELD_TRANSLATION_MAP.items():
            if field in program:
                # Add original field
                new_program[field] = program[field]
                
                # Add English translation
                if field in ['startDate', 'endDate']:
                    try:
                        date_str = trans[trans_key]
                        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
                        new_program[f'{field}_en'] = date_obj.strftime('%Y-%m-%d') + program[field][10:]
                    except:
                        new_program[f'{field}_en'] = program[field]
                elif field in ['goals', 'features', 'requirements']:
                    new_program[f'{field}_en'] = split_pipe_separated(trans[trans_key])
                else:
                    new_program[f'{field}_en'] = trans[trans_key]
        
        # 2. Add non-translatable fields at the end
        for field in NON_TRANSLATABLE_FIELDS:
            if field in program:
                new_program[field] = program[field]
        
        # 3. Add any remaining fields that weren't categorized
        for key in program:
            if key not in new_program and key not in FIELD_TRANSLATION_MAP and key not in NON_TRANSLATABLE_FIELDS:
                new_program[key] = program[key]
        
        # Replace the original program with our new ordered version
        programs[i] = new_program
# Save the updated JSON back to the same file
with open('Test/t.json', 'w', encoding='utf-8') as out_file:
    json.dump(programs, out_file, ensure_ascii=False, indent=2)

print("Translation complete. Original programs.json has been updated with English translations.")