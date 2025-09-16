import pyautogui as pag
import time
import requests
import os

time.sleep(40)

# Define actions with coordinates and duration
actions = [
    (516, 405, 4),  # install (wait 15sec)
    (50, 100, 1),   # tic launch avica
    (496, 438, 4),  # Later Update
    (249, 203, 4),  # allow rdp
    (249, 203, 4),  # allow rdp again
    (249, 203, 4),  # allow rdp again
    (249, 203, 4),  # allow rdp again
    (447, 286, 4),  # ss id & upload
]

# Give time to focus on the target application
time.sleep(10)

# Credentials and upload information
img_filename = 'NewAvicaRemoteID.png'

# Upload to Gofile.io
def upload_image_to_gofile(img_filename):
    url = 'https://store1.gofile.io/uploadFile'
    try:
        with open(img_filename, 'rb') as img_file:
            files = {'file': img_file}
            response = requests.post(url, files=files)
            response.raise_for_status()
            result = response.json()

        if result['status'] == 'ok':
            download_page = result['data']['downloadPage']
            with open('show.bat', 'a') as bat_file:
                bat_file.write(f'\necho Avica Remote ID : {download_page}')
            return download_page
        else:
            print("Upload error:", result.get('status'))
            return None
    except Exception as e:
        print(f"Failed to upload image: {e}")
        return None

# Iterate through actions
for x, y, duration in actions:
    pag.click(x, y, duration=duration)

    if (x, y) == (249, 203):  # Attempt to activate "Allow remote access"
        time.sleep(1)
        pag.click(x, y, duration=duration)

    if (x, y) == (447, 286):  # Launch avica and upload screenshot
        os.system('"C:\\Program Files (x86)\\Avica\\Avica.exe"')
        time.sleep(5)
        pag.click(249, 203, duration=4)  # Re-click Allow
        time.sleep(5)

        # 🔍 Find the element on screen before screenshot
        try:
            element_location = pag.locateCenterOnScreen('download.jpg', confidence=0.8)  
            if element_location:
                print(f"Found element at: {element_location}")
                pag.click(element_location)  # Tap on the element
                time.sleep(5)  # small delay
            else:
                print("Element not found on screen!")
        except Exception as e:
            print(f"Error finding element: {e}")

        # 📸 Take screenshot after tapping
        pag.screenshot().save(img_filename)
        gofile_link = upload_image_to_gofile(img_filename)

        if gofile_link:
            print(f"Image uploaded successfully. Link: {gofile_link}")
        else:
            print("Failed to upload the image.")

time.sleep(10)
print('Done!')
