import subprocess
import re
import os
import shlex

def dpkg_check(packagename):
    """
    Checks the installation status of packages that need to be checked via 
    dpkg -s <packagename>. Returns True if installed, False if not.
    """
    dpkg_success = "Status: install ok installed"
    try:
    	output = subprocess.check_output(shlex.split("dpkg -s %s" % packagename), stderr=subprocess.STDOUT)
	lines = output.split("\n")
	compare_result = False
	if lines[1] == dpkg_success:
	    compare_result = True
    except subprocess.CalledProcessError as cpe:
        dpkg_fail = re.compile("(Package `)(\S)+(\' is not installed and no info is available.)")
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

def psql91_check():
    """
    Checks the version number of Postgresql on the system. 
    Returns True if a version of Postgresql 9.1 is installed, and False 
    if it is not.
    """
    compare_result = False
    try:
        output = subprocess.check_output(shlex.split("psql --version"), stderr=subprocess.STDOUT)
        lines = output.split("\n")
        version_string = re.compile("(psql\ )(\S)+( 9.1.(\d)+)")
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
    system commands. Writes its output to a logfile and prints 
    it to the console. It is left to the calling function to close 
    the logfile, which is returned.
    
    The target OS is Ubuntu Linux. x86 and x64 Ubuntu are supported.
    """
    
    # Boolean variables for each dependency
    git_installed = dpkg_check("git")
    gcc_installed = dpkg_check("gcc")
    python_setuptools_installed = dpkg_check("python-setuptools")
    pip_installed = pip_check()
    python_imaging_installed = dpkg_check("python-imaging")
    python_dev_installed = dpkg_check("python-dev")
    libjpeg_dev_installed = dpkg_check("libjpeg-dev")
    postgresql91_installed = psql91_check()
    libpq_dev_installed = dpkg_check("libpq-dev")
    memcached_installed = dpkg_check("memcached")
    libmemcached_installed = dpkg_check("libmemcached-dev")
    virtualenvwrapper_installed = virtualenvwrapper_check()
    
    # Write start time to file
    firstline = "Makahiki startup script for Ubuntu %s" % arch
    logfile.write(firstline)
    print firstline
    start_time = "Script started at " + subprocess.check_output(["date"], stderr=subprocess.STDOUT)
    logfile.write(start_time)
    print start_time
    logfile.write("Starting dependency installation for Ubuntu %s.\nChecking for dependencies..." % arch)
    print "Starting dependency installation for Ubuntu %s.\nChecking for dependencies..." % arch
    
    # git
    if git_installed:
        logfile.write("git is already installed.")
        print "git is already installed."
    else:
        logfile.write("git will be installed.")
        print "git will be installed."
        logfile.write("apt-get install -y git")
        print "apt-get install -y git"
        git_output = subprocess.check_output(["apt-get", "install", "-y", "git"], stderr=subprocess.STDOUT)
        logfile.write(git_output)
        print git_output
        git_installed = dpkg_check("git")
        if git_installed:
            logfile.write("git was successfully installed.")
            print "git was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: git failed to install.")
            print "Error: git failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile
    
    # gcc
    if gcc_installed:
        logfile.write("gcc is already installed.")
        print "gcc is already installed."
    else:
        logfile.write("gcc will be installed.")
        print "gcc will be installed."
        logfile.write("apt-get install -y gcc")
        print "apt-get install -y gcc"
        gcc_output = subprocess.check_output(["apt-get", "install", "-y", "gcc"], stderr=subprocess.STDOUT)
        logfile.write(gcc_output)
        print gcc_output
        gcc_installed = dpkg_check("gcc")
        if gcc_installed:
            logfile.write("gcc was successfully installed.")
            print "gcc was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: gcc failed to install.")
            print "Error: gcc failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile
    
    # python-setuptools
    if python_setuptools_installed:
        logfile.write("python-setuptools is already installed.")
        print "python-setuptools is already installed."
    else:
        logfile.write("python-setuptools will be installed.")
        print "python-setuptools will be installed."
        logfile.write("apt-get install -y python-setuptools")
        print "apt-get install -y python-setuptools"
        setuptools_output = subprocess.check_output(["apt-get", "install", "-y", "python-setuptools"], stderr=subprocess.STDOUT)
        logfile.write(setuptools_output)
        print setuptools_output
        python_setuptools_installed = dpkg_check("python-setuptools")
        if python_setuptools_installed:
            logfile.write("python-setuptools was successfully installed.")
            print "python-setuptools was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: python-setuptools failed to install.")
            print "Error: python-setuptools failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile
    
    # pip
    if pip_installed:
        logfile.write("pip is already installed.")
        print "pip is already installed."
    else:
        logfile.write("pip will be installed.")
        print "pip will be installed."
        logfile.write("easy_install pip")
        print "easy_install pip"
        try:
            USER_HOME = subprocess.check_output(["echo $HOME"], stderr=subprocess.STDOUT, shell=True)
            # Remove newline from expected "/home/<username>\n"
            USER_HOME = USER_HOME[:-1]
            USER_PROJECT_HOME = USER_HOME[:-1] + "/makahiki"
            # cd to makahiki directory so easy_install will find its setup script
            os.chdir(USER_PROJECT_HOME)
            pip_output = subprocess.check_output(["easy_install", "pip"], stderr=subprocess.STDOUT)
            logfile.write(pip_output)
            print pip_output
    	    pip_installed = pip_check()
    	    if pip_installed:
                logfile.write("pip was successfully installed.")
                print "pip was successfully installed."
                # Flush the buffer and force a write to disk after each successful installation
                logfile.flush()
                os.fsync(logfile)
    	    else:
                logfile.write("Error: pip failed to install.")
                print "Error: pip failed to install."
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
        except subprocess.CalledProcessError as cpe:
            logfile.write("CalledProcessError: ")
            print "CalledProcessError: "
            logfile.write(cpe.output)
            print cpe.output
            logfile.write("Error: pip failed to install.")
            print "Error: pip failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile 
    
    logfile.write("Beginning installation of Python Imaging Library components python-imaging, python-dev, and libjpeg-dev. ")
    print "Beginning installation of Python Imaging Library components python-imaging, python-dev, and libjpeg-dev."
    
    # python-imaging
    if python_imaging_installed:
        logfile.write("python-imaging is already installed.")
        print "python-imaging is already installed."
    else:
        logfile.write("python-imaging will be installed.")
        print "python-imaging will be installed."
        logfile.write("apt-get install -y python-imaging")
        print "apt-get install -y python-imaging"
        python_imaging_output = subprocess.check_output(["apt-get", "install", "-y",  "python-imaging"], stderr=subprocess.STDOUT)
        logfile.write(python_imaging_output)
        print python_imaging_output
        python_imaging_installed = dpkg_check("python-imaging")
        if python_imaging_installed:
            logfile.write("python-imaging was successfully installed.")
            print "python-imaging was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: python-imaging failed to install.")
            print "Error: python-imaging failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile 
    
    # python-dev
    if python_dev_installed:
        logfile.write("python-dev is already installed.")
        print "python-dev is already installed."
    else:
        logfile.write("python-dev will be installed.")
        print "python-dev will be installed."
        logfile.write("apt-get install -y python-dev")
        print "apt-get install -y python-dev"
        python_dev_output = subprocess.check_output(["apt-get", "install", "-y",  "python-dev"], stderr=subprocess.STDOUT)
        logfile.write(python_dev_output)
        print python_dev_output
        python_dev_installed = dpkg_check("python-dev")
        if python_dev_installed:
            logfile.write("python-dev was successfully installed.")
            print "python-dev was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: python-dev failed to install.")
            print "Error: python-dev failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile     

    # libjpeg-dev
    if libjpeg_dev_installed:
        logfile.write("libjpeg-dev is already installed.")
        print "libjpeg-dev is already installed."
    else:
        logfile.write("libjpeg-dev will be installed.")
        print "libjpeg-dev will be installed."
        logfile.write("apt-get install -y libjpeg-dev")
        print "apt-get install -y libjpeg-dev"
        libjpeg_dev_output = subprocess.check_output(["apt-get", "install", "-y",  "libjpeg-dev"], stderr=subprocess.STDOUT)
        logfile.write(libjpeg_dev_output)
        print libjpeg_dev_output
        libjpeg_dev_installed = dpkg_check("libjpeg-dev")
        if libjpeg_dev_installed:
            logfile.write("libjpeg-dev was successfully installed.")
            print "libjpeg-dev was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: libjpeg-dev failed to install.")
            print "Error: libjpeg-dev failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile 
    
    # Check for shared libraries and configure symbolic links if needed
    # libjpeg.so
    try:
        libjpeg_stat = os.stat("/usr/lib/libjpeg.so")
        if libjpeg_stat:
            output1 = "Found libjpeg.so at /usr/lib/libjpeg.so"
            logfile.write(output1)
            print output1
    except OSError as libjpeg_error:
        if arch == "x86":
            try:
                libjpeg_stat2 = os.stat("/usr/lib/i386-linux-gnu/libjpeg.so")
                if libjpeg_stat2:
                    output2 = "Found: libjpeg.so at /usr/lib/i386-linux-gnu/libjpeg.so"
                    output3 = "Symbolic link will be created: /usr/lib/libjpeg.so --> /usr/lib/i386-linux-gnu/libjpeg.so"
                    output4 = "ln -s /usr/lib/i386-linux-gnu/libjpeg.so /usr/lib/libjpeg.so"
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
                output5 = "Error: Could not find libjpeg.so in /usr/lib or /usr/lib/i386-linux-gnu."
                output6 = "Python Imaging Library-related packages may not have installed properly."
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
                    output2 = "Found: libjpeg.so at /usr/lib/x86_64-linux-gnu/libjpeg.so"
                    output3 = "Symbolic link will be created: /usr/lib/libjpeg.so --> /usr/lib/x86_64-linux-gnu/libjpeg.so"
                    output4 = "ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/libjpeg.so"
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
                output5 = "Error: Could not find libjpeg.so in /usr/lib or /usr/lib/x86_64-linux-gnu."
                output6 = "Python Imaging Library-related packages may not have installed properly."
                logfile.write(output5)
                logfile.write(output6)
                print output5
                print output6
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile
        else:
            invalid_arch = "Error: Unsupported architecture for Ubuntu: %s" % arch
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
            output1 = "Found libz.so at /usr/lib/libz.so"
            logfile.write(output1)
            print output1
    except OSError as libz_error:
        if arch == "x86":
            try:
                libz_stat2 = os.stat("/usr/lib/i386-linux-gnu/libz.so")
                if libz_stat2:
                    output2 = "Found: libz.so at /usr/lib/i386-linux-gnu/libz.so"
                    output3 = "Symbolic link will be created: /usr/lib/libz.so --> /usr/lib/i386-linux-gnu/libz.so"
                    output4 = "ln -s /usr/lib/i386-linux-gnu/libz.so /usr/lib/libz.so"
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
                output5 = "Error: Could not find libz.so in /usr/lib or /usr/lib/i386-linux-gnu."
                output6 = "Python Imaging Library-related packages may not have installed properly."
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
                    output2 = "Found: libz.so at /usr/lib/x86_64-linux-gnu/libz.so"
                    output3 = "Symbolic link will be created: /usr/lib/libz.so --> /usr/lib/x86_64-linux-gnu/libz.so"
                    output4 = "ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/libz.so"
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
                output5 = "Error: Could not find libz.so in /usr/lib or /usr/lib/x86_64-linux-gnu."
                output6 = "Python Imaging Library-related packages may not have installed properly."
                logfile.write(output5)
                logfile.write(output6)
                print output5
                print output6
                end_time = termination_string()
                logfile.write(end_time)
                print end_time
                return logfile        
        else:
            invalid_arch = "Error: Unsupported architecture for Ubuntu: %s" % arch
            logfile.write(invalid_arch)
            print invalid_arch
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile 

                
    logfile.write("Installation of Python Imaging Library components is complete.")
    print "Installation of Python Imaging Library components is complete."
    
    # PostgreSQL 9.1
    if postgresql91_installed:
        logfile.write("postgresql-9.1 is already installed.")
        print "postgresql-9.1 is already installed."
    else:
        logfile.write("postgresql-9.1 will be installed.")
        print "postgresql-9.1 will be installed."
        logfile.write("apt-get install -y postgresql-9.1")
        print "apt-get install -y postgresql-9.1"
        psql_output = subprocess.check_output(["apt-get", "install", "-y",  "postgresql-9.1"], stderr=subprocess.STDOUT)
        logfile.write(psql_output)
        print psql_output
        postgresql91_installed = psql91_check()
        if postgresql91_installed:
            logfile.write("postgresql-9.1 was successfully installed.")
            print "postgresql-9.1 was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: postgresql-9.1 failed to install.")
            print "Error: postgresql-9.1 failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile 
    
    #libpq-dev
    if libpq_dev_installed:
        logfile.write("libpq-dev is already installed.")
        print "libpq-dev is already installed."
    else:
        logfile.write("libpq-dev will be installed.")
        print "libpq-dev will be installed."
        logfile.write("apt-get install -y libpq-dev")
        print "apt-get install -y libpq-dev"
        libpq_dev_output = subprocess.check_output(["apt-get", "install", "-y",  "libpq-dev"], stderr=subprocess.STDOUT)
        logfile.write(libpq_dev_output)
        print libpq_dev_output
        libpq_dev_installed = dpkg_check("libpq-dev")
        if libpq_dev_installed:
            logfile.write("libpq-dev was successfully installed.")
            print "libpq-dev was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: libpq-dev failed to install.")
            print "Error: libpq-dev failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile 
    
    #memcached
    if memcached_installed:
        logfile.write("memcached is already installed.")
        print "memcached is already installed."
    else:
        logfile.write("memcached will be installed.")
        print "memcached will be installed."
        logfile.write("apt-get install -y memcached")
        print "apt-get install -y memcached"
        memcached_output = subprocess.check_output(["apt-get", "install", "-y",  "memcached"], stderr=subprocess.STDOUT)
        logfile.write(memcached_output)
        print memcached_output
        memcached_installed = dpkg_check("memcached")
        if memcached_installed:
            logfile.write("memcached was successfully installed.")
            print "memcached was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: memcached failed to install.")
            print "Error: memcached failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile 

    #libmemcached-dev
    if libmemcached_installed:
        logfile.write("libmemcached-dev is already installed.")
        print "libmemcached-dev is already installed."
    else:
        logfile.write("libmemcached-dev will be installed.")
        print "libmemcached-dev will be installed."
        logfile.write("apt-get install -y libmemcached-dev")
        print "apt-get install -y libmemcached-dev"
        libmemcached_output = subprocess.check_output(["apt-get", "install", "-y",  "libmemcached-dev"], stderr=subprocess.STDOUT)
        logfile.write(libmemcached_output)
        print libmemcached_output
        libmemcached_installed = dpkg_check("libmemcached-dev")
        if libmemcached_installed:
            logfile.write("libmemcached-dev was successfully installed.")
            print "libmemcached-dev was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: libmemcached-dev failed to install.")
            print "Error: libmemcached-dev failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile 
        
    #virtualenvwrapper
    if virtualenvwrapper_installed:
        logfile.write("virtualenvwrapper is already installed.")
        print "virtualenvwrapper is already installed."
    else:
        logfile.write("virtualenvwrapper will be installed.")
        print "virtualenvwrapper will be installed."
        logfile.write("apt-get install -y virtualenvwrapper")
        print "apt-get install -y virtualenvwrapper"
        virtualenvwrapper_output = subprocess.check_output(["apt-get", "install", "-y",  "virtualenvwrapper"], stderr=subprocess.STDOUT)
        logfile.write(virtualenvwrapper_output)
        print virtualenvwrapper_output
        virtualenvwrapper_installed = virtualenvwrapper_check()
        if virtualenvwrapper_installed:
            logfile.write("virtualenvwrapper was successfully installed.")
            print "virtualenvwrapper was successfully installed."
            # Flush the buffer and force a write to disk after each successful installation
            logfile.flush()
            os.fsync(logfile)
        else:
            logfile.write("Error: virtualenvwrapper failed to install.")
            print "Error: virtualenvwrapper failed to install."
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile
    
    # bashrc
    USER_HOME = subprocess.check_output(["echo $HOME"], stderr=subprocess.STDOUT, shell=True) 
    # Remove newline from expected "/home/<username>\n"
    USER_HOME = USER_HOME[:-1]
    MAKAHIKI_HOME = USER_HOME + "/makahiki"
    bashrc_output0 = "Appending these lines to user's ~./bashrc file:"
    bashrc_output1 = "\n# Virtualenvwrapper settings for makahiki\n"
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
    logfile.write("Done appending to ~/.bashrc file.")
    print "Done appending to ~/.bashrc file."
    
    # Done with installation process   
    logfile.write("Script completed successfully.")
    print ("Script completed successfully.") 
    end_time = termination_string()
    logfile.write(end_time)
    print end_time
    return logfile
