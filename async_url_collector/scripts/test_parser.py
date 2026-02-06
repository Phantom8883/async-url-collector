from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_images(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    imgs = []
    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            imgs.append(urljoin(base_url, src))
    return imgs


html = """
<html>
<body>
<img src="img1.jpg">
<img src="/img2.png">
<img src="https://example.com/img3.gif">
</body>
</html>
"""

base_url = "https://mysite.com/articles/"
images = extract_images(html, base_url)
print(images)