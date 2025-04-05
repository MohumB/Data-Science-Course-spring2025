from bs4 import BeautifulSoup
import requests

url = "https://standardebooks.org/ebooks/charles-dickens/david-copperfield/text/single-page"


response = requests.get(url)


if response.status_code == 200:
    html_content = response.text
else:
    print("Failed to access the page:", requests.status_codes)
    
soup = BeautifulSoup(html_content, "html.parser")

title_element = soup.find("h2", attrs = {"epub:type" : "fulltitle"})

if title_element:
    title_text = title_element.get_text()
    print("Book Title:", title_text)
else:
    print("Title not found.")

chapter_elements = soup.find_all("p", attrs = {"epub:type" : "title"})

chapters = []
for chapter in chapter_elements:
    chapters.append(chapter.get_text())

paragraphs = soup.find_all("p")

full_content = "\n\n".join([paragraph.get_text() for 
                            paragraph in paragraphs])

with open("David_Copperfield.txt", "w", 
          encoding = "utf8") as file:
    file.write(full_content)
    

    
