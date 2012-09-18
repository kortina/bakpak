#!/usr/bin/ruby
require 'pathname'
ARGV.each do |f|
    dirname = File.dirname f
    basename = Pathname(f).basename.to_s
    insert = Time.now.strftime("%Y-%m-%d")
    if basename =~ /(.*)\.([^\.]+)$/
        dup = "#{$1}.#{insert}.#{$2}"
    else
        dup = "#{basename}.#{insert}"
    end
    cmd = "cd #{dirname} && cp -R #{basename} #{dup}"
    puts cmd
    `#{cmd}`
end
