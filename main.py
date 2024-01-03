import os
import time
import pickle
import random
import requests
from PIL import Image
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

COOKIES_FILE_PATH = 'pinterest_cookies.pkl'
USERNAME0 = []
USERNAME1 = []
USERNAME2 = []

MIN_FILE_SIZE = 20 * 1024  
ACCOUNTS = ["Instert 3 accounts here if you only have one account only input one email"],


MAX_POSTS_PER_ACCOUNT = 20
MIN_IMAGE_WIDTH = 200
MIN_IMAGE_HEIGHT = 300

IMAGES_FOLDER_BASE = r'Insert the path for image folder'
ACCOUNTS_IMAGE_FOLDERS = {
    0: os.path.join(IMAGES_FOLDER_BASE, 'images'),
    1: os.path.join(IMAGES_FOLDER_BASE, 'images2'),
    2: os.path.join(IMAGES_FOLDER_BASE, 'images3')
}

def download_image(url, account_index):
    folder = ACCOUNTS_IMAGE_FOLDERS[account_index]
    if not os.path.exists(folder):
        os.makedirs(folder)
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            filename = url.split('/')[-1].split('?')[0]
            file_path = os.path.join(folder, filename)
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
    except Exception as e:
        print(f"Error downloading {url}: {e}")

def scrape_images_from_user(usernames, account_index):
    driver = None
    try:
        IMAGES_FOLDER = ACCOUNTS_IMAGE_FOLDERS[account_index]
        service = Service(executable_path="chromedriver.exe")
        driver = webdriver.Chrome(service=service)

        image_count = 0
        for random_user in usernames:
            user_profile_url = f"https://www.pinterest.com/{random_user}/_created"
            print(f"Accessing {user_profile_url} for account index {account_index}")
            driver.get(user_profile_url)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "img"))
                )
                print("Page loaded successfully.")
            except Exception as wait_e:
                print(f"Error waiting for page to load for {user_profile_url}: {wait_e}")
                continue 

            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            images = soup.find_all('img', src=lambda x: x and "236x" in x)
            if not images:
                print(f"No images found on the page for {random_user}.")
                continue  
            for img in images:
                if image_count >= 50:
                    break
                large_img_src = img.get('src').replace("236x", "originals")
                print(f"Downloading image from {large_img_src}")
                download_image(large_img_src, account_index)
                image_count += 1

    except Exception as e:
        print(f"Error scraping images for account {account_index}: {e}")
    finally:
        if driver:
            print("Closing the browser.")
            driver.quit()

def post_images_to_pinterest(image_paths, driver):
    driver.get("https://www.pinterest.com/pin-creation-tool/")
    image_upload_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
    )

   
    image_paths_str = "\n".join(image_paths)
    image_upload_input.send_keys(image_paths_str)

   e
    time.sleep(20)  


    checkbox = driver.find_element(By.ID, "storyboard-drafts-sidebar-bulk-select-checkbox")
    checkbox.click()
    time.sleep(2)  


    publish_button = driver.find_element(By.XPATH, "//div[contains(@class, 'tBJ dyH iFc sAJ xnr tg7 H2s')]")
    publish_button.click()
    time.sleep(10)

def post_images_in_batches(image_folder, account_index, driver, max_batch_size=10):
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    print(f"Total images in folder for account {account_index}: {len(image_files)}")

    while image_files:
        batch = image_files[:max_batch_size]
        image_paths = [os.path.join(image_folder, image_name) for image_name in batch]
        image_files = image_files[max_batch_size:]

        if image_paths:
            print(f"Uploading batch of {len(image_paths)} images for account {account_index}")
            post_images_to_pinterest(image_paths, driver)
            for image_path in image_paths:
                os.remove(image_path)

        if image_files:
            print("Waiting before next batch...")
            time.sleep(10)

def login_and_save_cookies(driver, account_index, cookies_file_path):
    try:
        email, password = ACCOUNTS[account_index]
        driver.get("https://www.pinterest.com/login/")
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "email"))).send_keys(email)
        driver.find_element(By.ID, "password").send_keys(password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Log in')]"))).click()
        WebDriverWait(driver, 10).until(EC.url_to_be("https://www.pinterest.com/business/hub/"))
        time.sleep(5)
        cookies = driver.get_cookies()
        if cookies:
            pickle.dump(cookies, open(cookies_file_path, "wb"))
        else:
            print("No cookies to save.")
    except Exception as e:
        print(f"Error during login or saving cookies: {e}, Type: {type(e)}")
        with open(f"error_snapshot_{account_index}.html", "w", encoding='utf-8') as file:
            file.write(driver.page_source)
        driver.save_screenshot(f"error_snapshot_{account_index}.png")

def is_image_large_enough(image_path, min_width=200, min_height=300):
    with Image.open(image_path) as img:
        width, height = img.size
        return width > min_width and height > min_height

def process_account(account_index):
    driver = None
    try:
        print(f"Starting processing for account {account_index} with email: {ACCOUNTS[account_index][0]}")
        service = Service(executable_path="chromedriver.exe")
        chrome_options = Options()
        driver = webdriver.Chrome(service=service, options=chrome_options)

        images_folder = ACCOUNTS_IMAGE_FOLDERS[account_index]
        if not os.listdir(images_folder):  # Folder is empty
            print(f"Images folder for account {account_index} is empty. Starting image scraping.")
            usernames = globals()[f'USERNAME{account_index}']
            scrape_images_from_user(usernames, account_index)

        cookies_file_path = f'pinterest_cookies_{account_index}.pkl'
        if os.path.exists(cookies_file_path):
            driver.get("https://www.pinterest.com")
            cookies = pickle.load(open(cookies_file_path, "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()

            if not login_check(driver):
                login_and_save_cookies(driver, account_index, cookies_file_path)
        else:
            login_and_save_cookies(driver, account_index, cookies_file_path)

        post_images_in_batches(ACCOUNTS_IMAGE_FOLDERS[account_index], account_index, driver)

    except Exception as e:
        print(f"Error in processing account {account_index}: {e}")
    finally:
        if driver:
            driver.quit()

def login_check(driver):
   
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//div[text()='Home']")))
        return True
    except:
        return False

def main():
    for account_index in range(len(ACCOUNTS)):
        print(f"Starting processing for account {account_index}.")
        process_account(account_index)
        print(f"Finished processing for account {account_index}.")

    print("Processing completed for all accounts. Waiting 24 hours before next run.")
    time.sleep(86400)  # 86400 seconds = 24 hours

if __name__ == "__main__":
    main()
