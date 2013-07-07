import os
import sys
import subprocess
import shlex
import sys
import StringIO

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir + os.sep + "makahiki" + os.sep)
from apps.utils import script_utils

def termination_string():
    """
    Gets the current system time and appends it to a termination notice.
    """
    end_time = "Script exiting at %s" % subprocess.check_output(["date"], stderr=subprocess.STDOUT)
    return end_time

# Modified from manage_py_dir() in script_utils.py
def local_manage_py_dir():
    """Returns the directory holding the manage.py file as a string."""
    return os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir + os.sep)

# Modified from local_reset_db(heroku_app) in script_utils.py
def local_reset_db(logfile):
    """reset db.
    Returns a tuple result_tuple. result_tuple[0] has the logfile.
    result_tuple[1] is True if the reset was aborted, and False if was not.
    """
    local_reset_db_abort = False
    logfile.write("WARNING: This command will reset the database. " \
          "All existing data will be deleted. This process is irreversible.\n")
    print "WARNING: This command will reset the database. " \
          "All existing data will be deleted. This process is irreversible.\n"
    value = raw_input("Do you wish to continue (Y/n)? ")
    while value != "Y" and value != "n":
        logfile.write("Invalid option %s\n" % value)
        print "Invalid option %s\n" % value
        value = raw_input("Do you wish to continue (Y/n)? ")
    if value == "n":
	logfile.write("Operation cancelled.")
        print "Operation cancelled.\n"
        local_reset_db_abort = True
        result_tuple = [logfile, local_reset_db_abort]
        return result_tuple

    logfile.write("Do you wish to continue (Y/n)? %s" % value)
    print "resetting the db..."
    os.system("cd " + local_manage_py_dir() + "; python makahiki/scripts/initialize_postgres.py")
    result_tuple = [logfile, local_reset_db_abort]
    return result_tuple

def run(logfile):
    """
    Runs the makahiki/makahiki/scripts/initialize_instance.py --type default 
    script and logs the output to a file. This should only be used to initialize 
    local installations.
    """
    try:
        # Retrieve the user's home directory
        USER_HOME = subprocess.check_output(["echo $HOME"], stderr=subprocess.STDOUT, shell=True) 
        # Remove newline from expected "/home/<username>\n"
        USER_HOME = USER_HOME[:-1]
        USER_PROJECT_HOME = USER_HOME + "/makahiki"
        # cd to makahiki directory
        os.chdir(USER_PROJECT_HOME)

        # Capture console output from script_utils functions:
	normal_stdout = sys.stdout
        output_capturer = StringIO.StringIO()
        sys.stdout = output_capturer

        # Runs the initialization scripts in same order as 
        # makahiki/makahiki/scripts/initialize_instance.py
    	instance_type = None
    	heroku_app = None
    	manage_py = script_utils.manage_py_command()
    	manage_command = "python " + manage_py
    	fixture_path = "makahiki/fixtures"

        # Install requirements
	script_utils.install_requirements()

        # Switch back to standard I/O
        sys.stdout = normal_stdout
        output = output_capturer.getvalue()
        logfile.write(output)
        print(output)
        # Clear the logfile buffer.
        logfile.flush()
        os.fsync(logfile)
        
        # Reset the database 
        reset_db_result = local_reset_db(logfile)
	# If successful, write the output of local_reset_db to a logfile
        logfile = reset_db_result[0]
        local_reset_db_abort = reset_db_result[1]
        if local_reset_db_abort:
	    logfile.write("Warning: initialize_instance did not complete successfully.")
	    print "Warning: initialize_instance did not complete successfully."
	    end_time = termination_string()
	    logfile.write(end_time)
	    print end_time
	    return logfile
        else:
            # Resume capturing I/O
            normal_stdout = sys.stdout
            output_capturer = StringIO.StringIO()
            sys.stdout = output_capturer            
            
            # Sync the database
	    script_utils.syncdb(manage_command)

            # Switch I/O back, write output to logfile
            sys.stdout = normal_stdout
            output = output_capturer.getvalue()
            logfile.write(output)
            print(output)
            # Clear the logfile buffer.
            logfile.flush()
            os.fsync(logfile)

            # Resume capturing I/O
            normal_stdout = sys.stdout
            output_capturer = StringIO.StringIO()
            sys.stdout = output_capturer            

            # Copy static files
	    script_utils.copy_static_media(heroku_app)
            
            # Switch I/O back, write output to logfile
            sys.stdout = normal_stdout
            output = output_capturer.getvalue()
            logfile.write(output)
            print(output)
            # Clear the logfile buffer.
            logfile.flush()
            os.fsync(logfile)

            # Resume capturing I/O
            normal_stdout = sys.stdout
            output_capturer = StringIO.StringIO()
            sys.stdout = output_capturer 

            # Load data
    	    script_utils.load_data(manage_command, instance_type, fixture_path)
    	    
            # Switch I/O back, write output to logfile
            sys.stdout = normal_stdout
            output = output_capturer.getvalue()
            logfile.write(output)
            print(output)          
            # Clear the logfile buffer.
            logfile.flush()
            os.fsync(logfile)

            # Print a closing message
            closing = "\nMakahiki initialization script has completed.\n"
            logfile.write(closing)
            print closing
            end_time = termination_string()
            logfile.write(end_time)
            print end_time
            return logfile        

    except subprocess.CalledProcessError as cpe:
        logfile.write("CalledProcessError: ")
        print "CalledProcessError: "
        logfile.write(cpe.output)
        print cpe.output
        logfile.write("Warning: Makahiki initialization did not complete successfully.")
        print "Warning: Makahiki initialization did not complete successfully."
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile
    except OSError as ose:
        logfile.write("OSError: ")
        print "OSError: "
        logfile.write(ose.output)
        print ose.output
        logfile.write("Warning: Makahiki initialization did not complete successfully.")
        print "Warning: Makahiki initialization did not complete successfully."
        end_time = termination_string()
        logfile.write(end_time)
        print end_time
        return logfile
