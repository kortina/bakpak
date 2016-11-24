#!/usr/bin/env ruby

usage = <<EOF
gsub.rb [-i] [-v] regexp

Example:
echo -e "Yours truly,\nBetty" | gsub.rb -i "(yours)[^,]+," "\1,"
Yours,
Betty

EOF
=begin
Installation:

chmod 700 gsub.rb
mv gsub.rb to a directory on your PATH

=end

supported_flags = {
    #"-v" => "verbose", # TODO: add verbose mode
    "-i" => "case_insensitive"
}
reg = nil
rep = nil
argcount = 0
comp_args = []
until ARGV.empty? do
    a = ARGV.shift
    if supported_flags.has_key? a
        comp_args.push(Regexp::IGNORECASE) if a == "-i" # TODO: this should be some sort of cleaner switch statement
        # puts "Set: flag #{supported_flags[a]}"
    else
        argcount += 1
        if argcount == 1
            reg = a
        elsif argcount == 2
            rep = a
        end
    end
end

abort("Invalid # of arguments.\n#{usage}") unless argcount == 2
#puts "reg is #{reg}"
#puts "rep is #{rep}"
comp = Regexp.compile(reg, *comp_args)

# had to mod to get actual tabs etc inserted
rep = rep.gsub("\\t", "\t")
rep = rep.gsub("\\n", "\n")
while line = gets
    puts line.gsub(comp, rep)
end
