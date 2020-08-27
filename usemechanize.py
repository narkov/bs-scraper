import mechanize
import re # write a regex to get the parameters expected by __doPostBack
from bs4 import BeautifulSoup
from time import sleep


br = mechanize.Browser()
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
url = "https://www.xxxxx/"
response = br.open(url)

# satisfy the __doPostBack function to navigate to different pages 
for pg in range(2,5):
    br.select_form(nr=0) # the only form on the page
    br.set_all_readonly(False) # to set the __doPostBack parameters

    soup = BeautifulSoup(response, 'html.parser')
    table = soup.find('table', {'class': 'course-list-state'})
    records = table.find_all('tr')

    for rec in records:
        if not rec.h3:
          break
        company = rec.h3.string.strip()
        addr = rec.div.div.getText().strip().replace("Australia", "")
        print('"', company, '","', addr, '"')

    # disable 'Search' and 'Clear filters'
    for control in br.form.controls[:]:
        if control.type in ['submit', 'image', 'checkbox']:
            control.disabled = True

    # get parameters for the __doPostBack function
    for link in soup("a"):
        if link.string == str(pg):
            next = re.search("""<a href="javascript:__doPostBack\('(.*?)','(.*?)'\)">""", str(link))
            br["__EVENTTARGET"] = next.group(1)
            br["__EVENTARGUMENT"] = next.group(2)
    sleep(1)    
    response = br.submit()
