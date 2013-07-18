import subprocess
import re
import os
import shlex
import datetime
import commands

# This script needs to be run with sudo. Since this causes the 
# shell to default back to the default version of Python
# (2.6.6 on RHEL 6 / CentOS 6), the script uses the "commands" 
# module to replace functionality missing from 2.6.6's version 
# of the subprocess module.

def rpm_check(packagename):
    """
    Uses "rpm -q <packagename>" to check if a package is installed.
    It does not check the version. Returns True if it is installed, and 
    False if it is not.
    """
    rpm_regex = re.compile("(%s)(.)+(\.)(.)+" % packagename)
    result = False
    try:
        tuple = commands.getstatusoutput("rpm -q %s" % packagename)
        status = tuple[0]
        output = tuple[1]
        if status == 0:
            output2 = output.split("\n")
            if rpm_regex.match(output2[0]):
                result = True
            else:
                result = False
        elif status == 1:
            result = False
    # Assume not installed
    except OSError as ose:
        result = False
    except CalledProcessError as cpe:
        result = False
    return result

def python_package_check(packagename, expected_response):
    """
    Checks if <python-packagename> is installed as a site package 
    using <packagename> --version. Returns True if it is, and 
    False if it is not. The <packagename> may need to be a 
    filepath if it refers to a package that is installed under 
    an altinstall.
    
    It assumes that the version is represented by <packagename> 
    followed by at least two integer sequences separated 
    by a single period (e.g., "foo 11.11.11").
    
    Parameters:
    1. packagename: A string representing a Python package name.
       If the package is part of an altinstall, use its name 
       under the altinstall (e.g., a Python 2.7.3 altinstall 
       would check for "pip-2.7").
    2. expected_response: Allows for a package's --version command 
       to output a name different than <packagename>.
    """
    compare_result = False
    # Expects versions to have at least two parts (e.g., 3.0).
    version_string = re.compile("(%s )(\d)+(\.(\d)+)+(.)*" % expected_response)
    try:
        tuple = commands.getstatusoutput("%s --version" % packagename)
        status = tuple[0]
        output = tuple[1]
        # result = subprocess.check_call(shlex.split("%s --version" % packagename),stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if status == 0:
            output2 = output.split("\n")
            if version_string.match(output2[0]):            
                compare_result = True
            else:
                compare_result = False
    # Assume not installed
    except OSError as ose:
        compare_result = False
    except CalledProcessError as cpe:
        compare_result = False
    return compare_result

def postgresql91_repocheck():
    """
    Checks if the pgdg-redhat91-9.1-5.noarch.rpm repo (pgdg91) is installed.
    Returns True if it is listed by yum repolist, and False if it not.
    """
    repo_match = False
    repo_shortname = re.compile("(pgdg91)(.)*")
    try:
        tuple = commands.getstatusoutput("yum repolist | grep pgdg91")
        status = tuple[0]
        output = tuple[1]
        output2 = output.split("\n")
        for line in output2:
            linematch = repo_shortname.match(line)
            if linematch:
                repo_match = True
                break
    # Assume not installed
    except OSError as ose:
        repo_match = False
    return repo_match

def termination_string():
    """
    Gets the current system time and appends it to a termination notice.
    """
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    end_time = "Script exiting at %s\n" % time
    return end_time

def yum_install(packagename, logfile):
    """
    Installs <packagename> with "yum install -y <packagename>" and then 
    checks whether or not the package installed correctly. Output is logged to 
    the logfile.
    
    Parameters:
        1. packagename: A string with the name of the package to be installed.
        2. logfile: The file to write output to.
    Returns a tuple, result:
    result[0] is True if the installation succeeded and False if it did not.
    result[1] is a reference to the logfile passed in as parameter 2.
    """
    success = False
    logfile.write("%s will be installed.\n" % packagename)
    print ("%s will be installed.\n" % packagename)
    logfile.write("yum install -y %s\n" % packagename)
    print "yum install -y %s\n" % packagename
    try:
        tuple = commands.getstatusoutput("yum install -y %s" % packagename)
        status = tuple[0]
        output = tuple[1]
        # Print output line by line
        output2 = output.split("\n")
        for line in output2:
            logfile.write(line + "\n")
            print line
        # Check if RPM was installed
        is_installed = rpm_check(packagename)
        if is_installed:
            logfile.write("%s installed successfully.\n" % packagename)
            print "%s installed successfully.\n" % packagename
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
            success = True
        else:
            logfile.write("Package %s failed to install.\n" % packagename)
            print "Package %s failed to install.\n" % packagename
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            success = False
        return [success, logfile]
    except subprocess.CalledProcessError as cpe:
        # Print and log the error message
        logfile.write("CalledProcessError: ")
        print "CalledProcessError: "
        logfile.write(cpe.output)
        print cpe.output
        closing = "\nPackage %s failed to install.\n" % packagename
        logfile.write(closing)
        print closing
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        success = False
        return [success, logfile]
    except OSError as ose:
        logfile.write("OSError: ")
        print "OSError: "
        oserror_output = " errno: %s\n filename: %s\n strerror: %s\n" % (ose.errno, ose.filename, ose.strerror) 
        logfile.write(oserror_output)
        print oserror_output
        closing = "\nPackage %s failed to install.\n" % command
        logfile.write(closing)
        print closing
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        success = False
        return [success, logfile] 

