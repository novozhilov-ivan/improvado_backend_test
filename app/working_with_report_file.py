import csv
import json

from datetime import datetime


def structure_date_by_iso_format(date: str | None) -> str | None:
    if date is None:
        return None
    date = [int(elem) for elem in date.split('.')]
    if len(date) == 2:
        return None
    date.reverse()
    iso_date_format = datetime(year=date[0], month=date[1], day=date[2]).date().isoformat()
    return iso_date_format


def structure_data_by_fields(data: list) -> list:
    structure_data = {}
    report = []
    items = data
    for item in items:
        structure_data['first_name'] = item['first_name'] if item.get('first_name') else None
        structure_data['last_name'] = item['last_name'] if item.get('last_name') else None
        structure_data['country'] = item['country']['title'] if item.get('country') else None
        structure_data['city'] = item['city']['title'] if item.get('city') else None
        structure_data['birthdate'] = structure_date_by_iso_format(item.get('bdate'))
        structure_data['sex'] = "male" if item['sex'] == 2 else "female"
        report.append(structure_data.copy())
    return report


def write_data_to_file(friends: list, file_path_and_name: str, file_format: str) -> None:
    with open(f"{file_path_and_name}.{file_format}", 'w', encoding="utf-8") as file:
        if file_format == 'json':
            json.dump(friends, file, indent=4, ensure_ascii=False)
        elif file_format == 'csv':
            writer = csv.writer(file)
            writer.writerow(friends[0].keys())
            writer.writerows(map(dict.values, friends))
        elif file_format == 'tsv':
            for friend in friends:
                line = [elem if elem else '' for elem in friend.values()]
                line = '\t'.join(line)
                file.write(f"{line}\n")


def sort_friends_data_by_name(unsorted_items: list) -> list:
    sorted_items = sorted(unsorted_items, key=lambda k: k['first_name'])
    return sorted_items


def create_report(friends_data: list, file_path_and_name: str, file_format: str) -> None:
    structure_friends_data = structure_data_by_fields(friends_data)
    sorted_friends_by_name = sort_friends_data_by_name(structure_friends_data)
    write_data_to_file(sorted_friends_by_name, file_path_and_name, file_format)

