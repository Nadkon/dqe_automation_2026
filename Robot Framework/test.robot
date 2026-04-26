*** Settings ***
Documentation     Data Quality Comparison: HTML vs Parquet
Library           SeleniumLibrary
Library           helper.py
Test Teardown     Close Browser

*** Variables ***
${REPORT_FILE}       ${CURDIR}/report.html/report.html
${PARQUET_FOLDER}    ${CURDIR}/parquet_data/facility_type_avg_time_spent_per_visit_date
${FILTER_DATE}       2026-03-14  # take any date from the report

${BROWSER}           chrome

*** Test Cases ***
Verify Custom HTML Table Matches Parquet Dataset
    [Documentation]    Extracts div-based table and compares with Parquet.

    # 1. Report opening
    Open Browser    file:///${REPORT_FILE}    ${BROWSER}
    Maximize Browser Window
    Wait Until Element Is Visible    class:table    timeout=10s

    # 2. Access to the driver
    ${sel_lib}=    Get Library Instance    SeleniumLibrary

    # 3. Data extracting from  HTML and filtering by date
    ${df_html}=    Get Table Data From Elements    ${sel_lib.driver}    ${FILTER_DATE}

    # 4. Data extracting from  Parquet and filtering by date
    ${df_parquet}=    Read Parquet With Filter    ${PARQUET_FOLDER}    ${FILTER_DATE}

    # 5. Comparing
    ${status}    ${mismatch}=    Compare Dataframes    ${df_html}    ${df_parquet}

    IF    ${status} == False
        Fail    Mismatch detected:\n${mismatch}
    END

    Log    Test Passed: All records match.
