=======
Problem
=======
Using the rackspace api, write a script which gets a list of all of a users servers and updates the /etc/hosts file to map server names to ips. It can be run at any time so it should not duplicate and should work in both first and second generation rackspace servers. If an ip is updated, it should do its best to properly update the ip. External facing ips only.

========
Concepts
========

 *  `DNS Basics <http://docs.oracle.com/cd/E19455-01/806-1387/6jam692f2/index.html>`_ and another on how `/etc/hosts <http://www.freebsd.org/doc/en/books/handbook/configtuning-configfiles.html#AEN16796>`_ fits into that scheme.
 *  Using `cURL <http://curl.haxx.se/docs/httpscripting.html>`_
 *  For the curious and brave: `two factor authentication <http://en.wikipedia.org/wiki/Two-factor_authentication>`_ (which explains why the rackspace API uses tokens). Tokens `can be revoked <http://stackoverflow.com/questions/939836/service-based-authentication-using-tokens>`_ at any time and they are tied to a specific ip.
 * Making good choices on python package integration. Maintained, current, many followers/forks, "official", reputable

========
Solution
========
This script uses username and api_key information found in a local 'connect.cfg' file to collect server information (ip addresses and aliases), and writes that information to the /etc/hosts file. It will only add server information if 1) the ip and alias are not already in the hosts file, or 2) if the hosts file already has the ip but not the alias, in which case the alias is appended on to the list of aliases associated with that ip.  To run the script, first make sure to create a connect.cfg file in the same directory as sync_rackspace.py with the following format:

    [rackspace]
    username = <your_username>
    api_key = <your_password>

Additionally, the script assumes you have access to root privileges since the /etc/hosts file is protected. You will be prompted to enter your password before the script overwrites the /etc/hosts file.

=============
Helpful Stuff
=============
* `PDB Tutorial <http://pythonconquerstheuniverse.wordpress.com/2009/09/10/debugging-in-python>`_ If you guys still aren't using pdb, I highly *highly* recommend it. Especially when working with an outside api, where you have some json object and have to trace down to find the value that you're looking for. It's also great when things are blowing up, since it allows you to freeze time and poke around a little bit - see what values your variables are or what type of object your working with. 
* `dir() <http://docs.python.org/2/library/functions.html#dir>`_ and `type() <http://docs.python.org/2/library/functions.html#type>`_ I find I use these two functions a lot. dir() without an argument will show you all the names (eg, variables, classes, modules) you have defined, and with an argument, eg dir(my_var), will show you the methods and attributes associated with that object. type() will return, you guessed it, the type of the variable passed to it. I find it really helpful when trying to figure out what I'm looking at the deeper I get into a json object, or when trying to figure out what a method/function returns. 
* `for loop else <http://docs.python.org/2/tutorial/controlflow.html#break-and-continue-statements-and-else-clauses-on-loops>`_ I just recently found out the forloop has an else, and it kinda blew my mind. I used it in this script I wrote and plan on making some heavy use of it in the future.