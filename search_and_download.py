# 10/13/23 Image Scraping script used to search images from Google and download them in a square format

from selenium import webdriver
from selenium.webdriver.common.by import By
from opencv_functions import *
import requests
import io
import time
import os

dataset_pixel_count = 300

PATH = "C:/Users/dezmu/OneDrive/Desktop/Web Scraping Images/chromedriver.exe"

service = webdriver.ChromeService(executable_path=PATH)
wd = webdriver.Chrome(service=service)


def get_images_from_google(url, wd, delay, max_images):
    def scroll_down(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(delay)

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
                    if image_url not in image_urls:  # If the current picture is not already in the set of images
                        image_urls.add(image_url)
                        useful_images_count += 1  # Increment the counter
                        print(f"Found {useful_images_count} out of {max_images}")
                        if len(image_urls) >= max_images:
                            break  # Exit the loop when max_images is reached
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


def download_image(download_path, folder_name, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)

        # Load the image content into OpenCV
        image_cv = cv.imdecode(np.frombuffer(image_content, np.uint8), cv.IMREAD_COLOR)
        image_cv = pixel_adjust(image_cv, dataset_pixel_count)  # Resize the image

        folder_path = os.path.join(download_path, folder_name)  # Create the full path to the folder

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        file_path = os.path.join(folder_path, file_name)  # Create the full path to the image file

        cv.imwrite(file_path, image_cv)

        print("Success")
    except Exception as e:
        print('FAILED -', e)



# Define a list of URLs
urls = [
    "https://www.google.com/search?q=plastic+cup&tbm=isch&ved=2ahUKEwiS4oHvnf6BAxX_AWIAHYXIB1oQ2-cCegQIABAA&oq=plastic+cup&gs_lcp=CgNpbWcQAzIKCAAQigUQsQMQQzIHCAAQigUQQzIFCAAQgAQyBQgAEIAEMgcIABCKBRBDMgcIABCKBRBDMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABFDpFVjpFWDRF2gBcAB4AIABRYgBfpIBATKYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=YxgvZdKkD_-DiLMPhZGf0AU&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080",
    "https://www.google.com/search?q=blue+plastic+cup&tbm=isch&ved=2ahUKEwiT9aHJnf6BAxUWGmIAHW67DgEQ2-cCegQIABAA&oq=blue+plastic+cup&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB46BwgAEIoFEENQwgZY8wpggg1oAHAAeACAAUKIAdsCkgEBNpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=FBgvZZObBZa0iLMP7va6CA&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080"

    # Add your other URLs here
]

# Create a directory to store the downloaded images
download_directory = "C:/Users/dezmu/OneDrive/Desktop/Web Scraping Images/"

# Loop through each URL and download images into a separate folder for each URL
for i, url in enumerate(urls):
    folder_name = f"folder_{i}"  # Create a folder name based on the index
    folder_path = os.path.join(download_directory, folder_name)

    # Create a folder for the current URL if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Initialize a new WebDriver instance for each URL
    service = webdriver.ChromeService(executable_path=PATH)
    wd = webdriver.Chrome(service=service)

    # Get the image URLs for the current URL
    image_urls = get_images_from_google(url, wd, 0.1, 1)

    # Download images into the corresponding folder
    for j, image_url in enumerate(image_urls):
        file_name = f"image_{j}.jpg"
        download_image(download_directory, folder_name, image_url, file_name)

    wd.quit()

#
# url = "https://www.google.com/search?sca_esv=572573644&q=plastic+cup+images&tbm=isch&source=lnms&sa=X&sqi=2&ved=2ahUKEwiokvPg3e6BAxVVVTUKHZvsDc4Q0pQJegQIDRAB&biw=1707&bih=803&dpr=1.5"
#
# urls = get_images_from_google(url, wd, 0.1, 1)
# print(len(urls))
#
#
# for i, url in enumerate(urls):
#     download_image("C:/Users/dezmu/OneDrive/Desktop/Web Scraping Images/imgs", url, str(i) + ".jpg")

wd.quit()