def run(arch, logfile):
    """
    Installs and configures some Makahiki dependencies by issuing 
    system commands. Writes its output to a logfile while printing 
    it to the console.
    
    The target OS is Red Hat Enterprise Linux (RHEL). x64 RHEL is supported.
    """
    pythonpath = "/opt/rh/python27/root/usr/bin"
    
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
    logfile.write("This script will add PostgreSQL's pgdg91 repository to the system.\n")
    print "This script will add PostgreSQL's pgdg91 repository to the system.\n"
    dependencies_list = "This script will install these packages and their dependencies:\n\
         git,\n\
         gcc,\n\
         pip (Python 2.7),\n\
         python-imaging,\n\
         python-devel,\n\
         libjpeg-devel,\n\
         postgresql91-server,\n\
         postgresql91-contribs,\n\
         postgresql91-devel,\n\
         memcached,\n\
         libmemcached-devel,\n"
    logfile.write(dependencies_list)
    print dependencies_list
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
    git_installed = rpm_check("git")
    gcc_installed = rpm_check("gcc")
    pip_installed27 = python_package_check(pythonpath + os.sep + "pip-2.7", "pip")
    python_imaging_installed = rpm_check("python-imaging")
    python_devel_installed = rpm_check("python-devel")
    libjpeg_devel_installed = rpm_check("libjpeg-turbo-devel")
    postgresql91_repo = postgresql91_repocheck()
    postgresql91_server_installed = rpm_check("postgresql91-server")
    postgresql91_contrib_installed = rpm_check("postgresql91-contrib")
    postgresql91devel_installed = rpm_check("postgresql91-devel")
    memcached_installed = rpm_check("memcached")
    libmemcached_installed = rpm_check("libmemcached-devel")
    
    # git
    if git_installed:
        logfile.write("git is already installed.\n")
        print "git is already installed.\n" 
    else:
        result = yum_install("git", logfile)
        success = result[0]
        logfile = result[1]
        if not success:
            return logfile
            
    # gcc
    if gcc_installed:
        logfile.write("gcc is already installed.\n")
        print "gcc is already installed.\n" 
    else:
        result = yum_install("gcc", logfile)
        success = result[0]
        logfile = result[1]
        if not success:
            return logfile
      
    # pip for Python 2.7   
    if pip_installed27:
        logfile.write("pip is already installed for Python 2.7.3.\n")
        print "pip is already installed for Python 2.7.3.\n" 
    else:
        logfile.write("pip will be installed for Python 2.7.3\n")
        print ("pip will be installed for Python 2.7.3\n")
        pip27_command = pythonpath + os.sep + "easy_install-2.7 pip" 
        logfile.write(pip27_command + "\n")
        print pip27_command + "\n"
        
        pip_tuple = commands.getstatusoutput(pip27_command)
        status = pip_tuple[0]
        output = pip_tuple[1]
        # Print output line by line
        output2 = output.split("\n")
        for line in output2:
            logfile.write(line + "\n")
            print line
        if status == 0:
            pip_installed27 = python_package_check(pythonpath + os.sep + "pip-2.7", "pip")
            if pip_installed27:
                logfile.write("pip for Python 2.7.3 installed successfully.\n")
                print "pip for Python 2.7.3 installed successfully.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("pip for Python 2.7.3 failed to install.\n")
                print "pip for Python 2.7.3 failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
        elif status == 1:
            logfile.write("pip for Python 2.7.3 failed to install.\n")
            print "pip for Python 2.7.3 failed to install.\n"
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile

    logfile.write("Beginning installation of Python Imaging Library components python-imaging, python-devel, and libjpeg-devel.\n")
    print "Beginning installation of Python Imaging Library components python-imaging, python-devel, and libjpeg-devel.\n"
        
    # python-imaging    
    if python_imaging_installed:
        logfile.write("python-imaging is already installed.\n")
        print "python-imaging is already installed.\n" 
    else:
        result = yum_install("python-imaging", logfile)
        success = result[0]
        logfile = result[1]
        if not success:
            return logfile

    # postgresql91-server
    if python_devel_installed:
        logfile.write("python-devel is already installed.\n")
        print "python-devel is already installed.\n" 
    else:
        result = yum_install("python-devel", logfile)
        success = result[0]
        logfile = result[1]
        if not success:
            return logfile
        
    # libjpeg-devel
    if libjpeg_devel_installed:
        logfile.write("libjpeg-devel (libjpeg-turbo-devel) is already installed.\n")
        print "libjpeg-devel (libjpeg-turbo-devel) is already installed.\n" 
    else:
        result = yum_install("libjpeg-turbo-devel", logfile)
        success = result[0]
        logfile = result[1]
        if not success:
            return logfile

    # Check locations of shared libraries
    logfile.write("Checking for Python Imaging Library shared libraries.\n")
    print "Checking for Python Imaging Library shared libraries.\n"
    # libjpeg.so
    try:
        libjpeg_stat = os.stat("/usr/lib64/libjpeg.so")
        if libjpeg_stat:
            output1 = "Found libjpeg.so at /usr/lib64/libjpeg.so\n"
            logfile.write(output1)
            print output1
    except OSError as libjpeg_error:
        error1 = "Error: Could not find libjpeg.so in /usr/lib64.\n"
        error2 = "Python Imaging Library-related packages may not have installed properly.\n"
        logfile.write(error1)
        logfile.write(error2)
        print error1
        print error2
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile
    
    # libz.so
    try:
        libjpeg_stat = os.stat("/usr/lib64/libz.so")
        if libjpeg_stat:
            output1 = "Found libz.so at /usr/lib64/libz.so\n"
            logfile.write(output1)
            print output1
    except OSError as libjpeg_error:
        try:
            libz_stat2 = os.stat("/lib64/libz.so")
            if libz_stat2:
                output2 = "Found: libz.so at /lib64/libz.so\n"
                output3 = "Symbolic link will be created: /usr/lib64/libz.so --> /lib64/libz.so\n"
                output4 = "ln -s /lib64/libz.so /usr/lib64/libz.so\n"
                logfile.write(output2)
                logfile.write(output3)
                logfile.write(output4)
                print output2
                print output3
                print output4
                libjpeg_tuple = commands.getstatusoutput("ln -s /lib64/libz.so /usr/lib64/libz.so")
                status = libjpeg_tuple[0]
                if status != 0:
                    error1 = "Error: Could not create symbolic link: /usr/lib64/libz.so --> /lib64/libz.so\n"
                    logfile.write(error1)
                    print error1
                    end_time = termination_string()
                    logfile.write(end_time)
                    print end_time
                    return logfile 
        except OSError as libjpeg_error3:
            error1 = "Error: Could not find libz.so in /lib64.\n"
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
        repo_string = "The repository at http://yum.postgresql.org/9.1/redhat/rhel-6-x86_64/pgdg-redhat91-9.1-5.noarch rpm is already installed.\n"
        logfile.write(repo_string)
        print repo_string
    else:
        # Install Postgresql RPM
        logfile.write("Adding the PostgreSQL 9.1 repo pgdg91...\n")
        print "Adding the PostgreSQL 9.1 repo pgdg91...\n"
        pg_repo_command = "rpm -i http://yum.postgresql.org/9.1/redhat/rhel-6-x86_64/pgdg-redhat91-9.1-5.noarch.rpm"
        logfile.write(pg_repo_command + "\n")
        print pg_repo_command + "\n"
        repo_tuple = commands.getstatusoutput(pg_repo_command)
        status = repo_tuple[0]
        output = repo_tuple[1]
        # Print output line by line
        output2 = output.split("\n")
        for line in output2:
            logfile.write(line + "\n")
            print line + "\n"
        if status == 0:
            rpm_installed = postgresql91_repocheck()
            if rpm_installed:
                logfile.write("pgdg91 repo installed successfully.\n")
                print "pgdg91 repo installed successfully.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("PostgreSQL 9.1 repo failed to install.\n")
                print "PostgreSQL 9.1 repo failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
        elif status == 1:
            logfile.write("PostgreSQL 9.1 repo failed to install.\n")
            print "PostgreSQL 9.1 repo failed to install.\n"
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile
    
    # postgresql91-server
    if postgresql91_server_installed:
        logfile.write("postgresql91-server is already installed.\n")
        print "postgresql91-server is already installed.\n"
    else:
        result = yum_install("postgresql91-server", logfile)
        success = result[0]
        logfile = result[1]
        if not success:
            return logfile
    
    # postgresql-91-contrib
    if postgresql91_contrib_installed:
        logfile.write("postgresql91-contrib is already installed.\n")
        print "postgresql91-contrib is already installed.\n"   
    else:
        result = yum_install("postgresql91-contrib", logfile)
        success = result[0]
        logfile = result[1]
        if not success:
            return logfile
    
    # postgresql91-devel
    if postgresql91devel_installed:
        logfile.write("postgresql91-devel is already installed.\n")
        print "postgresql91-devel is already installed.\n"   
    else:
        result = yum_install("postgresql91-devel", logfile)
        success = result[0]
        logfile = result[1]
        if not success:
            return logfile
        
    # memcached
    if memcached_installed:
        logfile.write("memcached is already installed.\n")
        print "memcached is already installed.\n"   
    else:
        result = yum_install("memcached", logfile)
        success = result[0]
        logfile = result[1]
        if not success:
            return logfile
        
    # libmemcached-devel
    if libmemcached_installed:
        logfile.write("libmemcached-devel is already installed.\n")
        print "libmemcached-devel is already installed.\n"   
    else:
        result = yum_install("libmemcached-devel", logfile)
        success = result[0]
        logfile = result[1]
        if not success:
            return logfile 
        
    logfile.write("RHEL x64 installation script completed successfully.\n")
    print "RHEL x64 installation script completed successfully.\n"
    end_time = termination_string()
    logfile.write(end_time)
    print end_time
    return logfile