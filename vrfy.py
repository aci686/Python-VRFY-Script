#! /usr/bin/env python3

##
# This program checks if any given email address is valid on a particular server '
# Relies on AF_INET sockets and SMTP VRFY command to check '
##

__author__ = 'Aaron Castro'
__author_email__ = 'aaron.castro.sanchez@outlook.com'
__copyright__ = 'Aaron Castro'
__license__ = 'MIT'

# Needed libraries
import argparse, socket, sys

# Coloring output
class bcolors:
    INFO = '\033[96m'
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# Function to parse valid arguments

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--server', help='Server IP address or FQDN', required=True)
    email = parser.add_mutually_exclusive_group(required=True)
    email.add_argument('-e', '--email', help='Email address to test', type=str) 
    email.add_argument('-l', '--list', help='Email addresses list to test', type=str)
    parser.add_argument('-o', '--output', help='Output file for existing email addresses')    

    args = parser.parse_args()

    return(args)

# Core function. Takes an email account and server address. Then opens a connection to it,
# sends a SMTP VRFY command and gets its ouput. If the email account is valid, returns True.
# Otherwise, returns False

def vrfy(email, server):
    # Creates and opens the SMTP connection
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = conn.connect((server, 25))
    # Skips SMTP banner
    banner = conn.recv(1024)
    # Checks email address in the server
    conn.send('VRFY {} \n\r'.format(email).encode())
    result = conn.recv(1024)
    # Checks if return code is within success SMTP return codes...
    # https://tools.ietf.org/html/rfc821#page-34
    if result.decode()[0] == '2':
        account = True
    else:
        account = False
    # Shut opened connection
    conn.close()

    return(account)

def main():
    args = get_arguments()

    # Confirms which SMTP server are we using
    print('[' + bcolors.INFO + 'I' + bcolors.ENDC + '] ' + 'SMTP Server: ' + bcolors.HEADER + '{}'.format(args.server) + bcolors.ENDC)

    # Checks a particular email address specified as argument
    if args.server and args.email:
        print('[' + bcolors.INFO + 'I' + bcolors.ENDC + '] ' + 'Checking {}... '.format(args.email, args.server), end='')
        if vrfy(args.email, args.server):
            print(bcolors.OKBLUE + 'OK' + bcolors.ENDC)
        else:
            print(bcolors.FAIL + 'Not in there' + bcolors.ENDC)
        
    # Checks a list of email addresses if a list of them is provided by a filename given as argument
    if args.server and args.list:
        # Creastes output file if it was specified
        if args.output:
            # Creates if it does not exist and blanks it otherwise
            try:
                output = open(args.output, 'x')
            except:
                output = open(args.output, 'w')
        # Reads input file line by line
        with open(args.list, 'r') as input:
            for line in input:
                print('[' + bcolors.INFO + 'I' + bcolors.ENDC + '] ' + 'Checking ' + bcolors.HEADER + '{}... '.format(line.rstrip(), args.server) + bcolors.ENDC, end='')
                # Checking each particular email address
                if vrfy(line, args.server):
                    try:
                        output.write(line)
                    except:
                        pass
                    print(bcolors.OKBLUE + 'OK' + bcolors.ENDC)
                else:
                    print(bcolors.FAIL + 'Not in there' + bcolors.ENDC)
        try:
            output.close()
        except:
            pass

if __name__ == '__main__':
    main()
