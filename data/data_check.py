import json
import logging


def read_from_output(file_path):
    """
    Read from output file.
    :param file_path: NDJSON file path.
    :return: List of json strings.
    """
    with open(file_path, 'r') as f:
        lines = f.readlines()

    return lines


def validate_data(record):
    """
    Convert json string to python dictionary. Return True of False for each json string.
    If return False, update the corrupted json with error type.
    :param record: json string.
    :return: Boolean, error type.
    """
    fields = ["symbol", "timestamp", "open_price", "close_price", "high", "low", "volume", "daily_price_change"]
    try:
        data = json.loads(record.strip())
        if data['high'] < data['low']:  # if stock low is greater than high
            data.update({'ERROR': 'LOGICAL'})
            return False, data
        for field in fields:
            if field not in data:  # check for missing field
                data.update({'ERROR': 'MISSING FIELD'})
                return False, data
        return True, None

    except json.JSONDecodeError:  # empty value return JSONDecodeError
        corrected_record = record.replace('None', '0').strip()
        data = json.loads(str(corrected_record))
        data.update({'ERROR': 'EMPTY VALUE'})
        return False, data


def integrity_check(list_dicts):
    """
    Perform integrity check on the list of json strings read from NDJSON file.
    Count the total number of data that passed integrity check.
    Return a list of records that failed the test.
    :param list_dicts: List of json strings.
    :return: - Str summary containing number of records passed integrity check, list[str] containing records that
    failed integrity check.
            - List[dict] that failed integrity check.
    """
    num_records = 0
    corrupt_data = []
    for record in list_dicts:
        valid, error_type = validate_data(record)
        if valid:
            num_records += 1
        else:
            corrupt_data.append(error_type)

    result = f'Total number of records passed integrity check: {num_records}\n' \
             f'Records failed validation check and to be further reviewed: \n{corrupt_data}'

    return result, corrupt_data


def output_corrupted_data(corrupt_data, output_file):
    """
    Write the list of corrupt data to json file for further review.
    :param corrupt_data: List of Dicts.
    :param output_file: Json file path.
    :return: None
    """
    with open(output_file, 'w') as json_file:
        json.dump(corrupt_data, json_file, indent=2)
    logging.info(f'corrupted data written to file: {json_file} for further review')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    stock_data = read_from_output('stock_data.json')
    result, corrupted_data = integrity_check(stock_data)
    print(result)
    output_corrupted_data(corrupted_data, 'dataToBeReviewed.json')