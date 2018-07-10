require 'mechanize'

unless ARGV[0]
  puts "You must supply a URL to scrape links."
  puts "USAGE: ruby linkScrape.rb <url to scrape>"
  exit
end


agent = WWW::Mechanize.new
agent.set_proxy('localhost',8080)

begin
  page = agent.get(ARGV[0].strip)
    

  page.links.each do |l|
    if l.href.split("")[0] =='/'
      puts "#{ARGV[0]}#{l.href}"
    else
      puts l.href
    end
  end
rescue => e
  puts "An error occurred."
  puts e
  retry
end