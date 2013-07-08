import datetime
import subprocess
import shlex
import re
import sys
import os

def termination_string():
    """
    Gets the current system time and appends it to a termination notice.
    """
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    end_time = "Script exiting at %s\n" % time
    return end_time

def run_command(command, logfile):
    """
    Executes <command> and logs its output to <logfile>. Raises a 
    CalledProcessError if an error occurs. 
    Note that this does not log the console output of commands.
    
    Parameters:
       1. command: The command to be executed.
       2. logfile: The logfile to write output to.
       
    Returns the tuple "result."
    result[0] is True if the installation succeeded and False if it did not.
    result[1] is a reference to the logfile passed in as parameter 2.
    """
    success = False
    logfile.write("Attempting: " + command + "\n")
    print "Attempting: " + command + "\n"
    try:
        # Execute command
        command_result = subprocess.check_call(shlex.split(command))
        # Any CalledProcessError would be raised at this point
        # Check result
        if command_result == 0:
            logfile.write("Operation successful:\n%s" % command)
            print "Operation successful:\n%s" % command
            success = True
    except subprocess.CalledProcessError as cpe:
        # Print and log the error message
        logfile.write("CalledProcessError: ")
        print "CalledProcessError: "
        logfile.write(cpe.output)
        print cpe.output
        closing = "Operation failed:\n%s" % command
        logfile.write(closing)
        print closing
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        success = False
    except OSError as ose:
        logfile.write("OSError: ")
        print "OSError: "
        oserror_output = " errno: %s\n filename: %s\n strerror: %s\n" % (ose.errno, ose.filename, ose.strerror) 
        logfile.write(oserror_output)
        print oserror_output
        closing = "\nOperation failed:\n%s" % command
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
    Builds Python 2.7.3 from source as an altinstall.
    
    Parameters:
        1.    logfile: The logfile to write output to. 
    """
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    start_time = "Script starting at %s\n" % time
    logfile.write(start_time)
    print start_time
    
    compile_dir = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir + os.sep + "download")
    os.chdir(compile_dir)
    
    # Download source tarball
    #logfile.write("Downloading Python 2.7.3 source tarball.")
    #print "Downloading Python 2.7.3 source tarball."
    #result = run_and_capture("wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2", logfile)
    #success = result[0]
    #logfile = result[1]
    #if not success:
    #    return logfile
    
    # Check that the tarball exists
    #tarball_dir = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + \
    #                               os.sep + os.pardir + os.sep + "download" + \
    #                               os.sep + "Python-2.7.3.tar.bz2")  
    #try:
    #    python_stat = os.stat(tarball_dir) 
    #    if python_stat:
    #        output1 = "Python-2.7.3.tar.bz2 downloaded to %s" % tarball_dir
    #        logfile.write(output1)
    #        print output1
    #except OSError as tarball_error:
    #    closing = "Download failed: Could not find Python-2.7.3.tar.bz2 at %s" % tarball_dir
    #    logfile.write(closing)
    #    print closing
    #    end_time = termination_string()
    #    logfile.write(end_time)
    #    print end_time
    #    return logfile
    
    # Extract tarball
    #logfile.write("Extracting tarball.")
    #print "Extracting tarball."
    #result = run_command("tar xf Python-2.7.3.tar.bz2", logfile)
    #success = result[0]
    #logfile = result[1]
    #if not success:
    #    return logfile
    
    # Take ownership of the extracted directory
    extracted_dir = os.getcwd() + os.sep + "Python-2.7.3"
    logfile.write("Attempting: Taking ownership of %s" % extracted_dir)
    print "Attempting: Taking ownership of %s" % extracted_dir
    uname = os.getuid()
    os.chown(extracted_dir, uname, -1)
    logfile.write("Operation succeeded.")
    print ("Operation succeeded.")

    # Change to extracted directory
    logfile.write("Switching to %s\n" % extracted_dir)
    print "Switching to %s\n" % extracted_dir
    os.chdir(extracted_dir)
    logfile.write("Operation succeeded.")
    print ("Operation succeeded.")

    # Clear the logfile buffer.
    logfile.flush()
    os.fsync(logfile)
      
    # Configure and make altinstall
    result = run_command("./configure --prefix=/usr/local", logfile)
    success = result[0]
    logfile = result[1]
    if not success:
        return logfile

    # Code below this line does not work, and may break the OS if it changes the default python version
    
    result = run_command("make", logfile)
    success = result[0]
    logfile = result[1]
    if not success:
        return logfile
    
    result = run_command("make altinstall", logfile)
    success = result[0]
    logfile = result[1]
    if not success:
        return logfile

    # Print a closing message
    closing = "\nPython 2.7.3 altinstall setup is complete.\n"
    logfile.write(closing)
    print closing
    end_time = termination_string()
    logfile.write(end_time)
    print end_time
    return logfile
