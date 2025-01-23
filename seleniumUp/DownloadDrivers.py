import os
import urllib.request
import zipfile
import shutil
import time
import hashlib

# Define URLs and expected SHA256 checksums
chrome_files_info = [
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/chrome-win/chrome.zip.001",
        "10F671EA4C8325E4F6286E26E9565051A92AE0DB8377D06B0F4D2B4D3BABF145",
    ),
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/chrome-win/chrome.zip.002",
        "662956F222514CFFBA3EFB9405EABEB3F2921EF61F597B97A2A73FDB965FA976",
    ),
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/chrome-win/chrome.zip.003",
        "5D3412FFAB59905918150CD0595AB1EE9E050C570F143F34E17ABCA7819A3707",
    ),
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/chrome-win/chrome.zip.004",
        "D13D234A8F4057BCA52644FADE142144E4FCB5CB8EDA917341C29069CB7D81B5",
    ),
]

firefox_files_info = [
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/firefox-win/firefox.zip.001",
        "eada3b238a9940a502e15c8888991f9810f91a644296f5c8be58ceb0a9954096",
    ),
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/firefox-win/firefox.zip.002",
        "273578a4481f6d2979a46d0ef63457c9a951b980c435320ac535a15bd97b8123",
    ),
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/firefox-win/firefox.zip.003",
        "3365d3ea171e20e32016da8f3e52c2004d2315da1cab06a4bb31c693d5dd93f7",
    ),
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/firefox-win/firefox.zip.004",
        "56c782a7d28d239dc307b64ca09951aa58fac6bc4b53ac1d64298f70ba07f7b3",
    ),
]


# Function to calculate SHA256 checksum
def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


# Function to download files with retry logic
def download_files(files_info, download_path, retries=3, delay=2):
    os.makedirs(download_path, exist_ok=True)
    file_paths = []
    for url, expected_sha256 in files_info:
        file_name = os.path.join(download_path, os.path.basename(url))
        if os.path.exists(file_name) and calculate_sha256(file_name) == expected_sha256:
            print(
                f"File {file_name} already exists and is complete. Skipping download."
            )
            file_paths.append(file_name)
            continue
        success = False
        for attempt in range(retries):
            try:
                print(f"Downloading {url} to {file_name}... (Attempt {attempt + 1})")
                urllib.request.urlretrieve(url, file_name)
                if calculate_sha256(file_name) == expected_sha256:
                    file_paths.append(file_name)
                    success = True
                    break
                else:
                    print(f"File {file_name} is incomplete. Retrying...")
            except Exception as e:
                print(f"Failed to download {url}: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
        if not success:
            print(f"Failed to download {url} after {retries} attempts.")
    return file_paths


# Function to combine split zip files
def combine_files(file_paths, combined_file_path):
    with open(combined_file_path, "wb") as combined_file:
        for file_path in file_paths:
            with open(file_path, "rb") as part_file:
                shutil.copyfileobj(part_file, combined_file)


# Function to extract files
def extract_file(file_path, extract_path):
    os.makedirs(extract_path, exist_ok=True)
    print(f"Extracting {file_path} to {extract_path}...")
    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(extract_path)
    os.remove(file_path)


# Function to get extraction paths
def get_extraction_paths():
    if os.path.exists("settings.py"):
        try:
            from seleniumUp.settings import CHROMIUM, FIREFOX

            return CHROMIUM, FIREFOX
        except ImportError as e:
            print("Error importing settings:", e)
    print("Settings file not found or incomplete. Please enter extraction paths.")
    chromium_path = (
        input("Enter path for Chrome extraction (default resources/chrome/): ") or "resources/chrome/"
    )
    firefox_path = (
        input("Enter path for Firefox extraction (default resources/firefox/): ")
        or "resources/firefox/"
    )
    return chromium_path, firefox_path


def main():
    chromium_path, firefox_path = get_extraction_paths()

    # Download and extract Chrome drivers
    chrome_download_path = "./chrome_downloads"
    chrome_files = download_files(chrome_files_info, chrome_download_path)
    if len(chrome_files) == len(chrome_files_info):
        combined_chrome_file = os.path.join(chrome_download_path, "chrome_combined.zip")
        combine_files(chrome_files, combined_chrome_file)
        extract_file(combined_chrome_file, chromium_path)
        shutil.rmtree(chrome_download_path)
    else:
        print("Not all Chrome files were downloaded completely. Please retry.")

    # Download and extract Firefox drivers
    firefox_download_path = "./firefox_downloads"
    firefox_files = download_files(firefox_files_info, firefox_download_path)
    if len(firefox_files) == len(firefox_files_info):
        combined_firefox_file = os.path.join(
            firefox_download_path, "firefox_combined.zip"
        )
        combine_files(firefox_files, combined_firefox_file)
        extract_file(combined_firefox_file, firefox_path)
        shutil.rmtree(firefox_download_path)
    else:
        print("Not all Firefox files were downloaded completely. Please retry.")

    print("All drivers downloaded and extracted successfully.")


if __name__ == "__main__":
    main()
