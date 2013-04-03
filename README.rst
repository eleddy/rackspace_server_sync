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
