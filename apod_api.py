'''
Library for interacting with NASA's Astronomy Picture of the Day API.
'''
import sys
from pathlib import Path
from datetime import date
from sys import argv
import image_lib
import os
import requests

NASA_API_KEY = 'byAB4j1YbHoJiYXa2mPtDjXYitr27pR2eDdIPf9r'  # follow instructions to get this
APOD_URL = "https://api.nasa.gov/planetary/apod"


def main():
    import sys
    num_params = len(sys.argv) - 1
    # apod_date = date.fromisoformat(argv[1])

    # import sys
    # sys.argv

    apod_info_dict = get_apod_info(apod_date)
    if apod_info_dict:
        apod_url = get_apod_image_url(apod_info_dict)

        apod_image_data = image_lib.download_image(apod_url)

        image_lib.save_image_file(apod_image_data, r'C:\temp\image.jpg')

    return


def get_apod_info(apod_date):
    """Gets information from the NASA API for the Astronomy 
    Picture of the Day (APOD) from a specified date.

    Args:
        apod_date (date): APOD date (Can also be a string formatted as YYYY-MM-DD)

    Returns:
        dict: Dictionary of APOD info, if successful. None if unsuccessful
    """
    # Setup request parameters 
    apod_params = {
        'api_key': NASA_API_KEY,
        'date': apod_date,
        'thumbs': True
    }

    # Send GET request to NASA API
    print(f'Getting {apod_date} APOD information from NASA...', end='')
    resp_msg = requests.get(APOD_URL, params=apod_params)

    # Check if the info was retrieved successfully
    if resp_msg.status_code == requests.codes.ok:

        print('success')
        # Convert the received info into a dictionary 
        apod_info_dict = resp_msg.json()
        return apod_info_dict
    
    else:
        print('failure')

        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')


def get_apod_image_url(apod_info_dict):
    """Gets the URL of the APOD image from the dictionary of APOD information.

    If the APOD is an image, gets the URL of the high definition image.
    If the APOD is a video, gets the URL of the video thumbnail.

    Args:
        apod_info_dict (dict): Dictionary of APOD info

    Returns:
        str: APOD image URL
    """
    if apod_info_dict['media_type'] == 'image':

        return apod_info_dict['hdurl']
        
    elif apod_info_dict['media_type'] == 'video':
        # Some video APODs do not have thumbnails, so this will sometimes fail
        return apod_info_dict['thumbnail_url']


def get_apod_date():
    """Gets the APOD date

    The APOD date is taken from the first command line parameter.
    Validates that the command line parameter specifies a valid APOD date.
    Prints an error message and exits script if the date is invalid.
    Uses today's date if no date is provided on the command line.

    Returns:
        date: APOD date
    """
    num_params = len(sys.argv) - 1
    if num_params >= 1:
        # Date parameter has been provided, so get it
        try:
            apod_date = date.fromisoformat(sys.argv[1])
            
            print(f'{apod_date} apod_date')

            



        except ValueError as err:
            print('Error: Invalid date format; ', err)

            sys.exit('Script execution aborted')

        # Validate that the date is within range

        MIN_APOD_DATE = date.fromisoformat("1995-06-16")  # Complete this
        print(MIN_APOD_DATE, "MIN_APOD_DATE")
        if apod_date < MIN_APOD_DATE:

            print('Error: Date too far in past; First APOD was on ,' ,MIN_APOD_DATE.isoformat())
            

            sys.exit("Script execution aborted")

        elif apod_date > date.today():
            print(f'Error: APOD date cannot be in the future')

            sys.exit('Script execution aborted')
    else:
        # No date parameter has been provided, so use today's date
        apod_date = date.today()  # Fill in here

    return apod_date


if __name__ == '__main__':

    # Build paths inside the project like this: BASE_DIR / 'subdir'.


    # import sqlite3
    # DB_PATH = os.path.join(IMAGES_PATH, "image_cache.db")
    # print(f"Image cache DB: {DB_PATH}")
    # if os.path.exists(DB_PATH):
    #     print("Image cache DB already exists.")
    # else:
    #     sqlite3.connect(DB_PATH)
    #     print("Image cache DB created.")




    main()
    # # test the apod date method
    # # apod_date = get_apod_date()
    # # print(apod_date)
    # print("Image cache directory: \image.jpg")
    # import sqlite3
    # sqlite3.connect("test.db")
    # print("Opened database successfully")
