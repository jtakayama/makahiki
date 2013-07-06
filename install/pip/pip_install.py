import os
import subprocess
import shlex
import re

def termination_string():
    """
    Gets the current system time and appends it to a termination notice.
    """
    end_time = "Script exiting at %s" % subprocess.check_output(["date"], stderr=subprocess.STDOUT)
    return end_time

def requirements_check(logfile):
    """
    Uses "pip freeze" to check that requirements were installed. Meant to be used after 
    running "pip install -r requirements.txt".
    """
    USER_HOME = subprocess.check_output(["echo $HOME"], stderr=subprocess.STDOUT, shell=True)
    # Remove newline from expected "/home/<username>\n"
    USER_HOME = USER_HOME[:-1]
    USER_PROJECT_HOME = USER_HOME + "/makahiki"
    # cd to makahiki directory so pip can find the requirements.txt file
    os.chdir(USER_PROJECT_HOME)
    requirements_txt = open(USER_PROJECT_HOME + "/requirements.txt", 'r')
    requirements_list = []
    nextline = requirements_txt.readline()
    # Build a list of requirements
    while nextline != "":
        # Only dependencies that have not been commented out should be checked
        if nextline[0] != '#':
            requirements_list.append(nextline.strip())
        nextline = requirements_txt.readline()
    # Read in list of currently installed requirements using pip freeze
    installed = subprocess.check_output(shlex.split("pip freeze"), stderr=subprocess.STDOUT)
    installed_list = installed.split("\n")
    # Search in list of installed requirements for matches to entries in requirements.txt
    for element in requirements_list:
        element_regex = re.compile("(.*)(%s)(.*)" % element)
        element_installed = False
        for element2 in installed_list:
            if element_regex.match(element2):
                element_installed = True
                break
	    else:
                continue
        # Avoid printing empty list elements
        if element != "":
            if element_installed:
                logfile.write("%s installed successfully." % element)
                print ("%s installed successfully." % element)
            else:
                logfile.write("Warning: %s not installed." % element)
                print ("Warning: %s not installed." % element)
    return logfile
    
def run(logfile):
    """
    Runs "pip install -r requirements.txt", logging output to the logfile.
    """
    try:
        USER_HOME = subprocess.check_output(["echo $HOME"], stderr=subprocess.STDOUT, shell=True) 
        # Remove newline from expected "/home/<username>\n"
        USER_HOME = USER_HOME[:-1]
        USER_PROJECT_HOME = USER_HOME + "/makahiki"
        # cd to makahiki directory so pip can find the requirements.txt file
        os.chdir(USER_PROJECT_HOME)
        pip_output = subprocess.check_output(["pip install -r requirements.txt"], stderr=subprocess.STDOUT, shell=True)
        logfile.write(pip_output)
        print(pip_output)
        # pip produces a lot of output. Clear the buffer before reading in anything else.
        logfile.flush()
        os.fsync(logfile)
        # Check that requirements were installed
        output1 = "\nChecking if dependencies in requirements.txt were installed:\n"
        logfile.write(output1)
        print output1
        logfile = requirements_check(logfile)
        # Print a closing message
        output2 = "\npip install script has completed.\n"
        logfile.write(output2)
        print output2
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile
    except subprocess.CalledProcessError as cpe:
        logfile.write("CalledProcessError: ")
        print "CalledProcessError: "
        logfile.write(cpe.output)
        print cpe.output
        logfile.write("pip did not successfully install requirements.")
        print "pip did not successfully install requirements."
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile 
