from tld import get_tld

def domain_name(url):
	domain = get_tld(url)
	return domain