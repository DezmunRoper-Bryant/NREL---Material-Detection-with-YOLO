# Image Scraping script used to search images from Google and download them in a square format

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


class URL:
    all_url = []

    def __init__(self, folder, url):
        self.url = url
        self.folder = folder

        URL.all_url.append(self)

# URL objects created so that we can run through the urls and download images
url0 = URL("Red Plastic", "https://www.google.com/search?q=red+plastic+cup&tbm=isch&ved=2ahUKEwjhlcOFnf6BAxUFIWIAHftqCwIQ2-cCegQIABAA&oq=red+plastic+cup&gs_lcp=CgNpbWcQAzIHCAAQigUQQzIHCAAQigUQQzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEOgoIABCKBRCxAxBDOggIABCABBCxAzoGCAAQBRAeUJIIWPg2YI84aAVwAHgAgAFBiAHpB5IBAjE3mAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=hhcvZeG6AYXCiLMP-9WtEA&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080")
url1 = URL("Blue Plastic", "https://www.google.com/search?q=blue+plastic+cup&tbm=isch&ved=2ahUKEwiT9aHJnf6BAxUWGmIAHW67DgEQ2-cCegQIABAA&oq=blue+plastic+cup&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAUQHjIGCAAQBRAeMgYIABAFEB46BwgAEIoFEENQwgZY8wpggg1oAHAAeACAAUKIAdsCkgEBNpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=FBgvZZObBZa0iLMP7va6CA&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080")
url2 = URL("Clear Plastic", "https://www.google.com/search?q=clear+plastic+cup&tbm=isch&ved=2ahUKEwiLz7Lanf6BAxV4AWIAHczWDOAQ2-cCegQIABAA&oq=clear+plastic+cup&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgAEIoFEEM6BggAEAUQHjoGCAAQCBAeOgYIABAHEB5QgAdY4g5ghxBoAHAAeACAAaMBiAH-A5IBAzYuMZgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=OBgvZYtT-IKIsw_MrbOADg&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080")
url3 = URL("Base Plastic", "https://www.google.com/search?q=plastic+cup&tbm=isch&ved=2ahUKEwiS4oHvnf6BAxX_AWIAHYXIB1oQ2-cCegQIABAA&oq=plastic+cup&gs_lcp=CgNpbWcQAzIKCAAQigUQsQMQQzIHCAAQigUQQzIFCAAQgAQyBQgAEIAEMgcIABCKBRBDMgcIABCKBRBDMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABFDpFVjpFWDRF2gBcAB4AIABRYgBfpIBATKYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=YxgvZdKkD_-DiLMPhZGf0AU&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080")
url4 = URL("Base Styrofoam", "https://www.google.com/search?q=styrofoam+cup&tbm=isch&ved=2ahUKEwjEipT3nf6BAxWdF2IAHWXLA20Q2-cCegQIABAA&oq=sty&gs_lcp=CgNpbWcQARgBMgoIABCKBRCxAxBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDOgUIABCABDoNCAAQigUQsQMQgwEQQzoICAAQgAQQsQNQmhxYrkFg6FRoBnAAeACAAUmIAfICkgEBNpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=dBgvZcSAFJ2viLMP5ZaP6AY&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080")
url5 = URL("Dunkin Styrofoam", "https://www.google.com/search?q=dunkin+donuts+styrofoam+cups&tbm=isch&ved=2ahUKEwiPuoWsnv6BAxXhB1kFHVUMBdkQ2-cCegQIABAA&oq=dunkin+&gs_lcp=CgNpbWcQARgAMgcIABCKBRBDMggIABCABBCxAzIHCAAQigUQQzIHCAAQigUQQzIHCAAQigUQQzIKCAAQigUQsQMQQzIKCAAQigUQsQMQQzIHCAAQigUQQzIICAAQgAQQsQMyBwgAEIoFEEM6BggAEAgQHjoFCAAQgARQ7gxY_yFg7S9oA3AAeACAAUuIAagFkgECMTGYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=4xgvZc-8DuGP5NoP1ZiUyA0&bih=963&biw=1903&rlz=1C1GCEA_enUS1080US1080&hl=en")
url6 = URL("Base Metal", "https://www.google.com/search?q=metal+cup&tbm=isch&ved=2ahUKEwj7soSTov6BAxXOK2IAHWgkAJMQ2-cCegQIABAA&oq=metal+cup&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6CggAEIoFELEDEEM6BwgAEIoFEEM6BggAEAcQHjoGCAAQCBAeUO0IWLcWYK8YaAFwAHgAgAFGiAHwA5IBATiYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=4BwvZfvCIM7XiLMP6MiAmAk&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080")
url7 = URL("Stainless Metal", "https://www.google.com/search?q=stainless+steel+cup&tbm=isch&ved=2ahUKEwiPkae7ov6BAxV-MmIAHUX8Am4Q2-cCegQIABAA&oq=stain&gs_lcp=CgNpbWcQARgAMgcIABCKBRBDMgcIABCKBRBDMgoIABCKBRCxAxBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMggIABCABBCxAzIICAAQgAQQsQMyCAgAEIAEELEDOgUIABCABDoICAAQsQMQgwE6DQgAEIoFELEDEIMBEENQohJY-Rdg8iNoAHAAeACAAUqIAf8CkgEBNpgBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=NB0vZY-nPP7kiLMPxfiL8AY&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080")
url8 = URL("Tumbler Metal", "https://www.google.com/search?q=metal+tumbler&tbm=isch&ved=2ahUKEwjkws3lov6BAxUbOFkFHS9hBq0Q2-cCegQIABAA&oq=metal+tumbler&gs_lcp=CgNpbWcQAzIFCAAQgAQyBwgAEIoFEEMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BAgAEB46BggAEAUQHlCsB1i7CGD0CWgAcAB4AIABQYgBrQGSAQEzmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=jR0vZaTIKpvw5NoPr8KZ6Ao&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080 ")
url9 = URL("Base Can", "https://www.google.com/search?q=soda+can&tbm=isch&ved=2ahUKEwjr0vf5nv6BAxXcJFkFHbHDDnQQ2-cCegQIABAA&oq=soda+can&gs_lcp=CgNpbWcQAzIHCAAQigUQQzIICAAQgAQQsQMyBwgAEIoFEEMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEUJcKWKILYJANaABwAHgAgAE7iAGhAZIBATOYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=hhkvZev3I9zJ5NoPsYe7oAc&bih=963&biw=1903&rlz=1C1GCEA_enUS1080US1080&hl=en")
url10 = URL("Pepsi Can", "https://www.google.com/search?q=pepsi+can&tbm=isch&ved=2ahUKEwiK9eyGn_6BAxVANlkFHUg1Dx8Q2-cCegQIABAA&oq=pepsi&gs_lcp=CgNpbWcQARgAMgoIABCKBRCxAxBDMgoIABCKBRCxAxBDMgoIABCKBRCxAxBDMg0IABCKBRCxAxCDARBDMgcIABCKBRBDMggIABCABBCxAzIHCAAQigUQQzIHCAAQigUQQzIICAAQgAQQsQMyBwgAEIoFEEM6BQgAEIAEOgkIABAYEIAEEApQxAdYyhFg5h5oAXAAeACAAUyIAbcDkgEBN5gBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=oRkvZcqgKcDs5NoPyOq8-AE&bih=963&biw=1903&rlz=1C1GCEA_enUS1080US1080&hl=en")
url11 = URL("Dr Pepper Can", "https://www.google.com/search?q=dr+pepper+can&tbm=isch&ved=2ahUKEwjG5MOLn_6BAxVUIWIAHfFdAI8Q2-cCegQIABAA&oq=dr+pepper+can&gs_lcp=CgNpbWcQAzIICAAQgAQQsQMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6CggAEIoFELEDEEM6DQgAEIoFELEDEIMBEEM6BwgAEIoFEEM6BggAEAcQHlC2BljjGWD_HGgAcAB4AIABbIgBiwaSAQQxMC4xmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=qxkvZYbjHdTCiLMP8buB-Ag&bih=963&biw=1903&rlz=1C1GCEA_enUS1080US1080&hl=en")
url12 = URL("Base Bottle", "https://www.google.com/search?q=water+plastic+bottle&tbm=isch&ved=2ahUKEwjiofHcn_6BAxWaA2IAHVXdCTwQ2-cCegQIABAA&oq=water+plastic&gs_lcp=CgNpbWcQARgBMgcIABCKBRBDMgUIABCABDIFCAAQgAQyBwgAEIoFEEMyBwgAEIoFEEMyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgcIABCKBRBDUABYAGDxEmgAcAB4AIABP4gBP5IBATGYAQCqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=VhovZeKeBpqHiLMP1bqn4AM&bih=963&biw=1903&rlz=1C1GCEA_enUS1080US1080&hl=en")
url13 = URL("Dasani Bottle", "https://www.google.com/search?q=dasani+water+bottle&tbm=isch&ved=2ahUKEwjojcLgn_6BAxXACFkFHYjqDDgQ2-cCegQIABAA&oq=da&gs_lcp=CgNpbWcQARgAMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDMgcIABCKBRBDOgUIABCABDoICAAQgAQQsQNQrAtYiQ1gzRtoAHAAeACAAUWIAcYBkgEBM5gBAKABAaoBC2d3cy13aXotaW1nwAEB&sclient=img&ei=XRovZajrK8CR5NoPiNWzwAM&bih=963&biw=1903&rlz=1C1GCEA_enUS1080US1080&hl=en")
url14 = URL("Aquafina Bottle", "https://www.google.com/search?q=aquafine+water+bottle&tbm=isch&ved=2ahUKEwjg4smBoP6BAxUuC1kFHUIVCzMQ2-cCegQIABAA&oq=aquafine+water+bottle&gs_lcp=CgNpbWcQAzIFCAAQgAQyCQgAEBgQgAQQCjoHCAAQigUQQzoGCAAQBxAeUNUFWLYUYPQWaANwAHgAgAFJiAHrBJIBAjEwmAEAoAEBqgELZ3dzLXdpei1pbWfAAQE&sclient=img&ei=oxovZaCFA66W5NoPwqqsmAM&bih=963&biw=1903&rlz=1C1GCEA_enUS1080US1080&hl=en")
url15 = URL("Base Paper", "https://www.google.com/search?sca_esv=574277537&rlz=1C1GCEA_enUS1080US1080&q=paper+cup&tbm=isch&source=lnms&sa=X&ved=2ahUKEwjv1NzDof6BAxWeEVkFHT1TDNYQ0pQJegQIDBAB&biw=1920&bih=963&dpr=1")
url16 = URL("Coffee Paper", "https://www.google.com/search?q=disposable+coffee+cups&tbm=isch&ved=2ahUKEwjI-tzxof6BAxUiNlkFHQWAAbAQ2-cCegQIABAA&oq=disposable+coffee+cups&gs_lcp=CgNpbWcQAzIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQ6BwgAEIoFEEM6BggAEAcQHjoGCAAQCBAeUO8HWM0QYPURaABwAHgAgAFdiAGjBJIBATiYAQCgAQGqAQtnd3Mtd2l6LWltZ8ABAQ&sclient=img&ei=mhwvZcjFKaLs5NoPhYCGgAs&bih=963&biw=1920&rlz=1C1GCEA_enUS1080US1080")


# Create a directory to store the downloaded images
download_directory = "C:/Users/dezmu/OneDrive/Desktop/Web Scraping Images/"

# Loop through each URL and download images into a separate folder for each URL
for url in URL.all_url:
    # folder_name = f"folder_{i}"  # Create a folder name based on the index
    folder_name = url.folder
    folder_path = os.path.join(download_directory, folder_name)

    # Create a folder for the current URL if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Initialize a new WebDriver instance for each URL
    service = webdriver.ChromeService(executable_path=PATH)
    wd = webdriver.Chrome(service=service)

    # Get the image URLs for the current URL
    image_urls = get_images_from_google(url.url, wd, 0.1, 80)

    # Download images into the corresponding folder
    for j, image_url in enumerate(image_urls):
        file_name = f"{folder_name}_{j}.jpg"
        download_image(download_directory, folder_name, image_url, file_name)

    wd.quit()

wd.quit()


