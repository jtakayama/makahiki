import subprocess
import shlex
import re
import sys
import StringIO

def termination_string():
    """
    Gets the current system time and appends it to a termination notice.
    """
    # Capture console output from subprocess.check_call:
    normal_stdout = sys.stdout
    output_capturer = StringIO.StringIO()
    sys.stdout = output_capturer
    
    subprocess.check_call(["date"])
    
    # Switch back to standard I/O
    sys.stdout = normal_stdout
    time = output_capturer.getvalue().strip()
    
    end_time = "Script exiting at %s" % time
    return end_time

def install_and_capture(packagename, logfile):
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
    logfile.write("%s will be installed." % packagename)
    print "%s will be installed." % packagename
    # Capture console output:
    normal_stdout = sys.stdout
    output_capturer = StringIO.StringIO()
    sys.stdout = output_capturer
    try:
        # Install
        install_result = subprocess.check_call(shlex.split("yum install -y %" % packagename))
        # Any CalledProcessError would be raised at this point
        # Switch back to standard I/O
        sys.stdout = normal_stdout
        output = output_capturer.getvalue()
        logfile.write(output)
        print(output)
        # Clear the logfile buffer.
        logfile.flush()
        os.fsync(logfile)
        # Check result
        if install_result == 0:
            logfile.write("%s was successfully installed." % packagename)
            print "%s was successfully installed." % packagename
            success = True
    except subprocess.CalledProcessError as cpe:
        # Switch back to standard I/O
        sys.stdout = normal_stdout
        output = output_capturer.getvalue()
        logfile.write(output)
        print(output)
        # Clear the logfile buffer.
        logfile.flush()
        os.fsync(logfile)
        # Print and log the error message
        logfile.write("CalledProcessError: ")
        print "CalledProcessError: "
        logfile.write(cpe.output)
        print cpe.output
        closing = "Package %s did not install successfully." % packagename
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
             zlib-devel,\nbzip2-devel,\nopenssl-devel,\nncurses-devel,\n\
             sqlite-devel,\nreadline-devel,\ntk-devel,\nwget")
        print "This script will install these packages and their dependencies:\n\
             All packages in groupinstall of \"Development tools\",\n\
             zlib-devel,\nbzip2-devel,\nopenssl-devel,\nncurses-devel,\n\
             sqlite-devel,\nreadline-devel,\ntk-devel,\nwget"
        value = raw_input("Do you wish to continue (Y/n)? ")
        while value != "Y" and value != "n":
            logfile.write("Invalid option %s\n" % value)
            print "Invalid option %s\n" % value
            value = raw_input("Do you wish to continue (Y/n)? ")
        if value == "n":
            logfile.write("Do you wish to continue (Y/n)? %s\n" % value)
            logfile.write("Operation cancelled.")
            print "Operation cancelled.\n"
            return logfile
        elif value =="Y":
            logfile.write("Do you wish to continue (Y/n)? %s\n" % value)
            print "Installing packages..."
        
            # Groupinstall of "Development tools"
            logfile.write("\"Development tools\" packages will be groupinstalled.")
            print "\"Development tools\" packages will be groupinstalled."
            logfile.write("yum groupinstall -y \"Development tools\"")
            print "yum groupinstall -y \"Development tools\""
            # Capture console output:
            normal_stdout = sys.stdout
            output_capturer = StringIO.StringIO()
            sys.stdout = output_capturer
            # Run groupinstall
            groupinstall_result = subprocess.check_call(shlex.split("yum groupinstall -y \"Development tools\""))
            # Switch back to standard I/O
            sys.stdout = normal_stdout
            output = output_capturer.getvalue()
            logfile.write(output)
            print(output)
            # Clear the logfile buffer.
            logfile.flush()
            os.fsync(logfile)
            # Check result
            if groupinstall_result == 0:
                logfile.write("groupinstall \"Development tools\" completed successfully.")
                print "groupinstall \"Development tools\" completed successfully."
            
            # zlib-devel
            result = install_and_capture("zlib-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # bzip2-devel
            result = install_and_capture("bzip2-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # openssl-devel
            result = install_and_capture("openssl-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # ncurses-devel
            result = install_and_capture("ncurses-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile

            # sqlite-devel
            result = install_and_capture("sqlite-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # readline-devel
            result = install_and_capture("readline-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # tk-devel
            result = install_and_capture("tk-devel", logfile)
            success = result[0]
            logfile = result[1]
            if not success:
                return logfile
            
            # wget
            result = install_and_capture("wget", logfile)
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
        logfile.write("Warning: pre-installation setup for Python 2.7.3 did not complete successfully.")
        print "Warning: pre-installation setup for Python 2.7.3 did not complete successfully."
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile