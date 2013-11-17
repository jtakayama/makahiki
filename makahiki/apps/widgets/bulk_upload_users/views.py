"""Provides the view of the widget."""

from apps.managers.player_mgr import player_mgr

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

def supply(request, page_name):
    """ supply view_objects for widget rendering."""
    _ = request
    _ = page_name
        
    load_count = -1
    # This is the start of an error message
    file_upload_result = "No file uploaded."
    
    infile = request.FILES.get("csvfile")
    if infile != None:
        # Validate file type and extension
        extension_check_result = extension_check(infile.name)
        content_type_check_result = content_type_check(infile)
        if extension_check_result and content_type_check_result:
            # Create users
            try:
                load_count = player_mgr.bulk_create_players(infile)
                # Overwrite the default value, which begins the error message
                file_upload_result = "Valid"
            # This error occurs when the CSV file cannot be read by bulk_create_players
            except IndexError:
                file_upload_result = "Could not parse CSV file."
        else:
            load_count = -1
            # Assemble the error message by appending return values from validation functions
            if (not extension_check_result) or (not content_type_check_result):
                file_upload_result = "File is not a CSV file."
    else:
        load_count = -1
        # Append to error message
        file_upload_result = "No file uploaded."
    
    return {
        "load_count": load_count,
        "file_upload_result": file_upload_result
    }
