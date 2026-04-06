import pytest
import re


def test_file_not_empty(csv_data):
    assert len(csv_data) > 1, "The file is empty"

@pytest.mark.validate_csv
@pytest.mark.xfail(reason='File may contain duplicates. It is known issue')
def test_duplicates(csv_data):
    rows = csv_data[1:]

    unique_rows = set(tuple(row) for row in rows)
    assert len(rows) == len(unique_rows), (
        f"The duplicated rows have been found! Total number of rows received: {len(rows)}, number of unique rows:"
        f" {len(unique_rows)}"
    )


@pytest.mark.validate_csv
def test_validate_schema(csv_data, expected_csv_schema, validate_schema):
    actual_schema = csv_data[0]
    validate_schema(actual_schema, expected_csv_schema)


@pytest.mark.validate_csv
@pytest.mark.skip(reason='This test is to be skipped due to issues with the age column')
def test_age_column_valid(csv_data):
    for row in csv_data[1:]: # we do not take the header
        age = int(row[2]) # age is the third column with index 2

        assert 0 <= age <= 100, f"Error: the age {age} is not in ragne 0-100 for id {row[0]}"

@pytest.mark.validate_csv
def test_email_column_valid(csv_data):
    email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    for row in csv_data[1:]:
        email = row[3]
        assert re.match(email_pattern, email), f"Incorrect email format: '{email}' the row with id {row[0]}"

@pytest.mark.parametrize("target_id, expected_status", [
    ("1", "False"),
    ("2", "True")
])
def test_active_players(csv_data, target_id, expected_status):
    target_row = None

    for row in csv_data:
        if row[0] == target_id:
            target_row = row
            break

    assert target_row is not None, f"The user with id {target_id} is not found"

    actual_status = target_row[4]
    assert actual_status == expected_status, (
        f"For id {target_id} the expected status is {expected_status}, "
        f"but the actual status is {actual_status}"
    )


def test_active_player(csv_data):
    target_row = None
    for row in csv_data[1:]:
        if row[0] == "2":
            target_row = row
            break

    assert target_row is not None, f"The user with id 2 is not found"

    actual_status = target_row[4]
    assert actual_status == "True", (
        f"For id 2 the expected status is True "
        f"but the actual status is {actual_status}"
    )
