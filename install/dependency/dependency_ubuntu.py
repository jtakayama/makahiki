import subprocess
import re
import os
import shlex
import datetime

def dpkg_check(packagename):
    """
    Checks the installation status of packages that need to be checked via 
    dpkg -s <packagename>. Returns True if installed, False if not.
    """
    dpkg_success = "Status: install ok installed"
    compare_result = False
    try:
        output = subprocess.check_output(shlex.split("dpkg -s %s" % packagename), stderr=subprocess.STDOUT)
        lines = output.split("\n")
        if lines[1] == dpkg_success:
            compare_result = True
    except subprocess.CalledProcessError as cpe:
        dpkg_fail = re.compile("(Package `)(%s)+(\' is not installed and no info is available.)" % packagename)
        lines = cpe.output.split("\n")
        line0_result = dpkg_fail.match(lines[0])
        if (line0_result):
            compare_result = False
    return compare_result

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
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    end_time = "Script exiting at %s\n" % time
    return end_time

def run(arch, logfile):
    """
    Installs and configures some Makahiki dependencies by issuing 
    system commands. Writes its output to a logfile and prints 
    it to the console. It is left to the calling function to close 
    the logfile, which is returned.
    
    The target OS is Ubuntu Linux. x86 and x64 Ubuntu are supported.
    
    Warning: This will install or update to the newest available 
    versions of all packages specified.
    """
    
    # Boolean variables for each dependency
    git_installed = dpkg_check("git")
    gcc_installed = dpkg_check("gcc")
    python_setuptools_installed = dpkg_check("python-setuptools")
    pip_installed = pip_check()
    python_imaging_installed = dpkg_check("python-imaging")
    python_dev_installed = dpkg_check("python-dev")
    libjpeg_dev_installed = dpkg_check("libjpeg-dev")
    postgresql91_installed = dpkg_check("postgresql-9.1")
    libpq_dev_installed = dpkg_check("libpq-dev")
    memcached_installed = dpkg_check("memcached")
    libmemcached_installed = dpkg_check("libmemcached-dev")
    virtualenvwrapper_installed = virtualenvwrapper_check()
    
    # Write start time to file
    firstline = "Makahiki installation script for Ubuntu %s" % arch
    logfile.write(firstline)
    print firstline
    
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d %H:%M:%S")
    start_time = "Script started at %s\n" % time
    logfile.write(start_time)
    print start_time
    
    # Confirm that the user wants to continue.
    dependencies_list = "This script will install these packages and their dependencies:\n\
         git,\n\
         gcc,\n\
         python-setuptools,\n\
         pip,\n\
         python-imaging,\n\
         python-dev,\n\
         libjpeg-dev,\n\
         postgresql-9.1,\n\
         libpq-dev,\n\
         memcached,\n\
         libmemcached-dev,\n\
         virtualenvwrapper\n"
    logfile.write(dependencies_list)
    print dependencies_list
    logfile.write("This script will also append to the current user's .bashrc file.\n")
    print ("This script will also append to the current user's .bashrc file.\n")
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
        logfile.write("Starting dependency installation for Ubuntu %s.\nChecking for dependencies...\n" % arch)
        print "Starting dependency installation for Ubuntu %s.\nChecking for dependencies...\n" % arch
        
        # git
        if git_installed:
            logfile.write("git is already installed.\n")
            print "git is already installed.\n"
        else:
            logfile.write("git will be installed.\n")
            print "git will be installed.\n"
            logfile.write("apt-get install -y git\n")
            print "apt-get install -y git\n"
            git_output = subprocess.check_output(["apt-get", "install", "-y", "git"], stderr=subprocess.STDOUT)
            logfile.write(git_output)
            print git_output
            git_installed = dpkg_check("git")
            if git_installed:
                logfile.write("git was successfully installed.\n")
                print "git was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: git failed to install.\n")
                print "Error: git failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        # gcc
        if gcc_installed:
            logfile.write("gcc is already installed.\n")
            print "gcc is already installed.\n"
        else:
            logfile.write("gcc will be installed.\n")
            print "gcc will be installed.\n"
            logfile.write("apt-get install -y gcc\n")
            print "apt-get install -y gcc\n"
            gcc_output = subprocess.check_output(["apt-get", "install", "-y", "gcc"], stderr=subprocess.STDOUT)
            logfile.write(gcc_output)
            print gcc_output
            gcc_installed = dpkg_check("gcc")
            if gcc_installed:
                logfile.write("gcc was successfully installed.\n")
                print "gcc was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: gcc failed to install.\n")
                print "Error: gcc failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        # python-setuptools
        if python_setuptools_installed:
            logfile.write("python-setuptools is already installed.\n")
            print "python-setuptools is already installed.\n"
        else:
            logfile.write("python-setuptools will be installed.\n")
            print "python-setuptools will be installed.\n"
            logfile.write("apt-get install -y python-setuptools\n")
            print "apt-get install -y python-setuptools\n"
            setuptools_output = subprocess.check_output(["apt-get", "install", "-y", "python-setuptools"], stderr=subprocess.STDOUT)
            logfile.write(setuptools_output)
            print setuptools_output
            python_setuptools_installed = dpkg_check("python-setuptools")
            if python_setuptools_installed:
                logfile.write("python-setuptools was successfully installed.\n")
                print "python-setuptools was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: python-setuptools failed to install.\n")
                print "Error: python-setuptools failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        # pip
        if pip_installed:
            logfile.write("pip is already installed.\n")
            print "pip is already installed.\n"
        else:
            logfile.write("pip will be installed.\n")
            print "pip will be installed.\n"
            logfile.write("easy_install pip\n")
            print "easy_install pip\n"
            try:
                USER_HOME = subprocess.check_output(["echo $HOME"], stderr=subprocess.STDOUT, shell=True)
                # Remove newline from expected "/home/<username>\n"
                USER_HOME = USER_HOME[:-1]
                USER_PROJECT_HOME = USER_HOME + os.sep + "makahiki"
                # cd to makahiki directory so easy_install will find its setup script
                os.chdir(USER_PROJECT_HOME)
                pip_output = subprocess.check_output(["easy_install", "pip"], stderr=subprocess.STDOUT)
                logfile.write(pip_output)
                print pip_output
                pip_installed = pip_check()
                if pip_installed:
                    logfile.write("pip was successfully installed.\n")
                    print "pip was successfully installed.\n"
                    # Flush the buffer and force a write to disk after each successful installation
                    logfile.flush()
                    os.fsync(logfile)
                else:
                    logfile.write("Error: pip failed to install.\n")
                    print "Error: pip failed to install.\n"
                    end_time = termination_string()
                    logfile.write(end_time)
                    print end_time
                    return logfile
            except subprocess.CalledProcessError as cpe:
                logfile.write("CalledProcessError: ")
                print "CalledProcessError: "
                logfile.write(cpe.output)
                print cpe.output
                logfile.write("Error: pip failed to install.\n")
                print "Error: pip failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        logfile.write("Beginning installation of Python Imaging Library components python-imaging, python-dev, and libjpeg-dev.\n")
        print "Beginning installation of Python Imaging Library components python-imaging, python-dev, and libjpeg-dev.\n"
        
        # python-imaging
        if python_imaging_installed:
            logfile.write("python-imaging is already installed.\n")
            print "python-imaging is already installed.\n"
        else:
            logfile.write("python-imaging will be installed.\n")
            print "python-imaging will be installed.\n"
            logfile.write("apt-get install -y python-imaging\n")
            print "apt-get install -y python-imaging\n"
            python_imaging_output = subprocess.check_output(["apt-get", "install", "-y",  "python-imaging"], stderr=subprocess.STDOUT)
            logfile.write(python_imaging_output)
            print python_imaging_output
            python_imaging_installed = dpkg_check("python-imaging")
            if python_imaging_installed:
                logfile.write("python-imaging was successfully installed.\n")
                print "python-imaging was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: python-imaging failed to install.\n")
                print "Error: python-imaging failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        # python-dev
        if python_dev_installed:
            logfile.write("python-dev is already installed.\n")
            print "python-dev is already installed.\n"
        else:
            logfile.write("python-dev will be installed.\n")
            print "python-dev will be installed.\n"
            logfile.write("apt-get install -y python-dev\n")
            print "apt-get install -y python-dev\n"
            python_dev_output = subprocess.check_output(["apt-get", "install", "-y",  "python-dev"], stderr=subprocess.STDOUT)
            logfile.write(python_dev_output)
            print python_dev_output
            python_dev_installed = dpkg_check("python-dev")
            if python_dev_installed:
                logfile.write("python-dev was successfully installed.\n")
                print "python-dev was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: python-dev failed to install.\n")
                print "Error: python-dev failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        # libjpeg-dev
        if libjpeg_dev_installed:
            logfile.write("libjpeg-dev is already installed.\n")
            print "libjpeg-dev is already installed.\n"
        else:
            logfile.write("libjpeg-dev will be installed.\n")
            print "libjpeg-dev will be installed.\n"
            logfile.write("apt-get install -y libjpeg-dev\n")
            print "apt-get install -y libjpeg-dev\n"
            libjpeg_dev_output = subprocess.check_output(["apt-get", "install", "-y",  "libjpeg-dev"], stderr=subprocess.STDOUT)
            logfile.write(libjpeg_dev_output)
            print libjpeg_dev_output
            libjpeg_dev_installed = dpkg_check("libjpeg-dev")
            if libjpeg_dev_installed:
                logfile.write("libjpeg-dev was successfully installed.\n")
                print "libjpeg-dev was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: libjpeg-dev failed to install.\n")
                print "Error: libjpeg-dev failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        # Check for shared libraries and configure symbolic links if needed
        logfile.write("Checking for Python Imaging Library shared libraries.\n")
        print "Checking for Python Imaging Library shared libraries.\n"
        # libjpeg.so
        try:
            libjpeg_stat = os.stat("/usr/lib/libjpeg.so")
            if libjpeg_stat:
                output1 = "Found libjpeg.so at /usr/lib/libjpeg.so\n"
                logfile.write(output1)
                print output1
        except OSError as libjpeg_error:
            if arch == "x86":
                try:
                    libjpeg_stat2 = os.stat("/usr/lib/i386-linux-gnu/libjpeg.so")
                    if libjpeg_stat2:
                        output2 = "Found: libjpeg.so at /usr/lib/i386-linux-gnu/libjpeg.so\n"
                        output3 = "Symbolic link will be created: /usr/lib/libjpeg.so --> /usr/lib/i386-linux-gnu/libjpeg.so\n"
                        output4 = "ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/libjpeg.so\n"
                        logfile.write(output2)
                        logfile.write(output3)
                        logfile.write(output4)
                        print output2
                        print output3
                        print output4
                        subprocess.check_output(["ln", "-s", "/usr/lib/i386-linux-gnu/libjpeg.so", "/usr/lib/libjpeg.so"], stderr=subprocess.STDOUT)
                    else:
                        raise OSError
                except OSError as libjpeg_i386_error:
                    output5 = "Error: Could not find libjpeg.so in /usr/lib or /usr/lib/i386-linux-gnu.\n"
                    output6 = "Python Imaging Library-related packages may not have installed properly.\n"
                    logfile.write(output5)
                    logfile.write(output6)
                    print output5
                    print output6
                    end_time = termination_string()
                    logfile.write(end_time)
                    print end_time
                    return logfile 
            elif arch == "x64":
                try:
                    libjpeg_stat2 = os.stat("/usr/lib/x86_64-linux-gnu/libjpeg.so")
                    if libjpeg_stat2:
                        output2 = "Found: libjpeg.so at /usr/lib/x86_64-linux-gnu/libjpeg.so\n"
                        output3 = "Symbolic link will be created: /usr/lib/libjpeg.so --> /usr/lib/x86_64-linux-gnu/libjpeg.so\n"
                        output4 = "ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg.so\n"
                        logfile.write(output2)
                        logfile.write(output3)
                        logfile.write(output4)
                        print output2
                        print output3
                        print output4
                        subprocess.check_output(["ln", "-s", "/usr/lib/x86_64-linux-gnu/libjpeg.so", "/usr/lib/libjpeg.so"], stderr=subprocess.STDOUT)
                    else:
                        raise OSError
                except OSError as libjpeg_x86_64_error:
                    output5 = "Error: Could not find libjpeg.so in /usr/lib or /usr/lib/x86_64-linux-gnu.\n"
                    output6 = "Python Imaging Library-related packages may not have installed properly.\n"
                    logfile.write(output5)
                    logfile.write(output6)
                    print output5
                    print output6
                    end_time = termination_string()
                    logfile.write(end_time)
                    print end_time
                    return logfile
            else:
                invalid_arch = "Error: Unsupported architecture for Ubuntu: %s\n" % arch
                logfile.write(invalid_arch)
                print invalid_arch
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        # libz.so         
        try:
            libz_stat = os.stat("/usr/lib/libz.so")
            if libz_stat:
                output1 = "Found libz.so at /usr/lib/libz.so\n"
                logfile.write(output1)
                print output1
        except OSError as libz_error:
            if arch == "x86":
                try:
                    libz_stat2 = os.stat("/usr/lib/i386-linux-gnu/libz.so")
                    if libz_stat2:
                        output2 = "Found: libz.so at /usr/lib/i386-linux-gnu/libz.so\n"
                        output3 = "Symbolic link will be created: /usr/lib/libz.so --> /usr/lib/i386-linux-gnu/libz.so\n"
                        output4 = "ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/libz.so\n"
                        logfile.write(output2)
                        logfile.write(output3)
                        logfile.write(output4)
                        print output2
                        print output3
                        print output4
                        subprocess.check_output(["ln", "-s", "/usr/lib/i386-linux-gnu/libz.so", "/usr/lib/libz.so"], stderr=subprocess.STDOUT)
                    else:
                        raise OSError
                except OSError as libz_i386_error:
                    output5 = "Error: Could not find libz.so in /usr/lib or /usr/lib/i386-linux-gnu.\n"
                    output6 = "Python Imaging Library-related packages may not have installed properly.\n"
                    logfile.write(output5)
                    logfile.write(output6)
                    print output5
                    print output6
                    end_time = termination_string()
                    logfile.write(end_time)
                    print end_time
                    return logfile
            elif arch == "x64":
                try:
                    libz_stat2 = os.stat("/usr/lib/x86_64-linux-gnu/libz.so")
                    if libz_stat2:
                        output2 = "Found: libz.so at /usr/lib/x86_64-linux-gnu/libz.so\n"
                        output3 = "Symbolic link will be created: /usr/lib/libz.so --> /usr/lib/x86_64-linux-gnu/libz.so\n"
                        output4 = "ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/libz.so\n"
                        logfile.write(output2)
                        logfile.write(output3)
                        logfile.write(output4)
                        print output2
                        print output3
                        print output4
                        subprocess.check_output(["ln", "-s", "/usr/lib/x86_64-linux-gnu/libz.so", "/usr/lib/libz.so"], stderr=subprocess.STDOUT)
                    else:
                        raise OSError
                except OSError as libz_x86_64_error:
                    output5 = "Error: Could not find libz.so in /usr/lib or /usr/lib/x86_64-linux-gnu.\n"
                    output6 = "Python Imaging Library-related packages may not have installed properly.\n"
                    logfile.write(output5)
                    logfile.write(output6)
                    print output5
                    print output6
                    end_time = termination_string()
                    logfile.write(end_time)
                    print end_time
                    return logfile
            else:
                invalid_arch = "Error: Unsupported architecture for Ubuntu: %s\n" % arch
                logfile.write(invalid_arch)
                print invalid_arch
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        logfile.write("Installation of Python Imaging Library components is complete.\n")
        print "Installation of Python Imaging Library components is complete.\n"
        
        # PostgreSQL 9.1
        if postgresql91_installed:
            logfile.write("postgresql-9.1 is already installed.\n")
            print "postgresql-9.1 is already installed.\n"
        else:
            logfile.write("postgresql-9.1 will be installed.\n")
            print "postgresql-9.1 will be installed.\n"
            logfile.write("apt-get install -y postgresql-9.1\n")
            print "apt-get install -y postgresql-9.1\n"
            psql_output = subprocess.check_output(["apt-get", "install", "-y",  "postgresql-9.1"], stderr=subprocess.STDOUT)
            logfile.write(psql_output)
            print psql_output
            postgresql91_installed = dpkg_check("postgresql-9.1")
            if postgresql91_installed:
                logfile.write("postgresql-9.1 was successfully installed.\n")
                print "postgresql-9.1 was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: postgresql-9.1 failed to install.\n")
                print "Error: postgresql-9.1 failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
        
        #libpq-dev
        if libpq_dev_installed:
            logfile.write("libpq-dev is already installed.\n")
            print "libpq-dev is already installed.\n"
        else:
            logfile.write("libpq-dev will be installed.\n")
            print "libpq-dev will be installed.\n"
            logfile.write("apt-get install -y libpq-dev\n")
            print "apt-get install -y libpq-dev\n"
            libpq_dev_output = subprocess.check_output(["apt-get", "install", "-y",  "libpq-dev"], stderr=subprocess.STDOUT)
            logfile.write(libpq_dev_output)
            print libpq_dev_output
            libpq_dev_installed = dpkg_check("libpq-dev")
            if libpq_dev_installed:
                logfile.write("libpq-dev was successfully installed.\n")
                print "libpq-dev was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: libpq-dev failed to install.\n")
                print "Error: libpq-dev failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        #memcached
        if memcached_installed:
            logfile.write("memcached is already installed.\n")
            print "memcached is already installed.\n"
        else:
            logfile.write("memcached will be installed.\n")
            print "memcached will be installed.\n"
            logfile.write("apt-get install -y memcached\n")
            print "apt-get install -y memcached\n"
            memcached_output = subprocess.check_output(["apt-get", "install", "-y",  "memcached"], stderr=subprocess.STDOUT)
            logfile.write(memcached_output)
            print memcached_output
            memcached_installed = dpkg_check("memcached")
            if memcached_installed:
                logfile.write("memcached was successfully installed.\n")
                print "memcached was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: memcached failed to install.\n")
                print "Error: memcached failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
    
        #libmemcached-dev
        if libmemcached_installed:
            logfile.write("libmemcached-dev is already installed.\n")
            print "libmemcached-dev is already installed.\n"
        else:
            logfile.write("libmemcached-dev will be installed.\n")
            print "libmemcached-dev will be installed.\n"
            logfile.write("apt-get install -y libmemcached-dev\n")
            print "apt-get install -y libmemcached-dev\n"
            libmemcached_output = subprocess.check_output(["apt-get", "install", "-y",  "libmemcached-dev"], stderr=subprocess.STDOUT)
            logfile.write(libmemcached_output)
            print libmemcached_output
            libmemcached_installed = dpkg_check("libmemcached-dev")
            if libmemcached_installed:
                logfile.write("libmemcached-dev was successfully installed.\n")
                print "libmemcached-dev was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: libmemcached-dev failed to install.\n")
                print "Error: libmemcached-dev failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
            
        #virtualenvwrapper
        if virtualenvwrapper_installed:
            logfile.write("virtualenvwrapper is already installed.\n")
            print "virtualenvwrapper is already installed.\n"
        else:
            logfile.write("virtualenvwrapper will be installed.\n")
            print "virtualenvwrapper will be installed.\n"
            logfile.write("pip install virtualenvwrapper\n")
            print "pip install virtualenvwrapper\n"
            virtualenvwrapper_output = subprocess.check_output(["pip", "install",  "virtualenvwrapper"], stderr=subprocess.STDOUT)
            logfile.write(virtualenvwrapper_output)
            print virtualenvwrapper_output
            virtualenvwrapper_installed = virtualenvwrapper_check()
            if virtualenvwrapper_installed:
                logfile.write("virtualenvwrapper was successfully installed.\n")
                print "virtualenvwrapper was successfully installed.\n"
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
            else:
                logfile.write("Error: virtualenvwrapper failed to install.\n")
                print "Error: virtualenvwrapper failed to install.\n"
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
        
        # bashrc
        USER_HOME = subprocess.check_output(["echo $HOME"], stderr=subprocess.STDOUT, shell=True) 
        # Remove newline from expected "/home/<username>\n"
        USER_HOME = USER_HOME[:-1]
        MAKAHIKI_HOME = USER_HOME + os.sep + "makahiki"
        bashrc_output0 = "Appending these lines to user's ~./bashrc file:\n"
        bashrc_output1 = "# Virtualenvwrapper settings for makahiki\n"
        bashrc_output2 = "export WORKON_HOME=%s/.virtualenvs\n" % USER_HOME
        bashrc_output3 = "export PROJECT_HOME=%s\n" % MAKAHIKI_HOME
        bashrc_output4 = "source /usr/local/bin/virtualenvwrapper.sh\n"
        logfile.write(bashrc_output0 + bashrc_output1 + bashrc_output2 + bashrc_output3 + bashrc_output4)
        print bashrc_output0 + bashrc_output1 + bashrc_output2 + bashrc_output3 + bashrc_output4
        # Append to ~/.bashrc
        bashrc = open(USER_HOME + "/.bashrc", 'a')
        bashrc.write("\n# Virtualenvwrapper settings for makahiki\n")
        bashrc.write("export WORKON_HOME=%s/.virtualenvs\n" % USER_HOME)
        bashrc.write("export PROJECT_HOME=%s\n" % MAKAHIKI_HOME)
        bashrc.write("source /usr/local/bin/virtualenvwrapper.sh\n")
        bashrc.close()
        # Done appending to file
        logfile.write("Done appending to ~/.bashrc file.\n")
        print "Done appending to ~/.bashrc file.\n"
        
        # Done with installation process   
        logfile.write("Script completed successfully.\n")
        print ("Script completed successfully.\n") 
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile
