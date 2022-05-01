# CPSC-456-Worm-Assignment Spring 2022 
#### Group Members
Name: Akshaya Kizhkkencherry ; CWID: 885958652
      Shivani Patel ;  CWID: 887414993
      

## Project Description:
Executing the program will look through the hosts on the virutal environment and try to spread and execute itself there with an infected.txt file. As from the assignment description, we used GNS# to create the network topology with Lubuntu VM's provided in class as our basis of testing the code and executing it.
 
Primary Attack Machine:  Lubuntu 1 (10.20.22.2)

Target Machine: Lubuntu 2 (10.20.22.3) and Lubuntu 3 (10.20.22.4)

Credentials - Username: akshayak        Password: Aksh2000   (These are the orginal credentials for all the VM's used)



**Instructions for executing the worm program:**

You first must choose a VM, within the internal network of VMs, which you want to execute the worm from. Once selected, you execute by typing:
python3 worm.py.

**Extra Credit**

The first part of the extra credit has been attempted where we integrated a cleaner function to self-clean the worm in the infected machines. To execute the cleaner function we use either of the commands python worm.py -c or python worm.py --clean. 



The second part of the extra credit has also be been attempted for the code but we havent implmented it using the topology.
```
def extendspread():

   hosts= nmap.PortScanner()
   liveHosts = []
   for host in hosts:
        if portScanner[host].state() == "up":    
            liveHosts.append(host)
            
   if  "-m" in sys.argv or "--multi" in sys.argv:
        mPortScanner = nmap.PortScanner()
        mPortScanner.scan('10.20.22.0/25', arguments='-p 22 --open')
        multiData = mPortScanner.all_hosts()

        for multiHost in multiData:
            if mPortScanner[multiHost].state() == "up":
                liveHosts.append(multiHost)
    
    return liveHosts
```
