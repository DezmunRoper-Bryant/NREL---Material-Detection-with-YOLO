# Selenium can be used to automate the interaction with a web page
# Selenium pretends to be a real user anc can click on things and more

# Original Image scraping script

from selenium import webdriver
from selenium.webdriver.common.by import By
from opencv_functions import *
import requests
import io
from PIL import Image
import time

dataset_pixel_count = 300

PATH = "C:/Users/dezmu/OneDrive/Desktop/Web Scraping Images/chromedriver.exe"

service = webdriver.ChromeService(executable_path = PATH)
wd = webdriver.Chrome(service=service)

def get_images_from_google(wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

    url = "https://www.google.com/search?sca_esv=572573644&q=plastic+cup+images&tbm=isch&source=lnms&sa=X&sqi=2&ved=2ahUKEwiokvPg3e6BAxVVVTUKHZvsDc4Q0pQJegQIDRAB&biw=1707&bih=803&dpr=1.5"
    wd.get(url)

    image_urls = set()
    # skips = 0
    useful_images_count = 0  # Counter for useful images

    # while len(image_urls) + skips < max_images:
    while len(image_urls) < max_images:
        scroll_down(wd)

        thumbnails = wd.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")

        # for thumbnail in thumbnails[len(image_urls) + skips:max_images]:
        for thumbnail in thumbnails[len(image_urls):max_images]:
            try:
                wd.execute_script("arguments[0].click();", thumbnail)
                time.sleep(delay)
            except Exception as e:
                print(f"Error clicking image: {e}")
                continue

            images = wd.find_elements(By.CLASS_NAME, "Q4LuWd")
            for image in images:
                image_url = image.get_attribute('src')
                if image_url and image_url.startswith('http'):
                    if image_url not in image_urls: # If the current picture is not already in the set of images
                        image_urls.add(image_url)
                        useful_images_count += 1  # Increment the counter
                        print(f"Found {useful_images_count} out of {max_images}")
                        if len(image_urls) >= max_images:
                            break  # Exit the loop when max_images is reached
                else:
                    data_src = image.get_attribute('data-src')
                    if data_src and data_src.startswith('http'):
                        if data_src not in image_urls:
                            image_urls.add(data_src)
                            useful_images_count += 1  # Increment the counter
                            print(f"Found {useful_images_count} out of {max_images}")
                            if len(image_urls) >= max_images:
                                break  # Exit the loop when max_images is reached

    return image_urls



def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content

        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)


        file_path = download_path + file_name




        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print("Success")
    except Exception as e:
        print('FAILED -', e)

# def image_scraping(url, wd, delay, max_images):
#     urls = get_images_from_google(url, wd, delay, max_images)
#     for i, url in enumerate(urls):
#         download_image("C:/Users/dezmu/OneDrive/Desktop/Web Scraping Images/imgs", url, str(i) + ".jpg")
#         wd.quit()

urls = get_images_from_google(wd, 0.1, 1)

for i, url in enumerate(urls):
    download_image("C:/Users/dezmu/OneDrive/Desktop/Web Scraping Images/imgs", url, str(i) + ".jpg")
    
wd.quit()


