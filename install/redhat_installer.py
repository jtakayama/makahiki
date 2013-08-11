#!/usr/bin/env python
import sys
import os
import datetime
import subprocess
import shlex
import datestring_functions
import redhat.dependency_redhat
import pip.pip_install
import run_update_instance
import run_initialize_instance

def logfile_open(scripttype):
    """
    Returns an open logfile with a timestamp. It is left to the 
    calling function to write to the file and close it.
    
    This function will return None if an IOError occurs while 
    opening the file.
    
    Parameters:
        1. scripttype: A string describing the installation script
           that is being run.
    """
    # Build file path to logs directory based on location of this file
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
    
    logsdir = assembled_path + os.sep + "logs"
    prefix = "install_" + scripttype + "_"
    dt = datetime.datetime
    date_suffix = "null"
    logfile = None
    try:
        date_suffix = datestring_functions.datestring(dt)
        logfile_path = logsdir + os.sep + prefix + date_suffix + ".log"
        try:
            result = subprocess.check_call(shlex.split("touch %s" % logfile_path))
            if result == 0:
                logfile = open(logfile_path, 'a')
            elif result == 1:
                print "Could not create logfile at %s." % logfile_path
                print "Script will terminate."
                logfile = None
        except IOError as ioe:
            print "IOError:\n %s" % ioe
            print "Could not open logfile at %s for writing." % logfile_path
            print "Script will terminate."
            logfile = None
    except ValueError as ve:
        print "ValueError:\n %s" % ve
        print "Bad datetime object, could not generate logfile name."
        print "Script will terminate."
        logfile = None
    return logfile

def scriptrunner(scripttype, arch, logfile):
    """
    Chooses and runs an installation script, and supplies the
    logfile that the script will write its output to.
    
    Though not all scripts are OS-dependent, the "arch" 
    parameter is used to determine if the system is supported.
    
    Parameters:
        1. scripttype: The installation script that is being run. 
           Supported values: 
           "dependencies", "pip", "initialize_instance," "update_instance"
        2. arch: Architecture. RHEL / CentOS is supported for x64.
        3. logfile: The log file to pass to the installation script.
    """
    if arch != "x64":
        logfile.write("Unsupported architecture for RHEL / CentOS: %s" % arch)
        logfile.write("Script could not be completed.")
        print "Unsupported architecture for RHEL / CentOS: %s" % arch
        print "Script could not be completed."
    else: 
        if scripttype == "dependencies":
            logfile = redhat.dependency_redhat.run(arch, logfile)
        elif scripttype == "pip":
            logfile = pip.pip_install.run(logfile)
        elif scripttype == "initialize_instance":
            logfile = run_initialize_instance.run(logfile)
        elif scripttype == "update_instance":
            logfile = run_update_instance.run(logfile)
        else:
            logfile.write("Error: redhat_installer.py invoked with invalid command: %s" % scripttype)
            print "Error: redhat_installer.py invoked with invalid command: %s" % scripttype
    # After the function is done, return the logfile.
    return logfile

def main():
    if ((len(sys.argv) != 4) or (sys.argv[2] != "--arch")):
        print "Usage: redhat_installer.py < --dependencies | --pip | --initialize_instance | --update_instance > --arch < x64 >"
        print "--dependencies: Install Makahiki dependencies (software packages)."
        print "--pip: Install Makahiki local dependencies using pip."
        print "--initialize_instance: Initialize the Makahiki installation."
        print "--update_instance: Update the Makahiki installation."
        print "--arch: Architecture. This script only supports x64 for RHEL / CentOS."
    else:
        args = sys.argv[1:]
        scripttype = args[0].strip()[2:]
        arch = args[2].strip()
        
        logfile = logfile_open(scripttype)
        if logfile == None:
            exit(1)
        else:
            logfile = scriptrunner(scripttype, arch,logfile)
            logfile.close()

if __name__ == '__main__':
    main()