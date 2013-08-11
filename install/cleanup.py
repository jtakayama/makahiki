import os
import datetime.datetime
import sys
import stat
import shutil.rmtree

def termination_string():
    """
    Gets the current system time and appends it to a termination notice.
    """
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    end_time = "Script exiting at %s\n" % time
    return end_time

def run(logfile):
    """
    Erases all files and directories in makahiki/install/download 
    except for download_readme.txt.
    Parameters:
        1. logfile: A file to log output to.
    """
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    start_time = "Makahiki downloads cleanup script started at %s\n" % time
    logfile.write(start_time)
    print start_time
    try:
        # Build file path to "download" directory based on location of this file
        runpath = os.path.dirname(os.path.realpath(__file__))
        pathdirs = runpath.split(os.sep)
        assembled_path = ""
        i = 0
        # Assume the last part is the filename
        while i < len(pathdirs):
            if i == 0:
                assembled_path = pathdirs[i]
            else:
                assembled_path = assembled_path + os.sep + pathdirs[i]
            i = i + 1
        downloads_dir = assembled_path + os.sep + "download"
        all_files = os.listdir(downloads_dir)
        j = len(all_files)
        delete_list = []
        # Build list of files. Exclude project file download_readme.txt
        for entry in all_files:
            if entry != "download_readme.txt":
                delete_list.append(downloads_dir + os.sep + entry)
        if len(delete_list) == 0:
            logfile.write("Nothing to remove.\n")
            print "Nothing to remove."
        else:
            logfile.write("Cleaning up...\n")
            print "Cleaning up..."
            for entry in delete_list:
                mode = os.stat(entry).st_mode
                if stat.S_ISREG(mode):
                    logfile.write("Removing file: %s.\n" % entry)
                    print "Removing file: %s." % entry
                    os.remove(entry)
                elif stat.S_ISDIR(mode):
                    logfile.write("Removing directory recursively: %s." % entry)
                    print "Removing directory recursively: %s." % entry
                    shutil.rmtree(entry)
            logfile.write("Done.\n")
            print "Done."
        closing = "\nMakahiki downloads cleanup script has completed.\n"
        logfile.write(closing)
        print closing
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile
    # Many of the os.* commands raise OSErrors.
    except OSError as ose:
        logfile.write("OSError: ")
        print "OSError: "
        oserror_output = " errno: %s\n filename: %s\n strerror: %s\n" % (ose.errno, ose.filename, ose.strerror) 
        logfile.write(oserror_output)
        print oserror_output
        logfile.write("Warning: Makahiki downloads cleanup did not complete successfully.\n")
        print "Warning: Makahiki downloads cleanup did not complete successfully."
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile
        