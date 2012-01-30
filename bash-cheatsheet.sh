

# foreach string
for ss in "hello" "world"; do echo $ss; done;


# grep -q is an easy way to do switch on proram output or file contents
echo "dog " > ~/tmp/test.txt
grep -q dog ~/tmp/test.txt || echo "dog not found"
grep -q ball ~/tmp/test.txt || echo "ball not found"
grep -q dog ~/tmp/test.txt && echo "dog found"
grep -q ball ~/tmp/test.txt && echo "ball found"

# grep -q with if conditional
if grep -q dog ~/tmp/test.txt ; then 
    echo 1; 
fi;
if grep -q ball ~/tmp/test.txt ; then 
    echo 2; 
fi;


# conditional based on exit status
someprogthatdoesntexist
if [ "$?" -ne 0 ]; then echo "failed. someprogthatdoesntexist exited non-zero"; fi;
echo "a"
if [ "$?" -ne 0 ]; then echo "this won't print cause echo exited 0"; fi;


# symlinks
ln -s /path/target /path/to/symlink
## update existing symlink to file
ln -sf /new/targetfile /path/to/symlink
## update existing symlink to directory
ln -sfn /new/targetdir /path/to/symlink

# test if a file is a symlink or not
test -h /path/possible_sym || echo "possible_sym is NOT a symlink"
test -h /path/possible_sym && echo "possible_sym IS a symlink"


# file renaming util
for i in *.avi; do j=`echo $i | sed 's/find/replace/g'`; mv "$i" "$j"; done


# ssh tunnel
# http://blog.kenweiner.com/2007/09/reverse-ssh-tunnel-for-facebook.html

ssh -gNR 8888:localhost:8080 www.myremoteserver.com

"Forward requests on www.myremoteserver.com:8888 to my workstation port 8080."

     -g Allows remote hosts to connect to local forwarded ports.
     -N Do not execute a remote command.  This is useful for just forwarding ports (protocol version 2 only).
     -R [bind_address:]port:host:hostport
        Specifies that the given port on the remote (server) host is to be
        forwarded to the given host and port on the local side.  This works by
        allocating a socket to listen to port on the remote side, and whenever
        a connection is made to this port, the connection is forwarded over the
        secure channel, and a connection is made to host port hostport from the
        local machine.


NB: You will need to edit /etc/ssh/sshd_config and add the following line:

    GatewayPorts yes

Forward requests made to localhost:27018 to remoteserver:27017

    ssh -N -i ./rsa_private_key -L 27018:localhost:27017 ubuntu@remoteserver.com

