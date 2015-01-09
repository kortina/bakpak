#!/usr/bin/env ruby

usage = <<EOF
Make some text more "unixy"

tunixy.rb

Example:
echo -e "“" | tunixy.rb 
"

EOF
=begin
Installation:

chmod 700 tunixy.rb
mv tunixy.rb to a directory on your PATH

=end

# replace double curly quotes
# replace curly single quotes
# replace control characters
# replace tabs with newlines
# replace 3+ newlines with only 2 newlines
puts STDIN.read.gsub(/“|”/, '"').gsub(/‘|’/, "'").gsub(/\^L+/, "").gsub(/\r/, "\n").gsub(/^\t+/, "\n").gsub(/\n{3,}/, "\n\n")
