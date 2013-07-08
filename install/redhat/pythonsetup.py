import datetime
import subprocess
import shlex
import re
import sys
import StringIO
import os

def termination_string():
    """
    Gets the current system time and appends it to a termination notice.
    """
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    end_time = "Script exiting at %s\n" % time
    return end_time

def install(packagename, logfile):
    """
    Installs <packagename> and logs console output to <logfile>. Raises a 
    CalledProcessError if an error occurs.
    
    Parameters:
       1. packagename: The name of the package to be installed.
       2. logfile: The logfile to write output to.
       
    Returns the tuple "result."
    result[0] is True if the installation succeeded and False if it did not.
    result[1] is a reference to the logfile passed in as parameter 2.
    """
    success = False
    logfile.write("%s will be installed.\n" % packagename)
    print "%s will be installed.\n" % packagename
    try:
        # Install
        logfile.write("yum install -y %s" % packagename)
        print "yum install -y %s" % packagename
        install_result = subprocess.check_call(shlex.split("yum install -y %s" % packagename))
        # Any CalledProcessError would be raised at this point
        if install_result == 0:
            logfile.write("%s was successfully installed.\n" % packagename)
            print "%s was successfully installed.\n" % packagename
            success = True
    except subprocess.CalledProcessError as cpe:
        # Print and log the error message
        logfile.write("CalledProcessError: ")
        print "CalledProcessError: "
        logfile.write(cpe.output)
        print cpe.output
        closing = "Package %s did not install successfully.\n" % packagename
        logfile.write(closing)
        print closing
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        success = False
    # Return result tuple
    result = [success, logfile]
    return result

def run(logfile):
    """
    Uses yum to install dependencies needed to build Python 2.7.3 from 
    source. Writes its output to a logfile and prints it to the console. 
    It is left to the calling function to close the logfile, which is 
    returned.
    
    Intended to be run under Python 2.6.6 or later versions of 
    Python 2.6.
    
    Warning: This will install or update to the newest available 
    versions of all packages specified.
    
    Parameters:
        1.    logfile: The logfile to write output to. 
    """
    
    try:
        #Confirm that the user wants to continue.
        logfile.write("This script will install these packages and their dependencies:\n\
        All packages in groupinstall of \"Development tools\",\n\
        zlib-devel,\n\
        bzip2-devel,\n\
        openssl-devel,\n\
        ncurses-devel,\n\
        sqlite-devel,\n\
        readline-devel,\n\
        tk-devel,\n\
        wget")
        print "This script will install these packages and their dependencies:\n\
        All packages in groupinstall of \"Development tools\",\n\
        zlib-devel,\n\
        bzip2-devel,\n\
        openssl-devel,\n\
        ncurses-devel,\n\
        sqlite-devel,\n\
        readline-devel,\n\
        tk-devel,\n\
        wget"
        value = raw_input("Do you wish to continue (Y/n)? ")
        while value != "Y" and value != "n":
            logfile.write("Invalid option %s\n" % value)
            print "Invalid option %s\n" % value
            value = raw_input("Do you wish to continue (Y/n)? ")
        if value == "n":
            logfile.write("\nDo you wish to continue (Y/n)? %s\n" % value)
            logfile.write("Operation cancelled.\n")
            print "Operation cancelled.\n"
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile
        elif value =="Y":
            logfile.write("Do you wish to continue (Y/n)? %s\n" % value)
            print "Installing packages...\n"
        
            # Groupinstall of "Development tools"
            logfile.write("\"Development tools\" packages will be groupinstalled.\n")
            print "\"Development tools\" packages will be groupinstalled.\n"
            logfile.write("yum groupinstall -y \"Development tools\"\n")
            print "yum groupinstall -y \"Development tools\"\n"
            # Run groupinstall
            groupinstall_result = subprocess.check_call(shlex.split("yum groupinstall -y \"Development tools\"\n"))
            # Check result
            if groupinstall_result == 0:
                logfile.write("groupinstall \"Development tools\" completed successfully.\n")
                print "groupinstall \"Development tools\" completed successfully.\n"
            
            # zlib-devel
            result = install("zlib-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # bzip2-devel
            result = install("bzip2-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # openssl-devel
            result = install("openssl-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # ncurses-devel
            result = install("ncurses-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile

            # sqlite-devel
            result = install("sqlite-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # readline-devel
            result = install("readline-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # tk-devel
            result = install("tk-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # wget
            result = install("wget", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # Print a closing message
            closing = "\nInstallation script for Python-compiling dependencies has completed.\n"
            logfile.write(closing)
            print closing
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile

    except subprocess.CalledProcessError as cpe:
        logfile.write("CalledProcessError: ")
        print "CalledProcessError: "
        logfile.write(cpe.output)
        print cpe.output
        logfile.write("Warning: pre-installation setup for Python 2.7.3 did not complete successfully.\n")
        print "Warning: pre-installation setup for Python 2.7.3 did not complete successfully.\n"
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile
