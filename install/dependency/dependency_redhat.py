import subprocess
import re
import os
import shlex

def run(arch, logfile):
    """
    Installs and configures some Makahiki dependencies by issuing 
    system commands. Writes its output to a logfile while printing 
    it to the console.
    
    The target OS is Red Hat Enterprise Linux (RHEL). x64 RHEL is supported.
    """
    
    # Boolean variables for each dependency
    git_installed = False
    gcc_installed = False
    python_setuptools_installed = False
    pip_installed = False
    python_imaging_installed = False
    pythondev_installed = False
    libjpeg_installed = False
    postgresql91_available = False
    postgresql91_installed = False
    libpqdev_installed = False
    memcached_installed = False
    virtualenvwrapper_installed = False
    
    logfile.write("Not implemented.")
    print "Not implemented."
    return logfile
