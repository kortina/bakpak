

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
