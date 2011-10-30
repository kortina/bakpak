#!/usr/bin/env ruby

`svn diff #{ARGV.join(' ')}`.each do |line|
  puts( if line =~ /^\+(.*)$/
        "\e[32m#{$&}\e[0m" 
        elsif line =~ /^-(.*)$/
          "\e[31m#{$&}\e[0m" 
        else
          line
        end
      )
end