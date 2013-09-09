YASC: Yet Another Southwest Checkin
========================

A Python script for automatically checking into Southwest flights.

Usage:

`checkin.py <FIRSTNAME> <LASTNAME> <CONFIRMATIONNUMBER> (<EMAIL>)`

With [crontab](http://unixhelp.ed.ac.uk/CGI/man-cgi?crontab+5) (for a flight with a departure date of April 20 at 2:20 PM)

    $ crontab -l
    20 14 19 04 * cd ~/path/to/YASC && python checkin.py Benjamin Gleitzman G78ZOV gleitz@mit.edu # note checkin date of April 19 for the flight the next day

Extra notes:

*   Requires the excellent [Requests library](http://docs.python-requests.org/)
*   You may optionally provide an email address to send the boarding pass. If you do put your gmail username and password in a file called secret.txt separated by a double pipe character (e.g. `yourname@gmail.com||password`) and then run `chmod 600 secret.txt`
*   Southwest likes to change their login process rather regularly so YMMV.
