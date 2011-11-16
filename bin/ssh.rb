#!/usr/bin/env ruby 

# Inspired by http://jeffmiller.github.com/2011/01/10/ssh-host-color

# == What this version does:
# 1) Launch an SSH process
# 2) Grab the IP that SSH connected to
# 3) Hash that IP and generate a colour from it
# 4) Change Terminal.app's background colour to that colour.
# 5) Change the colour back when SSH exits.

# == How to install:
# 1) Put this somewhere in your path. I put mine at ~/bin/ssh.

# == Caveats:
# - Only works with OS X. shouldn't be hard to port to Linux if you care.

# == Configuration:
# The range to be selected from for each or {r,g,b}. Change RANGE whatever you like, or use one of the presets.
DARK  = 0x00..0x33
LIGHT = 0xCC..0xFF
RANGE = DARK

# Your default background colour. E.g. black is [0,0,0], white is [255,255,255] or [0xff,0xff,0xff]
DEFAULT = [0,0,0]


require 'digest/sha1'

t=Thread.new do

  def set_color(r, g, b)

    cmd = <<CMD
/usr/bin/osascript <<EOF
  tell application "Terminal"
    tell window 0
      set the background color to {$((#{r}*65535/255)), $((#{g}*65535/255)), $((#{b}*65535/255))}
    end tell
  end tell
EOF
CMD

    system cmd
  end 

  def mapcolor(range, seed)
    size = range.last - range.first
    ((seed.to_i(16) * (size.to_f / 255.0)).to_i + range.first)
  end 
   
  def color_from_ip(range, ip)
    hash = Digest::SHA1.hexdigest(ip)
     
    r = mapcolor(range, hash[0..1])
    g = mapcolor(range, hash[2..3])
    b = mapcolor(range, hash[4..5])
   
    [r, g, b]
  end 

  this_pid = Process.pid

  child_pid = nil
  until child_pid
    child_pid = `ps -opid,ppid`.scan(/^\s*(\d+)\s+#{this_pid}$/).flatten.first
    sleep 0.1
  end 

  ip = nil
  until ip
    ip = `lsof -w -a -i -p #{child_pid} -Pn -Fn | tail -n1`.scan(/^n.*->(.*):.*$/).flatten.first
    sleep 0.1
  end 

  set_color(*color_from_ip(RANGE, ip))
  
end

END { set_color(*DEFAULT) }

system(*["/usr/bin/ssh", *ARGV])
