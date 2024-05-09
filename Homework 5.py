#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def github() -> str:
    """
    Returns a link to solutions on GitHub.
    """
    return "https://github.com/drobon481/drobon481/tree/main"

print(github())


# In[10]:


import requests
from bs4 import BeautifulSoup
import re

def scrape_code(lecture_url: str) -> str:
    # Fetch the HTML content of the lecture URL
    response = requests.get(lecture_url)
    #response.ok
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all <pre> tags containing Python code
    code_blocks = soup.find_all('pre', class_='python')
    
    # Extract the code from each block
    python_code = ''
    for block in code_blocks:
        code = block.get_text()
        
        # Remove ipython magic commands
        code = re.sub('^%.*\n', '', code, flags=re.MULTILINE) # do this for every new line
        
        # Append the code to the result string
        python_code += code + '\n\n' # put spaces between each line
        
    # time.sleep(5) ##in case a loop is made
    return python_code

# Usage
#1 lecture_url = 'https://lukashager.netlify.app/econ-481/01_intro_to_python'
#2 lecture_url = 'https://lukashager.netlify.app/econ-481/02_numerical_computing_in_python'
#3 lecture_url = 'https://lukashager.netlify.app/econ-481/03_pandas'
lecture_url = 'https://lukashager.netlify.app/econ-481/05_web_scraping'

python_code = scrape_code(lecture_url)
print(python_code)


# In[ ]:




