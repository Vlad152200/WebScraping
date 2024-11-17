import re

text = """Welcome to the Regex Training Center! 

01/02/2021, 12-25-2020, 2021.03.15, 2022/04/30, 2023.06.20, and 2021.07.04. You can
also find dates with words: March 14, 2022, and December 25, 2020. 

(123) 456-7890, +1-800-555-1234, 800.555.1234, 800-555-1234, and 123.456.7890. 
Other formats include international numbers: +44 20 7946 0958, +91 98765 43210.

john.doe@example.com, jane_doe123@domain.org, support@service.net, info@company.co.uk, 
and contact.us@my-website.com. You might also find these tricky: weird.address+spam@gmail.com,
"quotes.included@funny.domain", and this.one.with.periods@weird.co.in.

http://example.com, https://secure.website.org, http://sub.domain.co, 
www.redirect.com, and ftp://ftp.downloads.com. Don't forget paths and parameters:
https://my.site.com/path/to/resource?param1=value1&param2=value2, 
http://www.files.net/files.zip, https://example.co.in/api/v1/resource, and 
https://another-site.org/downloads?query=search#anchor. 

0x1A3F, 0xBEEF, 0xDEADBEEF, 0x123456789ABCDEF, 0xA1B2C3, and 0x0. 

#FF5733, #C70039, #900C3F, #581845, #DAF7A6, and #FFC300. RGB color codes can be tricky: 
rgb(255, 99, 71), rgba(255, 99, 71, 0.5).

123-45-6789, 987-65-4321, 111-22-3333, 555-66-7777, and 999-88-7777. Note that Social 
Security numbers might also be written like 123 45 6789 or 123456789.

Let's throw in some random sentences for good measure:
- The quick brown fox jumps over the lazy dog.
- Lorem ipsum dolor sit amet, consectetur adipiscing elit.
- Jack and Jill went up the hill to fetch a pail of water.
- She sells seashells by the seashore.

123456789, !@#$%^&*()_+-=[]{}|;':",./<>?, 3.14159, 42, and -273.15.
"""

def use_re():
    pattern_email = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9_.+-]+\.[a-zA-Z]{2,}'
    email = re.findall(pattern_email,text)
    print(email)

    pattern_dates = r'(?:\b\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{4}\b|\b\d{4}[\/\.-]\d{1,2}[\/\.-]\d{1,2}|\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}\b)'
    dates = re.findall(pattern_dates,text)
    print(dates)

    #pattern_url = r'(([a-zA-Z]{2,}:\/\/(www\.)?|www.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\/[^\s]*)?)'
    pattern_url = r'(?:[a-zA-Z]{2,}:\/\/(?:www\.)?|www\.)[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}(?:\/[^\s]*)?'
    url = re.findall(pattern_url,text)
    print(url)

    pattern_num = r'\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{4,5}'
    num = re.findall(pattern_num,text)
    print(num)

if __name__ == '__main__':
    use_re()
