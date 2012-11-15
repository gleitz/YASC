YASC: Yet Another Southwest Checkin
========================

A Python script for automatically checking into Southwest flights. Works as of November 2012. You may optionally provide an email address to send the boarding pass. If you do, put your gmail username and password in a file called secret.txt, separated by a double pipe character (e.g. yourname@gmail.com||password)

`checkin.py <FIRSTNAME> <LASTNAME> <CONFIRMATIONNUMBER> (<EMAIL>)`

Extra notes:

*   Requires the excellent [Requests library](http://docs.python-requests.org/)
*   Southwest likes to change their login process rather regularly so YMMV.
