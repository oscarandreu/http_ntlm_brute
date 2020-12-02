# NTLM HTTP Brute force tool

## Usage

http_ntlm_brute.py [-h] -p <passwordsFile> -s <serviceURL> [-d <domain>] [-u <user>] [-U <usersFile>] [-t <threads>]  
  
HTTP NTLM cracking tool  
  
optional arguments:  
  -h, --help          show this help message and exit  
  -p <passwordsFile>  Passwords file  
  -s <serviceURL>     Service URL  
  -d <domain>         Domain name  
  -u <user>           User name  
  -U <usersFile>      Users file  
  -t <threads>        Number of threads, default 5  
 

## Example 

python3 http_ntlm_brute.py -s http://devops.worker.htb -u nathen -p passwords.list -d worker  