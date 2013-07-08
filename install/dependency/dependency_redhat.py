import subprocess
import re
import os
import shlex

def rpm_check(packagename):
    """
    Uses "rpm -qa <packagename>" to check if a package is installed.
    It does not check the version. Returns True if it is installed, and 
    False if it is not.
    """
    rpm_regex = re.compile("(%s)(.)+(.x86_64)" % packagename)
    result = False
    rpm_qa = subprocess.check_output(shlex.split("rpm -qa %s" % packagename), stderr=subprocess.STDOUT)
    if rpm_regex.match(rpm_qa):
        result = True
    return result

def psql91_check():
    """
    Uses the "rpm -qa postgresql" command to check if the PostgreSQL version 
    is a version of PostgreSQL 9.1. Returns True if it is installed, and 
    False if it is not.
    """
    version = "postgresql-9.1."
    version_regex = re.compile("(%s)(.)+(.x86_64)")
    result = False
    rpm_qa = subprocess.check_output(shlex.split("rpm -qa postgresql"), stderr=subprocess.STDOUT)
    if version_regex.match(rpm_qa):
        result = True
    return result

def pip_check():
    """
    Checks if pip is installed on the system. Returns True if it is, 
    and False if it is not.
    """
    compare_result = False
    try:
        output = subprocess.check_output(shlex.split("pip --version"), stderr=subprocess.STDOUT)
        lines = output.split("\n")
        version_string = re.compile("(pip )(\d)+.(\d)+.(\d)")
        line0_result = version_string.match(lines[0])
        if not line0_result:
            compare_result = False
        else:
            compare_result = True
    except OSError as ose:
        # Assume not installed
        compare_result = False
    return compare_result

def virtualenvwrapper_check():
    """
    Checks if virtualenvwrapper is installed in the system. Returns True if 
    virtualenvwrapper is installed, and False if it is not.
    """
    compare_result = False
    try:
        output = subprocess.check_output(shlex.split("virtualenv --version"), stderr=subprocess.STDOUT)
        lines = output.split("\n")
        version_string = re.compile("(\d)+.(\d)+.(\d)")
        line0_result = version_string.match(lines[0])
        if not line0_result:
            compare_result = False
        else:
            compare_result = True
    except OSError as ose:
        # Assume not installed
        compare_result = False
    return compare_result

def termination_string():
    """
    Gets the current system time and appends it to a termination notice.
    """
    end_time = "Script exiting at %s" % subprocess.check_output(["date"], stderr=subprocess.STDOUT)
    return end_time

def run(arch, logfile):
    """
    Installs and configures some Makahiki dependencies by issuing 
    system commands. Writes its output to a logfile while printing 
    it to the console.
    
    The target OS is Red Hat Enterprise Linux (RHEL). x64 RHEL is supported.
    """
    
    # Boolean variables for each dependency
    git_installed = rpm_check("git")
    gcc_installed = rpm_check("gcc")
    python_setuptools_installed = rpm_check("python-setuptools")
    pip_installed = pip_check()
    python_imaging_installed = rpm_check("python-imaging")
    python_dev_installed = rpm_check("python-dev")
    libjpeg_dev_installed = rpm_check("libjpeg-dev")
    postgresql91_installed = psql91_check()
    # I do not know what the equivalent of libpq-dev is
    # libpq_dev_installed = rpm_check("libpq-dev")
    memcached_installed = rpm_check("memcached")
    libmemcached_installed = rpm_check("libmemcached-dev")
    virtualenvwrapper_installed = virtualenvwrapper_check()
    
    logfile.write("Not implemented.")
    print "Not implemented."
    return logfile
