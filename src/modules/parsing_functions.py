import pandas as pd
import time
import re
import requests
import nbformat

from collections import OrderedDict

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException



def PARSING_COMPETITION_NOTEBOOKS(COMPETITION_URL, SORT_BY='public score', PYTHON_ONLY=True, excludeNonAccessedDatasources=True, NOTEBOOKS_AMOUNT = 5):
    
    columns = ["notebook_name", "notebook_url", "public_score", "private_score", "medal", "upvotes", "views", "run_time_info", "last_updated", "notebook_full_text", "code_text", "markdowns_text", "input_datasources", "python_libraries"]
    df = pd.DataFrame(columns=columns)
    
    start_time = time.time()
    print('PARSING LINKS,  Time = ', 0)
    
    # -------------------------------------------------------------------------------------------------------------------------------------------------------
    # BLOCKING ALL DOWNLOADS
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.set_preference("browser.download.folderList", 2)  # Use the last directory specified for downloads
    firefox_options.set_preference("browser.download.dir", "./downloads")  # Specify the download directory [directory does not exists -> not downloading at all]
    firefox_options.set_preference("browser.download.useDownloadDir", True)  # Use the specified download directory
    firefox_options.set_preference("browser.download.manager.showWhenStarting", False)  # Do not show download manager
    firefox_options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream")  # Prevent automatic download of certain file types
    firefox_options.headless = True  # Run in headless mode to hide browser window
    driver = webdriver.Firefox(options=firefox_options)

    # Load the webpage
    driver.get(COMPETITION_URL)
    
    # # Wait for some time to allow dynamic content to load (you can adjust the time accordingly)
    # time.sleep(2)
    
    # finding COMPETITION ID through the header (banner image)
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//img[contains(@src, '/competitions/') and contains(@src, '/images/header')]")))
    required_str = driver.find_element(By.XPATH, "//img[contains(@src, '/competitions/') and contains(@src, '/images/header')]").get_attribute('src')
    competition_id = re.search(r'/(\d+)/', required_str).group(1)
    
    
    # FILTERS
    COMPETITION_URL += f'/code?competitionId={competition_id}'
    
    if SORT_BY == 'public score':
        COMPETITION_URL += '&sortBy=scoreDescending'
    elif SORT_BY == 'vote count':
        COMPETITION_URL += '&sortBy=voteCount'
    else:
        COMPETITION_URL += '&sortBy=commentCount'
        
    if PYTHON_ONLY: COMPETITION_URL += '&language=Python'
    if excludeNonAccessedDatasources: COMPETITION_URL += '&excludeNonAccessedDatasources=true'
    

    # Load the webpage
    driver.get(COMPETITION_URL)
    # # Wait for some time to allow dynamic content to load (you can adjust the time accordingly)
    # time.sleep(2)
    

    notebook_links = []
    url_count = 0
    MAX_NOTEBOOKS = NOTEBOOKS_AMOUNT
    
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@id="site-content"]')))
    element = driver.find_element(By.XPATH, '//*[@id="site-content"]')
    for i in range(MAX_NOTEBOOKS//15): 
        driver.execute_script("arguments[0].scrollBy(0, 50000);", element)
        time.sleep(1.5)
    
    # Find all list items within the object list
    WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/code/') and contains(@href, '/comments')]")))
    list_items = driver.find_elements(By.XPATH, "//a[contains(@href, '/code/') and contains(@href, '/comments')]")
    while (url_count < MAX_NOTEBOOKS):
        notebook_links.append(list_items[url_count].get_attribute('href')[:-9])
        url_count += 1
            

        
    print('LINKS DONE,  Time = ', time.time() - start_time)
        
    
    # -------------------------------------------------------------------------------------------------------------------------------------------------------
    
    url_count = 0
    for NOTEBOOK_URL in notebook_links:
        url_count += 1
        print(f'PARSING INFO FOR NOTEBOOK № {url_count}/{MAX_NOTEBOOKS},  Time = ', time.time() - start_time)
        
        # Load the webpage
        driver.get(NOTEBOOK_URL)
        # # Wait for some time to allow dynamic content to load (you can adjust the time accordingly)
        # time.sleep(2)

        # NOTEBOOK NAME
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//*[span[contains(text(), 'Python')]]")))
        text = driver.find_element(By.XPATH, "//*[span[contains(text(), 'Python')]]").text     # getting element above the element via *[]
        index = text.find('\n')
        notebook_name = text[:index]

        # UPDATE LAST TIME
        update_date = driver.find_element(By.XPATH, "//span[contains(@aria-label, 'ago')]").get_attribute('aria-label')[:-4]
        if update_date == 'a day': update_date = '1 day'
        if update_date == 'a month': update_date = '1 month'
        if update_date == 'a year': update_date = '1 year'

        # UPVOTES
        upvotes_amount = int(driver.find_element(By.XPATH, ".//button[contains(@aria-label, 'votes')]").text)

        # MEDAL
        try:
            medal = driver.find_element(By.XPATH, "//img[contains(@src, '/static/images/medals/notebooks/') and contains(@src, '.png')]").get_attribute('alt')[:-6]
        except NoSuchElementException:
            medal = 'None'

        # PUBLIC SCORE
        try:
            element = driver.find_element(By.XPATH, f"//*[text()='Public Score']") 
            parent = element.find_element(By.XPATH, "..")
            public_score = float(parent.find_element(By.TAG_NAME, "p").text)
        except NoSuchElementException:
            public_score = 'None'

        # PRIVATE SCORE
        try:
            element = driver.find_element(By.XPATH, f"//*[text()='Private Score']") 
            parent = element.find_element(By.XPATH, "..")
            private_score = float(parent.find_element(By.TAG_NAME, "p").text)
        except NoSuchElementException:
            private_score = 'None'

        # RUN TIME
        try:
            element = driver.find_element(By.XPATH, f"//*[text()='Run']") 
            parent = element.find_element(By.XPATH, "..")
            run_time_info = parent.find_element(By.TAG_NAME, "p").text
        except NoSuchElementException:
            run_time_info = 'None'

        # VIEWS
        text = driver.find_element(By.XPATH, f"//*[text()='views']").text
        views_amount = int(re.search(r'\b(\d+\s*)+ VIEWS$', text).group(0).replace(' VIEWS', '').replace(' ', ''))
    
        # -------------------------------------------------------------------------------------------------------------------------------------------------------
        
        time.sleep(0.5)
        
        # click ':'
        inner_html_content = "more_vert"
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(., '{inner_html_content}')]")))
        download_button = driver.find_element(By.XPATH, f"//*[contains(., '{inner_html_content}')]")   # specifying by 'button name' -> since CSS selector changes every time
        download_button.click()

        # click 'download'
        innter_html_content = "Download code"
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, f"//*[contains(., '{inner_html_content}')]")))
        download_button = driver.find_element(By.XPATH, f"//*[contains(., '{inner_html_content}')]")   # specifying by 'button name' -> since CSS selector changes every time
        download_button.click()
        
        # return logs
        logs = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

        for log in logs:
            if log['name'].startswith('https://www.kaggleusercontent.com/kf/'):
                kernel_link = log['name']
                break
                
        kernel_id = re.search(r'/(\d+)/', kernel_link).group(1)
        
        # -------------------------------------------------------------------------------------------------------------------------------------------------------
        
        url = NOTEBOOK_URL + "/input"
        input_datasources = []

        # Load the webpage
        driver.get(url)
        # # Wait for some time to allow dynamic content to load (you can adjust the time accordingly)
        # time.sleep(2)
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//p[text()='Data Sources']")))

        # Find all list items within the object list [using 'child element' Data Sources -> to find parent element -> that containts list of objects that we need [ul class list, li class element]]
        list_of_elements = driver.find_element(By.XPATH, f"//p[text()='Data Sources']")
        parent_element = list_of_elements.find_element(By.XPATH, "../..")
        ul_element = parent_element.find_element(By.TAG_NAME, "ul")
        list_of_elements = ul_element.find_elements(By.TAG_NAME, "li") 
        for el in list_of_elements:
            input_datasources.append(el.text[12:])
        
        # -------------------------------------------------------------------------------------------------------------------------------------------------------
        
        # URL of the Jupyter notebook
        kernel_link = f'https://www.kaggle.com/kernels/scriptcontent/{kernel_id}/download'

        # Download the notebook
        response = requests.get(kernel_link)
        notebook_content = response.content

        # Parse the notebook content with nbformat
        notebook = nbformat.reads(notebook_content, as_version=4)

        # Extract text from the notebook cells
        all_text = ""
        code_text = ""
        markdown_text = ""
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                # Include code cell content
                all_text += cell.source + '\n'
                code_text += cell.source + '\n'
            elif cell.cell_type == 'markdown':
                # Include markdown cell content
                all_text += cell.source + '\n'
                markdown_text += cell.source + '\n'
        
        # Forming list of Python libraries
        lines_of_code = list(filter(bool, code_text.split('\n')))
        python_libraries = []
        for line in lines_of_code:
            if line.startswith('import') or line.startswith('from'):
                python_libraries.append(line.split(' ')[1])
        python_libraries = list(OrderedDict.fromkeys(python_libraries))
        
        # -------------------------------------------------------------------------------------------------------------------------------------------------------
        
        df.loc[len(df.index)] = [notebook_name, NOTEBOOK_URL, public_score, private_score, medal, upvotes_amount, views_amount, run_time_info, update_date, all_text, code_text, markdown_text, input_datasources, python_libraries]
        
    # -------------------------------------------------------------------------------------------------------------------------------------------------------
    driver.quit()
    end_time = time.time()
    print("Elapsed time:", end_time - start_time, "seconds")
        
    return df