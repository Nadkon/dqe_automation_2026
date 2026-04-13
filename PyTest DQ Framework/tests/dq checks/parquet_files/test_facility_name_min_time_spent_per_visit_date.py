"""
Description: Data Quality checks ...
Requirement(s): TICKET-1234
Author(s): Name Surname
"""

import pytest

class TestFacilityDataQuality:

    @pytest.mark.smoke
    def test_check_dataset_is_not_empty(self, target_data, data_quality_library):
        data_quality_library.check_dataset_is_not_empty(target_data)

    @pytest.mark.integrity
    def test_check_count(self, source_data, target_data, data_quality_library):
        data_quality_library.check_count(source_data, target_data)

    @pytest.mark.integrity
    def test_check_not_null_values(self, target_data, data_quality_library):
        columns_to_check = ['facility_name', 'visit_date', 'min_time_spent']
        data_quality_library.check_not_null_values(target_data, columns_to_check)

    @pytest.mark.uniqueness
    def test_check_uniqueness(self, target_data, data_quality_library):
        data_quality_library.check_duplicates(target_data)

    @pytest.mark.unmarked
    def test_check_data_completeness(self, source_data, target_data, data_quality_library):
        data_quality_library.check_data_completeness(source_data, target_data)



