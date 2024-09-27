import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options


# Function to initialize the WebDriver
# def initialize_driver():
#     options = webdriver.ChromeOptions()
#     # Set headless to False to see the browser
#     # options.add_argument("--headless")  # Uncomment this line for headless mode
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
#     driver = webdriver.Chrome(
#         service=Service(
#             ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
#         ),
#         options=options,
#     )
#     return driver

def initialize_driver():
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--headless")

    return webdriver.Chrome(
            service=Service(
                ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            options=options,
        )

# Function to perform a Google search and retrieve results
def google_search(query):
    driver = initialize_driver()
    driver.get("https://www.google.com")
    
    # Wait for the cookies consent popup and accept it if present
    try:
        # Wait for the consent popup and click the accept button
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//div[text()="Accept all"]'))
        ).click()
    except Exception as e:
        print("No cookies popup found or unable to accept cookies:", e)

    # Wait for the search box to be present and clickable
    try:
        search_box = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.NAME, "q"))
        )
        search_box.send_keys(f'"{query}"')
        search_box.submit()
        
        # Wait for the results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.g'))
        )

        # Extract the top 10 results
        results = driver.find_elements(By.CSS_SELECTOR, 'div.g')[:10]
        
        list_data = []
        
        for result in results:
            # Title of search
            try:
                title = result.find_element(By.TAG_NAME, 'h3').text
            except Exception as e:
                title = ''
            
            # URL of search
            try:
                link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
            except Exception as e:
                link = ''
            
            # Snippet -> short display 
            snippet = "No snippet available"
            # snippet_elements = result.find_elements(By.CSS_SELECTOR, 'div.VwiC3b.yXK7lf.lVm3ye')
            snippet_elements = result.find_elements(By.CSS_SELECTOR, 'div[style*="-webkit-line-clamp:2"]')
            if snippet_elements:
                snippet = snippet_elements[0].text
            
            try:
                # Open the link in a new tab and get the full page content
                driver.execute_script("window.open(arguments[0]);", link)
                driver.switch_to.window(driver.window_handles[1])  # Switch to the new tab

                # Wait for the page to fully load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'body'))
                )

                # Get the full page content
                full_page_content = driver.find_element(By.TAG_NAME, 'body').text

                # Close the new tab and switch back to the original tab
                driver.close()
                driver.switch_to.window(driver.window_handles[0])  # Switch back to the original tab
            except Exception as e:
                full_page_content = ''
            

            list_data.append({
                "title": title,
                "url": link,
                "snippet": snippet,
                "content": full_page_content
            })

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()
        
    return list_data
