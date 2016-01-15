Feature: Reading and writting ical DB cfg files from/to Disk

    Background: Setup dblocpath for testing
        Given DB Temp Location needed

    Scenario: Ask to read empty file_key
        Given An empty file_key to read
        When I try to read file with empty file_key
        Then should receive ICAL_FILEKEY_IS_EMPTY exception on read

    Scenario: Ask to read invalid file_key
        Given An invalid file_key "invalid" to read
        When I try to read file with invalid file_key
        Then should receive ICAL_FILEKEY_UNKNOWN exception on read
 
    Scenario Outline: Ask to read DB files
        Given A file_key <file_key> to read
        When The file does not exist
        Then should receive IcalFileNotFound exception
 
        Given An valid file_key <file_key> to read
        When I try to read file having contents <content>
        Then should return the correct content string
 
    Examples: READ_DB_Files
    | file_key | content |
    | q330     | q330_content |
    | auth     | auth_content |
    | lcq      | lcq_content |
    | calib    | calib_content |
    | sensor   | sensor_content |
    | detector | detector_ccontent |


    Scenario Outline: Ask to write DB files
        Given A file_key <wfile_key> to write
        When and IOError is raised
        Then should receive IcalWriteError exception
 
        Given a valid file_key <wfile_key> to write
        When I try to write file having contents <wcontent>
        Then should write the correct string


    Examples: WRITE_DB_Files
    | wfile_key | wcontent |
    | q330     | q330_content |
    | auth     | auth_content |


    Scenario: Ask to write with empty file_key
        Given An empty file_key to write
        Then should receive ICAL_FILEKEY_IS_EMPTY exception on write

    Scenario: Ask to write invalid file_key
        Given An invalid file_key "invalid" to write
        Then should receive ICAL_FILEKEY_UNKNOWN exception on write
 
