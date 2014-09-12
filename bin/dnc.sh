#!/bin/bash
# dnc - Domain Name Checker
# 
# adapted from http://bashscripts.org/forum/viewtopic.php?f=7&t=220 by Crouse

tld=(.com .net .org .co .ly .io)

if [ -z "$1" ] ; then
   echo ""
   echo "Missing required argument, [domain]"
   echo ""
   echo "USAGE: $0 [domain]";
   echo ""
   echo "EXAMPLE:";
   echo "$0 bashscripts";
   echo "will check availability of bashcripts{${tld[*]}}";
   echo ""
   exit;
fi

echo ""
echo "======== DNC Started  ========";echo ""
domainname=$1
declare -a tld
# You can put other tld extensions into the array, just remember to
#  add more numbers to the "num" section for every new tld extension.... next num needed as shown would be 4.
for num in 0 1 2 3
   do
      digdomain="$domainname${tld[num]}"
      dig $digdomain | grep "QUERY: 1, ANSWER: 0," &>/dev/null
         if [ $? -ne 0 ]; then
            echo "$digdomain is registered"
         else
            whois $digdomain | grep -i "Updated On" &>/dev/null
               if [ $? -eq 0 ]; then
                  echo "$digdomain is registered"
                     else
                        echo -ne "$digdomain is " ;tput smso; echo "AVAILABLE"; tput rmso;
               fi
         fi
   done
echo "";echo "======== DNC Finished ========";echo ""
exit
