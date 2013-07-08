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

def run_and_capture(command, logfile):
    """
    Executes <command> and logs console output to <logfile>. Raises a 
    CalledProcessError if an error occurs.
    
    Parameters:
       1. command: The command to be executed.
       2. logfile: The logfile to write output to.
       
    Returns the tuple "result."
    result[0] is True if the installation succeeded and False if it did not.
    result[1] is a reference to the logfile passed in as parameter 2.
    """
    success = False
    logfile.write(command)
    print command
    # Capture console output:
    normal_stdout = sys.stdout
    output_capturer = StringIO.StringIO()
    sys.stdout = output_capturer
    try:
        # Execute command
        command_result = subprocess.check_call(shlex.split(command))
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
        if command_result == 0:
            logfile.write("Operation successful:\n%s" % command)
            print "Operation successful:\n%s" % command
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
        closing = "Operation failed:\n%s" % command
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
    compile_dir = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir + os.sep + "download")
    os.chdir(compile_dir)
    
    # Download source tarball
    logfile.write("Downloading Python 2.7.3 source tarball.")
    print "Downloading Python 2.7.3 source tarball."
    result = run_and_capture("wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2", logfile)
    success = result[0]
    logfile = result[1]
    if not success:
        return logfile
    
    # Check that the tarball exists
    tarball_dir = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + \
                                   os.sep + os.pardir + os.sep + "download" + \
                                   os.sep + "Python-2.7.3.tar.bz2")  
    try:
        python_stat = os.stat(tarball_dir) 
        if python_stat:
            output1 = "Python-2.7.3.tar.bz2 downloaded to %s" % tarball_dir
            logfile.write(output1)
            print output1
    except OSError as tarball_error:
        closing = "Download failed: Could not find Python-2.7.3.tar.bz2 at %s" % tarball_dir
        logfile.write(closing)
        print closing
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile
    
    # Extract tarball
    logfile.write("Extracting tarball.")
    print "Extracting tarball."
    result = run_and_capture("tar xf Python-2.7.3.tar.bz2", logfile)
    success = result[0]
    logfile = result[1]
    if not success:
        return logfile
    
    # Change to extracted directory
    result = run_and_capture("cd Python-2.7.3", logfile)
    success = result[0]
    logfile = result[1]
    if not success:
        return logfile
    
    # Configure and make altinstall
    result = run_and_capture("./configure --prefix=/usr/local", logfile)
    success = result[0]
    logfile = result[1]
    if not success:
        return logfile
    
    result = run_and_capture("make && make altinstall", logfile)
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