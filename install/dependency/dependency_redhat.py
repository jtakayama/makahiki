import subprocess
import re
import os
import shlex
import datetime

def rpm_check(packagename):
    """
    Uses "rpm -qa <packagename>" to check if a package is installed.
    It does not check the version. Returns True if it is installed, and 
    False if it is not.
    """
    rpm_regex = re.compile("(%s)(.)+(.x86_64)" % packagename + "-")
    result = False
    rpm_qa = subprocess.check_output(shlex.split("rpm -qa %s" % packagename), stderr=subprocess.STDOUT)
    if rpm_regex.match(rpm_qa):
        result = True
    return result

def python_package_check(packagename, expected_response):
    """
    Checks if <python-packagename> is installed as a site package 
    using <packagename> --version. Returns True if it is, and 
    False if it is not.
    
    Parameters:
    1. packagename: A string representing a Python package name.
       If the package is part of an altinstall, use its name 
       under the altinstall (e.g., a Python 2.7.3 altinstall 
       would check for "pip-2.7").
    2. expected_response: Allows for a package's --version command 
       to output a name different than <packagename>.
    """
    compare_result = False
    try:
        output = subprocess.check_output(shlex.split("%s --version" % packagename), stderr=subprocess.STDOUT)
        lines = output.split("\n")
        # Expects versions to have at least two parts (e.g., 3.0).
        version_string = re.compile("(%s )(\d)+(\.(\d)+)+" % packagename)
        line0_result = version_string.match(lines[0])
        if not line0_result:
            compare_result = False
        else:
            compare_result = True
    except OSError as ose:
        # Assume not installed
        compare_result = False
    return compare_result

def postgresql91_repocheck():
    """
    Checks if the pgdg-redhat91-9.1-5.noarch.rpm repo (pgdg91) is installed.
    Returns True if it is listed by yum repolist, and False if it not.
    """
    result = subprocess.check_output(shlex.split("yum repolist | grep pgdg91"), stderr=subprocess.STDOUT)
    lines = result.split("\n")
    repo_shortname = re.compile("(pgdg91)(.)*")
    repo_match = False
    for line in lines:
        linematch = repo_shortname.match(line)
        if linematch:
            repo_match = True
            break
    return repo_match
    
def termination_string():
    """
    Gets the current system time and appends it to a termination notice.
    """
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    end_time = "Script exiting at %s\n" % time
    return end_time

