"""Provides the view of the widget."""

from apps.managers.player_mgr import player_mgr
import csv

def extension_check(filename):
    """Checks the file extension against a whitelist of file extensions.
       Note that this will not catch a file that has been renamed with a CSV extension."""
    
    extension_whitelist = ["csv"]
    filename_split = filename.split(".")
    invalid_string = "Invalid file extension"
    result = invalid_string
    if len(filename_split) == 2:
        if filename_split[1] in extension_whitelist:
            result = True
        else:
            result = False
    else:
        result = False
    return result

def content_type_check(infile):
    """Checks the file's MIME type against a whitelist of mime types.
       Note that this will not catch a file that has been renamed with a CSV extension."""
    
    content_type_whitelist = ["application/vnd.ms-excel","text/csv"]
    result = False
    content_type = infile.content_type
    if content_type in content_type_whitelist:
        result = True
    else:
        result = False
    return result

def test_first_line(infile):
    """Check the first line in a CSV file to see if the file can be read as a CSV file."""

    result = False
    reader = csv.reader(infile)
    
    try:
        for items in reader:
            # Lines for normal users have 6 items
            if (len(items) == 6):
                result = True
            # Lines for RA users have 7 items
            elif (len(items) == 7) and (items[6].strip().lower() == "ra"):
                result = True
            # Failure: line has too many items.
            else:
                result = False
                break
    # Failure: cannot read file or index out of bounds.
    except IndexError:
        result = False
    return result

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
        
    load_count = -1
    # Default error message (replaced by other strings later in this function)
    file_upload_result = "No file uploaded."
    
    infile = request.FILES.get("csvfile")
    if infile != None:
        # Validate file type and extension
        extension_check_result = extension_check(infile.name)
        content_type_check_result = content_type_check(infile)
        if extension_check_result and content_type_check_result:
            if test_first_line(infile):
                # Create users
                try:
                    load_count = player_mgr.bulk_create_players(infile)
                    # Overwrite the default value, which begins the error message
                    file_upload_result = "Valid"
                # This error occurs when the CSV file cannot be read by bulk_create_players
                except IndexError:
                    load_count = -1
                    file_upload_result = "Could not parse CSV file."
            else:
                load_count = -1
                file_upload_result = "Could not parse CSV file."
        else:
            load_count = -1
            # Assemble the error message by appending return values from validation functions
            if (not extension_check_result) or (not content_type_check_result):
                file_upload_result = "File is not a CSV file."
    else:
        load_count = -1
        file_upload_result = "No file uploaded."
    
    return {
        "load_count": load_count,
        "file_upload_result": file_upload_result
    }
