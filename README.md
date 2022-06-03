## Introduction ##
Are you using `rooms.nl` to look for a place to rent in the Netherlands?  
Do you want to know when new places become available?  
Would you rather receive an email than repeatedly check manually?

You sound like a very specific person, and you came to the right git repo.


---

## Summary ##

This program checks recent listings for rooms available to rent (in Amsterdam specifically, by default).
If new rooms are found, they will be emailed according to the command line arguments you pass it.
It then saves what it has seen to disk, so that the program knows which rooms are new the next time it is run.

---


## Usage ##

To use this program, simply run main.py with the following required positional arguments:
`sender email username` `sender email password` `email recipient`  
There are also two optional positional arguments:
`email domain` and `email port`

To get the full use out of this program, it is recommended to be run automatically and repeatedly, like as a cron job.
However, that would certainly have negative security implications, as the email login information is supplied via command line.
A system that stores and obfuscates the login information in memory would be better, however that is out of scope for this program.
So if you have a cron program that hides its entries, I'd suggest using that.
Alternatively, the email address you use to send emails could be a throwaway one.


---

## Requirements ##

* Python version 3
* An internet connection
