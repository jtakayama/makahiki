import subprocess
import re

def dpkg_check(packagename):
    """
    Checks the installation status of packages that need to be checked via 
    dpkg -s <packagename>. Returns True if installed, False if not.
    """
    dpkg_fail = re.compile("(Package `)(\S)+(\' is not installed and no info is available.)")
    dpkg_success = "Status: install ok installed"
    output = subprocess.check_output(["dpkg", "-s", packagename], stderr=subprocess.STDOUT)
    lines = output.split("\n")
    line0_result = dpkg_fail.match(lines[0])
    compare_result = False
    if (not line0_result) and result[1] == dpkg_success:
        compare_result = True
    else: 
        compare_result = False
    return compare_result

def psql91_check(version):
    """
    Checks the version number of Postgresql on the system. 
    Returns True if a version of Postgresql 9.1 is installed, and False 
    if it is not.
    """
    output = subprocess.check_output(["psql", "--version"], stderr=subprocess.STDOUT)
    lines = output.split("\n")
    version_string = re.compile("(psql\ )(\S)+( 9.1.(\d)+)")
    line0_result = version_string.match(lines[0])
    compare_result = False
    if not line0_result:
        compare_result = False
    else:
        compare_result = True
    return compare_result

def dependency_ubuntu(arch, logfile):
    """
    Installs and configures some Makahiki dependencies by issuing 
    system commands. Writes its output to a logfile and prints 
    it to the console.
    
    The target OS is Ubuntu Linux. x86 and x64 Ubuntu are supported.
    """
    
    # Boolean variables for each dependency
    git_installed = False
    gcc_installed = False
    python_setuptools_installed = False
    pip_installed = False
    python_imaging_installed = False
    pythondev_installed = False
    libjpeg_installed = False
    postgresql91_installed = False
    libpqdev_installed = False
    memcached_installed = False
    virtualenvwrapper_installed = False
    
    print "Not implemented."