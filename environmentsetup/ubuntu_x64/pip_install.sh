# pip_install.sh
# Sets up the Makahiki local installation or development environment by
# installing project-specific dependencies.
# Target operating system: Ubuntu Linux (64-bit).

# To record all the output from this script, use tee to redirect it:
# sh pip_install.sh | tee <file-to-write-to>

# Enter your username and password to enable sudo when prompted.

echo "Makahiki Pip Install Script for Ubuntu (x64)"
echo "Script 2 of 2"
echo "--------------------------------------------------"
echo "Script started at $(date)"

# Check that the first script was run.
echo "Did you run environment_setup.sh before running this script [Y/n]:"
read PART1_OK
if [ "$PART1_OK" != "Y" ]
	then
		echo "To be able to run this script, you must: "
		echo "1. Run the environment_setup.sh script"
		echo "2. Configure and initialize the makahiki virtual environment."
		echo "3. Run this script when you are in the makahiki virtual environment."
		echo "Script exiting at $(date)."
		exit 1
fi

# Ask user if Makahiki virtual environment exists
echo "Did you create the Makahiki virtual environment [Y/n]:"
read VIRTUALENV_EXISTS
if [ "$VIRTUALENV_EXISTS" != "Y" ]
	then
		echo "Please create the makahiki virtual environment before running this script."
		echo "Script exiting at $(date)."
		exit 1
fi

# Ask user if they are in the makahiki virtual environment.
echo "Did you run this script in the makahiki virtual environment [Y/n]:"
read IN_VENV
if [ "$IN_VENV" != "Y" ]
	then
		echo "This script must be run in the Makahiki virtual environment."
		echo "Script exiting at $(date)."
		exit 1
fi

# This script assumes that requirements.txt is in the top-level 
# makahiki directory. $PROJECT_HOME is set by the virtual environment.
if [ ! -f $PROJECT_HOME/requirements.txt ]
	then
		echo "requirements.txt file not found in makahiki."
		echo "pip could not be used to install dependencies."
		echo "Script exiting at $(date)."
		exit 1
fi

# Install dependencies with pip
echo "Starting pip install."
echo "pip install -r $PROJECT_HOME/requirements.txt"
pip install -r $PROJECT_HOME/requirements.txt
echo "pip install has completed."

echo "Script completed at $(date)"
exit 0
