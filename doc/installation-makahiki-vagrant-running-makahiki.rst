.. _section-installation-makahiki-vagrant-running-makahiki-vagrant:

Running Makahiki on Vagrant
===========================

This article describes maintenance tasks for the Makahiki database, 
and describes the process for starting and stopping the Makahiki web 
server.

Here, ``%`` indicates that a command can be performed from 
any working directory in the virtual machine. Directories 
are specified otherwise.

Initialize Makahiki
-------------------

The provisioning script that was run when the virtual machine was started for 
the first time initialized the database. This section describes how to 
initialize the database again.

.. warning:: Running the initialize_instance.py script will:

     * Install and/or update all pip-installed packages required by Makahiki.
     * Reinitialize the database contents and perform any needed database migrations.
     * Initialize the system with data.
     * Set up static files.

   This script should be run only a single time in production scenarios, because 
   any subsequent configuration modifications will be lost if initialize_instance 
   is invoked again.

   The script initializes the Makahiki database and populates it with default 
   information and users.

Switch to the /vagrant/makahiki directory::

  vagrant@precise32:~/$ cd /vagrant/makahiki
  vagrant@precise32:/vagrant/makahiki$ ./scripts/initialize_instance.py --type default

You will need to answer ``Y`` to the question ``Do you wish to continue (Y/n)?``.

If the script experiences errors while connecting to the database, see 
:ref:`section-installation-makahiki-vagrant-troubleshooting`.

Update the Makahiki Instance
----------------------------

Makahiki is designed to support post-installation updating of your configured 
system when bug fixes or system enhancements become available.

Close the running server in the shell process that is running Makahiki::

  (type control-c in the shell running the makahiki server process)

Go to the vagrant directory (the makahiki directory on the host machine)::

  % cd /vagrant

Download the updated source code into the Makahiki installation::

  vagrant@precise32:/vagrant$ git pull origin master

Switch to vagrant/makahiki and run the update_instance.py script::

  vagrant@precise32:/vagrant$ cd makahiki
  vagrant@precise32:/vagrant/makahiki$ ./scripts/update_instance.py

Start the server with runserver or gunicorn.

To start the runserver server::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver

To start the gunicorn server::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn

Start the Makahiki Server
-------------------------

This guide assumes you are in the directory /vagrant/makahiki on the 
virtual machine.

Makahiki's manage.py script provides two web servers: runserver and gunicorn.
runserver is better for development, and gunicorn is better for production use. 

It is important to bind the server to IP 0.0.0.0 (accepts incoming connections 
on any IP address) and port 8000 in order to work with the port forwarding 
settings in the Vagrantfile.

To start the server with manage.py::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000

To start the server with gunicorn::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py run_gunicorn -b 0.0.0.0:8000

View the site in your host machine's web browser at http://192.168.56.4:8000.

Log in with the username (admin) and password (admin) specified in 
makahiki_env.sh. 

To stop either of the servers, type Control-C in the virtual machine terminal.

Testing the Server Without a Web Browser
****************************************

If you cannot reach the web server from the host machine, you will need to 
use wget to test the server on the virtual machine::

  vagrant@precise32:/vagrant/makahiki$ ./manage.py runserver 0.0.0.0:8000 &
  Validating models...
  
  Development server is running at http://127.0.0.1:8000/
  Quit the server with CONTROL-C.
  vagrant@precise32:/vagrant/makahiki$ (press "Enter" here)
  vagrant@precise32:/vagrant/makahiki$ cd ~/
  vagrant@precise32:~$ mkdir test
  vagrant@precise32:~/test$ cd test
  vagrant@precise32:~/test$ wget http://127.0.0.1:8000
  --2013-08-09 11:19:25--  http://127.0.0.1:8000/
  Connecting to 127.0.0.1:8000... connected.
  HTTP request sent, awaiting response... 302 FOUND
  Location: http://127.0.0.1:8000/landing/ [following]
  [09/Aug/2013 11:19:26] "GET / HTTP/1.0" 302 0
  --2013-08-09 11:19:26--  http://127.0.0.1:8000/landing/
  Connecting to 127.0.0.1:8000... connected.
  HTTP request sent, awaiting response... 200 OK
  Length: unspecified [text/html]
  [09/Aug/2013 11:19:26] "GET /landing/ HTTP/1.0" 200 6181
  Saving to: “index.html"
  
      [ <=>                                   ] 6,181       --.-K/s   in 0s

  2013-08-09 11:19:26 (192 MB/s) - “index.html" saved [6181]

If your HTTP response is "200 OK," the server is running correctly. You can 
delete the "test" directory when you are done.

Because this server was started in the background with ``&``, you cannot stop 
it with Control-C. You will need to find the PIDs of its processes first::

  % ps ax | grep manage.py
  21791 tty1     S     0:00 python ./manage.py runserver
  21798 tty1     Sl    0:52 /root/.virtualenvs/makahiki/bin/python ./manage.py ru
  nserver
  21893 tty1     S+    0:00 grep manage.py
  % kill -9 21791 21798
  % 
  [1]+  Killed                 ./manage.py runserver  (wd: ~/makahiki/makahiki)
  (wd now: <your-working-directory>)

The PID of a given process will be different each time it runs. ``kill -9 <PID>`` 
forces the OS to stop the process. Kill the ``python ./manage.py runserver`` 
and ``/root/.virtualenvs/makahiki/bin/python ./manage.py runserver`` processes 
to stop the server.




