
---

# Pinterest Automation Script Guide

This guide will assist you in setting up and running a Pinterest automation script designed to scrape and post images on multiple Pinterest accounts.

## Prerequisites
Before starting, ensure the following are installed:
- Python (3.6 or later)
- Google Chrome browser
- ChromeDriver (compatible with your Chrome version)

## Installation

### 1. Clone the Repository OR just downlaod it 


### 2. Navigate to the Project Directory
Change to the project directory:
```
cd [Project Directory Name]
```
### 3. Install Required Python Libraries

Install the required Python packages:
```
pip install -r requirements.txt
```

## Configuration

### 1. Set Up Account Information
Edit the script to include your Pinterest account credentials and usernames you wish to scrape images from. Update the `ACCOUNTS`, `USERNAME0`, `USERNAME1`, and `USERNAME2` variables accordingly.

### 2. Configure Image Folders
Ensure the image folders (`images`, `images2`, `images3`) are correctly set up in the specified directory as per the script configuration.

### 3. Download and Specify ChromeDriver Path
Download the ChromeDriver executable compatible with your Chrome version from the [ChromeDriver website](https://sites.google.com/chromium.org/driver/). Update the `chromedriver.exe` path in the script if necessary.

###  IF YOU WANT DOWNLOAD THE CHROME DRIVER THAT IS IN THE SCRIPT IT IS DIRECTLY FROM THE [ChromeDriver website](https://sites.google.com/chromium.org/driver/)

## Running the Script

### 1. Execute the Script
Run the script using Python:
```
python main.py
```

## Additional Notes

- The script automatically scrapes images from specified Pinterest users and posts them to configured accounts.
- The script includes features like downloading images, Posting the images for you, Then after the images are downloaded they'll be deleted from your computer. 
- Modify and use this script responsibly.
---