def run(arch, logfile):
    """
    Installs and configures some Makahiki dependencies by issuing 
    system commands. Writes its output to a logfile while printing 
    it to the console.
    
    The target OS is Red Hat Enterprise Linux (RHEL). x64 RHEL is supported.
    """
    # Write first line to file
    firstline = "Makahiki installation script for Red Hat Enterprise Linux %s" % arch
    logfile.write(firstline)
    print firstline
    
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    start_time = "Script started at %s\n" % time
    logfile.write(start_time)
    print start_time
    
    # Confirm that the user wants to continue.
    logfile.write("This script will install these packages and their dependencies:\n\
         git,\ngcc,\npython-setuptools (Python 2.6),\npython-setuptools (Python 2.7),\n\
         pip (Python 2.6),\npip (Python 2.7),\npython-imaging,\n\
         python-dev,\nlibjpeg-dev,\npostgresql91-server,\npostgresql91-contribs,\n\
         postgresql91-devel,\nmemcached,\nlibmemcached-dev,\nvirtualenvwrapper (Python 2.6)")
    print "This script will install these packages and their dependencies:\n\
         git,\ngcc,\npython-setuptools (Python 2.6),\npython-setuptools (Python 2.7),\n\
         pip (Python 2.6),\npip (Python 2.7),\npython-imaging,\n\
         python-dev,\nlibjpeg-dev,\npostgresql91-server,\npostgresql91-contribs,\n\
         postgresql91-devel,\nmemcached,\nlibmemcached-dev,\nvirtualenvwrapper (Python 2.6)"
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
        logfile.write("Starting dependency installation for RHEL %s.\nChecking for dependencies...\n" % arch)
        print "Starting dependency installation for RHEL %s.\nChecking for dependencies...\n" % arch
        
    
    # Boolean variables for each dependency
    # The assumption is that none of the Python 2.7 tools have been 
    # installed before.
    git_installed = rpm_check("git")
    gcc_installed = rpm_check("gcc")
    python_setuptools26 = rpm_check("python-setuptools")
    python_setuptools27 = python_package_check("easy_install-2.7", "setuptools")
    pip_installed26 = python_package_check("pip", "pip")
    pip_installed27 = python_package_check("pip-2.7", "pip")
    python_imaging_installed = rpm_check("python-imaging")
    python_devel_installed = rpm_check("python-devel")
    libjpeg_devel_installed = rpm_check("libjpeg-turbo-devel")
    postgresql91_repo = postgresql91_repocheck()
    postgresql91_server_installed = rpm_check("postgresql91-server")
    postgresql91_contrib_installed = rpm_check("postgresql91-contrib")
    postgresql91devel_installed = rpm_check("postgresql91-devel")
    memcached_installed = rpm_check("memcached")
    libmemcached_installed = rpm_check("libmemcached-devel")
    virtualenvwrapper26_installed = python_package_check("virtualenv")
    
    # git
    if git_installed:
        logfile.write("git is already installed.\n")
        print "git is already installed.\n" 
    else:
        logfile.write("git will be installed.\n")
        print ("git will be installed.\n")
        logfile.write("yum install -y git\n")
        print "yum install -y git\n"
    #    git_output = subprocess.check_output(["yum", "install", "-y", "git"], stderr=subprocess.STDOUT)
    #    logfile.write(git_output)
    #    print git_output
    #    git_installed = rpm_check("git")
    #    if git_installed:
    #        logfile.write("git installed successfully.")
    #        print "git installed successfully."
    #        # Flush the buffer and force a write to disk after each successful installation
    #        logfile.flush()
    #        os.fsync(logfile)
    #    else:
    #        logfile.write("git failed to install.")
    #        print "git failed to install."
    #        end_time = termination_string()
    #        logfile.write(end_time)
    #        print end_time
    #        return logfile 
    
    # gcc
    if gcc_installed:
        logfile.write("gcc is already installed.\n")
        print "gcc is already installed.\n" 
    else:
        logfile.write("gcc will be installed.\n")
        print ("gcc will be installed.\n")
        logfile.write("yum install -y gcc\n")
        print "yum install -y gcc\n"
    #    gcc_output = subprocess.check_output(["yum", "install", "-y", "gcc"], stderr=subprocess.STDOUT)
    #    logfile.write(gcc_output)
    #    print gcc_output
    #    gcc_installed = rpm_check("gcc")
    #    if gcc_installed:
    #        logfile.write("gcc installed successfully.")
    #        print "gcc installed successfully."
    #        # Flush the buffer and force a write to disk after each successful installation
    #        logfile.flush()
    #        os.fsync(logfile)
    #    else:
    #        logfile.write("gcc failed to install.")
    #        print "gcc failed to install."
    #        end_time = termination_string()
    #        logfile.write(end_time)
    #        print end_time
    #        return logfile 
    
    # python-setuptools
    if python_setuptools26:
        logfile.write("python-setuptools is already installed for Python 2.6.\n")
        print "python-setuptools is already installed for Python 2.6.\n" 
    else:
        logfile.write("python-setuptools will be installed for Python 2.6.\n")
        print ("python-setuptools will be installed for Python 2.6.\n")
        logfile.write("yum install -y python-setuptools\n")
        print "yum install -y python-setuptools\n"
        # TODO: Execute shell command here
    
    # python-setuptools, a.k.a. easy_install, for Python 2.7
    if python_setuptools27:
        logfile.write("python-setuptools is already installed for Python 2.7.\n")
        print "python-setuptools is already installed for Python 2.7.\n" 
    else:
        logfile.write("python-setuptools will be installed for Python 2.7.\n")
        print ("python-setuptools will be installed for Python 2.7.\n")
        logfile.write("python-setuptools (setuptools-0.8) will be downloaded.")
        print "python-setuptools (setuptools-0.8) will be downloaded."
        wget_command = "wget https://pypi.python.org/packages/source/s/setuptools/setuptools-0.8.tar.gz --no-check-certificate"
        logfile.write(wget_command + "\n")
        print wget_command + "\n"
        # TODO: Execute shell command here
        tar_command = "tar xf setuptools-0.8.tar.gz"
        logfile.write(tar_command + "\n")
        print tar_command + "\n"
        # TODO: Execute shell command here
        logfile.write("Switching to extracted setuptools-0.8 directory")
        print "Switching to extracted setuptools-0.8 directory"
        # TODO: Execute shell command here
        install_command = "/usr/local/bin/python2.7 setup.py install"
        logfile.write(install_command + "\n")
        print install_command + "\n"
        # TODO: Execute shell command here
        
    # pip for Python 2.6
    if pip_installed26:
        logfile.write("pip is already installed for Python 2.6.\n")
        print "pip is already installed for Python 2.6.\n" 
    else:
        logfile.write("pip will be installed for Python 2.6.\n")
        print ("pip will be installed for Python 2.6.\n")
        logfile.write("easy_install pip\n")
        print "easy_install pip\n"
        # TODO: Execute shell command here
        
    # pip for Python 2.7   
    if pip_installed27:
        logfile.write("pip is already installed for Python 2.7.\n")
        print "pip is already installed for Python 2.7.\n" 
    else:
        logfile.write("pip will be installed for Python 2.7.\n")
        print ("pip will be installed for Python 2.7.\n")
        logfile.write("/usr/local/bin/easy_install-2.7 pip\n")
        print "/usr/local/bin/easy_install-2.7 pip\n"
        # TODO: Execute shell command here

    logfile.write("Beginning installation of Python Imaging Library components python-imaging, python-devel, and libjpeg-devel.\n")
    print "Beginning installation of Python Imaging Library components python-imaging, python-devel, and libjpeg-devel.\n"
        
    # python-imaging    
    if python_imaging_installed:
        logfile.write("python-imaging is already installed.\n")
        print "python-imaging is already installed.\n" 
    else:
        logfile.write("python-imaging will be installed.\n")
        print ("python-imaging will be installed.\n")
        logfile.write("yum install -y python-imaging\n")
        print "yum install -y python-imaging\n"
        # TODO: Execute shell command here

    # python-devel
    if python_devel_installed:
        logfile.write("python-devel is already installed.\n")
        print "python-devel is already installed.\n" 
    else:
        logfile.write("python-devel will be installed.\n")
        print ("python-devel will be installed.\n")
        logfile.write("yum install -y python-devel\n")
        print "yum install -y python-devel\n"
        # TODO: Execute shell command here    
        
    # libjpeg-devel
    if libjpeg_devel_installed:
        logfile.write("libjpeg-devel (libjpeg-turbo-devel) is already installed.\n")
        print "libjpeg-devel (libjpeg-turbo-devel) is already installed.\n" 
    else:
        logfile.write("libjpeg-devel (libjpeg-turbo-devel) will be installed.\n")
        print ("libjpeg-devel (libjpeg-turbo-devel) will be installed.\n")
        logfile.write("yum install -y libjpeg-devel\n")
        print "yum install -y libjpeg-devel\n"
        # TODO: Execute shell command here

    # Code to check for existence of libraries goes here
    logfile.write("Checking for Python Imaging Library shared libraries.\n")
    print "Checking for Python Imaging Library shared libraries.\n"
    try:
        libjpeg_stat = os.stat("/usr/lib64/libjpeg.so")
        if libjpeg_stat:
            output1 = "Found libjpeg.so at /usr/lib64/libjpeg.so\n"
            logfile.write(output1)
            print output1
    except OSError as libjpeg_error:
        error1 = "Error: Could not find libjpeg.so in /usr/lib64 .\n"
        error2 = "Python Imaging Library-related packages may not have installed properly.\n"
        logfile.write(error1)
        logfile.write(error2)
        print error1
        print error2
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile

    try:
        libjpeg_stat = os.stat("/usr/lib64/libz.so")
        if libjpeg_stat:
            output1 = "Found libz.so at /usr/lib64/libz.so\n"
            logfile.write(output1)
            print output1
    except OSError as libjpeg_error:
        error1 = "Error: Could not find libz.so in /usr/lib64 .\n"
        error2 = "Python Imaging Library-related packages may not have installed properly.\n"
        logfile.write(error1)
        logfile.write(error2)
        print error1
        print error2
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile 
    
    logfile.write("Installation of Python Imaging Library components is complete.\n")
    print "Installation of Python Imaging Library components is complete.\n"
    
    if postgresql91_repo:
        repo_string = "The repo at http://yum.postgresql.org/9.1/redhat/rhel-6-x86_64/pgdg-redhat91-9.1-5.noarch rpm\n is already installed."
        logfile.write(repo_string)
        print repo_string
    else:
        # Install Postgresql RPM
        logfile.write("Adding the PostgreSQL repo...\n")
        print "Adding the PostgreSQL repo...\n"
        pg_repo_command = "rpm -i http://yum.postgresql.org/9.1/redhat/rhel-6-x86_64/pgdg-redhat91-9.1-5.noarch.rpm"
        logfile.write(pg_repo_command + "\n")
        print pg_repo_command + "\n"
        # TODO: Execute shell command here
        # TODO: Check for repo after installation
    
    # postgresql91-server
    if postgresql91_server_installed:
        logfile.write("postgresql91-server is already installed.\n")
        print "postgresql91-server is already installed.\n"
    else:
        logfile.write("postgresql91-server will be installed.\n")
        print ("postgresql91-server will be installed.\n")
        logfile.write("yum install -y postgresql91-server\n")
        print "yum install -y postgresql91-server\n"
        # TODO: Execute shell command here
    
    # postgresql-91-contrib
    if postgresql91_contrib_installed:
        logfile.write("postgresql91-contrib is already installed.\n")
        print "postgresql91-contrib is already installed.\n"   
    else:
        logfile.write("postgresql91-contrib will be installed.\n")
        print ("postgresql91-contrib will be installed.\n")
        logfile.write("yum install -y postgresql91-contrib\n")
        print "yum install -y postgresql91-contrib\n"
        # TODO: Execute shell command here
    
    # postgresql91-devel
    if postgresql91devel_installed:
        logfile.write("postgresql91-devel is already installed.\n")
        print "postgresql91-devel is already installed.\n"   
    else:
        logfile.write("postgresql91-devel will be installed.\n")
        print ("postgresql91-devel will be installed.\n")
        logfile.write("yum install -y postgresql91-devel\n")
        print "yum install -y postgresql91-devel\n"
        # TODO: Execute shell command here  
        
    # memcached
    if memcached_installed:
        logfile.write("memcached is already installed.\n")
        print "memcached is already installed.\n"   
    else:
        logfile.write("memcached will be installed.\n")
        print ("memcached will be installed.\n")
        logfile.write("yum install -y memcached\n")
        print "yum install -y memcached\n"
        # TODO: Execute shell command here  
        
    # libmemcached-devel
    if libmemcached_installed:
        logfile.write("libmemcached-devel is already installed.\n")
        print "libmemcached-devel is already installed.\n"   
    else:
        logfile.write("libmemcached-devel will be installed.\n")
        print ("libmemcached-devel will be installed.\n")
        logfile.write("yum install -y libmemcached-devel\n")
        print "yum install -y libmemcached-devel\n"
        # TODO: Execute shell command here  
        
    # virtualenvwrapper for Python 2.6
    if virtualenvwrapper26_installed:
        logfile.write("virtualenvwrapper is already installed for Python 2.6.\n")
        print "virtualenvwrapper is already installed for Python 2.6.\n" 
    else:
        logfile.write("virtualenvwrapper will be installed for Python 2.6.\n")
        print ("virtualenvwrapper will be installed for Python 2.6.\n")
        logfile.write("easy_install virtualenvwrapper\n")
        print "easy_install virtualenvwrapper\n"
        # TODO: Execute shell command here
    
    logfile.write("Not implemented.\n")
    print "Not implemented.\n"
    end_time = termination_string()
    logfile.write(end_time)
    print end_time
    return logfile
