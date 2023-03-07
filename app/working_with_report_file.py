import csv
import json


from datetime import datetime


def structure_date_by_iso_format(date: str | None):
    if date is None:
        return None
    date = [int(elem) for elem in date.split('.')]
    if len(date) == 2:
        return None
    date.reverse()
    iso_date_format = datetime(year=date[0], month=date[1], day=date[2]).date().isoformat()
    return iso_date_format


def structure_data_by_fields(data: list):
    structure_data = {}
    report = []
    # items = data['response']['items']
    items = data
    for item in items:
        structure_data['first_name'] = item['first_name'] if item['first_name'] else None
        structure_data['last_name'] = item['last_name'] if item['last_name'] else None
        structure_data['country'] = item['country']['title'] if item.get('country') else None
        structure_data['city'] = item['city']['title'] if item.get('city') else None
        structure_data['birthdate'] = structure_date_by_iso_format(item.get('bdate'))
        structure_data['sex'] = "male" if item['sex'] == 2 else "female"
        report.append(structure_data.copy())
    return report


def write_data_to_file(friends_data: list, file_path_and_name: str, file_format: str):
    with open(f"{file_path_and_name}.{file_format}", 'w', encoding="utf-8") as file:
        if file_format == 'json':
            json.dump(friends_data, file, indent=4, ensure_ascii=False)
        elif file_format == 'csv':
            writer = csv.writer(file)
            writer.writerow(['first_name', 'last_name', 'country', 'city', 'birthdate', 'sex'])
            for friend_data in friends_data:
                writer.writerow(friend_data.values())
        elif file_format == 'tsv':
            for friend_data in friends_data:
                line = [elem if elem else '' for elem in friend_data.values()]
                line = '\t'.join(line)
                file.write(f"{line}\n")


def sort_friends_data_by_name(unsorted_items: list) -> list:
    sorted_items = sorted(unsorted_items, key=lambda k: k['first_name'])
    return sorted_items


def create_report(friends_data: list, file_path_and_name: str, file_format: str):
    structure_friends_data = structure_data_by_fields(friends_data)
    sorted_friends_data = sort_friends_data_by_name(structure_friends_data)
    allowed_formats = ["json", "csv", "tsv"]
    if file_format in allowed_formats:
        write_data_to_file(sorted_friends_data, file_path_and_name, file_format)
    else:
        return {'error': f'Формат файла {file_format} не предусмотрен в приложении. '
                         f'Доступные форматы отчета {",".join(allowed_formats)}.'}
