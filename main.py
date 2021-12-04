from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from PIL import Image
import pyautogui
from io import BytesIO
import time, os, random

pyautogui.MINIMUM_DURATION = 0
BROWSER_MENU_HEIGHT = 170
THRESHOLD = 100

os.makedirs('snaps', exist_ok=True)

s = Service('/Users/brad/Development/bdf_code/geetest-slider-captcha-cracker/chromedriver')
driver = webdriver.Chrome(service=s)

driver.get('https://www.geetest.com/en/demo')
driver.implicitly_wait(3)
driver.set_window_position(0, 0, windowHandle='current')

driver.find_element(By.CSS_SELECTOR, 'div[class="tab-item tab-item-1"]').click()
driver.implicitly_wait(3)

time.sleep(1)

# You can click [radar_btn] using Selenium, but using pyautogui is way safer
radar_btn = driver.find_element(By.CSS_SELECTOR, 'div[class="geetest_radar_btn"]')
pyautogui.moveTo(radar_btn.location['x'] + 50, radar_btn.location['y'] + BROWSER_MENU_HEIGHT, duration=2, tween=pyautogui.easeInOutElastic)
pyautogui.click(duration=0.1)

for _ in range(10):
    pyautogui.scroll(-10)
time.sleep(1)

# Get images
img_el = driver.find_element(By.CSS_SELECTOR, 'canvas[class="geetest_canvas_slice geetest_absolute"]')

byte = img_el.screenshot_as_png
puzzle_img = Image.open(BytesIO(byte))
puzzle_img.save(os.path.join('snaps', f'snap_{time.time()}.png'))

driver.execute_script(
    '''var x = document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0];
    x.style.display = 'block';
    x.style.opacity = 1'''
)

time.sleep(0.5)
byte = img_el.screenshot_as_png
complete_img = Image.open(BytesIO(byte))
complete_img.save(os.path.join('snaps', f'snap_{time.time()}.png'))

# Get diffenrence between puzzle and complete images and get distance between different pixels
def get_distance(img1, img2):
    for x in range(60, img1.size[0]):
        for y in range(img1.size[1]):
            rgb1 = img1.getpixel((x, y))
            rgb2 = img2.getpixel((x, y))

            diff_r = abs(rgb1[0] - rgb2[0])
            diff_g = abs(rgb1[1] - rgb2[1])
            diff_b = abs(rgb1[2] - rgb2[2])

            if diff_r > THRESHOLD or diff_g > THRESHOLD or diff_b > THRESHOLD:
                return x

distance = get_distance(puzzle_img, complete_img) - 7 # some calibration needed
print(distance)

# Move slide button
slider_button = driver.find_element(By.CSS_SELECTOR, 'div[class="geetest_slider_button"]')
scroll = driver.execute_script('return window.scrollY;') # get scroll positon

pyautogui.moveTo(slider_button.location['x'] + 10, slider_button.location['y'] - scroll + BROWSER_MENU_HEIGHT, duration=0.2, tween=pyautogui.easeInOutElastic)
pyautogui.mouseDown()

current_x = 0

while True:
    dx = random.randint(50, 100)
    dy = random.randint(-8, 8)
    print(dx, dy)
    pyautogui.moveRel(xOffset=dx, yOffset=dy, duration=random.randint(50, 100) / 100, tween=pyautogui.easeInOutSine)

    current_x += dx

    if current_x >= distance:
        dx = distance - current_x
        dy = random.randint(-8, 8)
        print(dx, dy)
        pyautogui.moveRel(xOffset=dx, yOffset=dy, duration=0.25, tween=pyautogui.easeInOutSine)
        break

pyautogui.mouseUp()
