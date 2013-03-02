Password Generator
==================

This repository contains a simple password generator, suitable for command-line
use or embedding into a PHP or Python project.

By default, the generator provides secure and random passwords guaranteed to
satisfy the following requirements:

- 8 characters.

- At least one character from each of the following categories: upper case
  letters, lower case letters, digits.

- No homoglyphs (characters that look alike, such as the number ``0`` and the
  letter ``O``).


Files
-----

The following files are included:

- ``PasswordGenerator.php``: PHP implementation.

- ``passwordgenerator.py``: Python implementation.

The Python implementation improves on the PHP version in that it uses the OS
secure random functionality (``/dev/urandom`` on Linux, ``CryptGenRandom`` on
Windows), and allows a password length to be specified on the command-line.


Usage
-----

Generate a password::

    ./passwordgenerator.php
    ./passwordgenerator.py

Generate a password of custom length (not supported in the PHP version)::

    ./passwordgenerator.py 12

Estimate entropy (number of possible password combinations)::

    ./passwordgenerator.php -e
    ./passwordgenerator.py -e


Comparison to alternatives
--------------------------

A password generator is not a novel idea, and most Linux distros include a few
in their packages repositories, such as `pwgen`__  and `makepasswd`__.

__ http://manpages.ubuntu.com/manpages/dapper/man1/pwgen.1.html
__ http://manpages.ubuntu.com/manpages/dapper/man1/makepasswd.1.html


=========================   =====================  ====================  ==========  ==============
Feature                     PasswordGenerator.php  passwordgenerator.py  pwgen       makepasswd
=========================   =====================  ====================  ==========  ==============
Implementation language     PHP                    Python                C           Perl
Password length             Fixed (8)              Any                   Any         Any
Password complexity         Alphanumeric           Alphanumeric          Any         Letters only
Uses secure random?         No                     Yes                   Yes         Yes
Avoids homoglyphs?          Yes                    Yes                   Optionally  No
Estimates entropy?          Yes                    Yes                   No          No
=========================   =====================  ====================  ==========  ==============


Public Domain Dedication
------------------------

To the extent possible under law, the author has waived all copyright and
related or neighboring rights to Password Generator.

For more information see:
http://creativecommons.org/publicdomain/zero/1.0/
