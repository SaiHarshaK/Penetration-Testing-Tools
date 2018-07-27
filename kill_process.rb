#!/usr/bin/ruby

max = 300
ps_list = `ps h -eo cputime, pcpu, pid, user, cmd`


list = ps_list.split(/\n/)


list.each do |p|
  process = p.split
  process[0] =~ /(\d+):(\d+):(\d+)/
  cpu_time = $1*3600 + $2*60 + $3
  next if cpu_time < $max
  next if process[3] == "root" or process[3] == "postfix"
  next if process[4] == "kdeinit"
	
  begin
    print "Kill: #{process[4]} (y/n)? "
    if gets.downcase == "y"
      Process.kill :TERM,process[2]	
    end
  rescue
    puts "Couldn't kill the process. Please check permission."
    retry
  end
end