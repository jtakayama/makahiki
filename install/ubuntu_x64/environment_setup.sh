# environment_setup.sh
# Sets up the Makahiki local installation or development environment by
# installing packages and configuring the .bashrc with settings for 
# virtualenvwrapper.
# Target operating system: Ubuntu Linux (64-bit).

# To record all the output from this script, use tee to redirect it:
# sh environment_setup.sh | tee <file-to-write-to>

# Enter your username and password to enable sudo when prompted.

echo "Makahiki Environment Setup Script for Ubuntu (x64)"
echo "Script 1 of 2"
echo "--------------------------------------------------"
echo "Script started at $(date)"

echo "Is Python 2.7.3 or higher (but not Python 3) installed? [Y/n]:"
read PYTHON_OK
if [ "$PYTHON_OK" != "Y" ]
	then
		echo "Please install Python 2.7.3 or higher (not Python 3)."
		echo "Script exiting at $(date)."
		exit 1
fi

echo "The script will install these packages and their dependencies:"
echo "gcc"
echo "python-setuptools" 
echo "pip" 
echo "virtualenvwrapper"
echo "Python Imaging Library (python-imaging, python-dev, libjpeg-dev)"
echo "postgresql-9.1" 
echo "libpq-dev"
echo "Memcached (memcached, libmemcached-dev)"
SCRIPT_OK="n"
echo "Continue? [Y/n]:"
read SCRIPT_OK
if [ "$SCRIPT_OK" != "Y" ]
	then
		echo "Script exiting at $(date)."
		exit 1
fi
echo "Certain installations will require sudo permissions."
echo "Give your username and/or password for sudo if prompted."

# gcc
echo "gcc will be installed."
echo "sudo apt-get install -y gcc"
sudo apt-get install -y gcc

# python-setuptools
echo "python-setuptools will be installed."
echo "sudo apt-get install -y python-setuptools"
sudo apt-get install -y python-setuptools

# pip
echo "pip will be installed."
echo "sudo easy_install pip"
sudo easy_install pip

# Python Imaging Library
echo "Python Imaging Library components python-imaging, python-dev and "
echo "libjpeg-dev will be installed."
echo "sudo apt-get install -y python-imaging python-dev libjpeg-dev"
sudo apt-get install -y python-imaging python-dev libjpeg-dev
# Python Imaging Library shared library symlink setup
echo "Checking locations of Python Imaging Library shared libraries."
if [ ! -f /usr/lib/libjpeg.so ]
	then
	    if [ -f /usr/lib/x86_64-linux-gnu/libjpeg.so ]
			then
				echo "Found: /usr/lib/x86_64-linux-gnu/libjpeg.so"
				echo "Creating symlink: /usr/lib/x86_64-linux-gnu/libjpeg.so --> /usr/lib/"
				echo "sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/"
				sudo ln -s /usr/lib/x86_64-linux-gnu/libjpeg.so /usr/lib/
			else
				echo "Could not find libjpeg.so in /usr/lib or /usr/lib/x86_64-linux-gnu/." 
				echo "Python Imaging Library packages may not have installed properly."
				echo "Script exiting at $(date)."
				exit 1
		fi
	else
		echo "Found: /usr/lib/libjpeg.so"
fi

if [ ! -f /usr/lib/libz.so ]
	then
		if [ -f /usr/lib/x86_64-linux-gnu/libz.so ]
			then
				"Found: /usr/lib/x86_64-linux-gnu/libz.so"
				echo "Creating symlink: /usr/lib/x86_64-linux-gnu/libz.so --> /usr/lib/"
				echo "sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/"
				sudo ln -s /usr/lib/x86_64-linux-gnu/libz.so /usr/lib/
			else
				echo "Could not find libz.so in /usr/lib or /usr/lib/x86_64-linux-gnu/."
				echo "Python Imaging Library packages may not have installed properly."
				echo "Script exiting at $(date)"
				exit 1
		fi
	else
		echo "Found: /usr/lib/libz.so"
fi
echo "Python Imaging Library shared libraries check is complete."

# postgresql
echo "PostgreSQL 9.1 will be installed."
echo "sudo apt-get install -y postgresql-9.1"
sudo apt-get install -y postgresql-9.1

# libpq-dev
echo "libpq-dev will be installed."
echo "sudo apt-get install -y libpq-dev"
sudo apt-get install -y libpq-dev

# memcached
echo "memcached and libmemcached-dev will be installed."
echo "sudo apt-get install memcached"
sudo apt-get install -y memcached
echo "sudo apt-get install libmemcached-dev"
sudo apt-get install -y libmemcached-dev

# virtualenvwrapper installation
echo "virtualenvwrapper will be installed."
echo "sudo pip install virtualenvwrapper"
sudo pip install virtualenvwrapper

# virtualenv ~/.bashrc setup
echo "Setting locations in ~/.bashrc file:"
echo "Virtual environment locations: WORKON_HOME=$HOME/.virtualenvs"
USER_PROJECT_HOME="$HOME/makahiki"
PROJECT_HOME_OK="n"
echo "Default virtualenv project directory is $USER_PROJECT_HOME."
echo "Is this OK? [Y/n]:"
read PROJECT_HOME_OK
if [ "$PROJECT_HOME_OK" != "Y" ]
	then
		echo "Enter full path to project directory:"
		read USER_PROJECT_HOME
fi 

echo "Appending these lines to the current user's ~/.bashrc file:"
echo "export WORKON_HOME=$HOME/.virtualenvs"
echo "export PROJECT_HOME=$USER_PROJECT_HOME"
echo "source /usr/local/bin/virtualenvwrapper.sh"
echo "Appending to .bashrc file:"
# Append lines to end of ~/.bashrc file:
echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.bashrc
echo "export PROJECT_HOME=$USER_PROJECT_HOME" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
# Done appending to ~/.bashrc file
echo "~/.bashrc locations have been set."

echo "Script completed at $(date)"
exit 0
