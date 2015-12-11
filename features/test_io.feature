Feature: Reading empty DB File From Disk

    Background: Setup dblocpath for testing
        Given DB Temp Location needed

    Scenario: Ask to read empty file_key
        Given An empty file_key
        When I try to read file with empty file_key
        Then should receive ICAL_FILEKEY_IS_EMPTY exception

    Scenario: Ask to read invalid file_key
        Given An invalid file_key "invalid"
        When I try to read file with invalid file_key
        Then should receive ICAL_FILEKEY_UNKNOWN exception
 
    Scenario Outline: Ask to read missing DB files
        Given A file_key <file_key>
        When The file does not exist
        Then should receive IcalFileNotFound exception
 
        Given An valid file_key <file_key>
        When I try to read file having contents <content>
        Then should return the correct content string
 
    Examples: DB_Files
    | file_key | content |
    | q330     | q330_content |
    | auth     | auth_content |
    | lcq      | lcq_content |
    | calib    | calib_content |
    | sensor   | sensor_content |
    | detector | detector_ccontent |

#    Scenario Outline: Ask to read valid file_keys
