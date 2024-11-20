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
        "10f671ea4c8325e4f6286e26e9565051a92ae0db8377d06b0f4d2b4d3babf145",
    ),
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/chrome-win/chrome.zip.002",
        "9045148b91282238c7086489c79f7acd88d8ec6f6fa448015560bf38c7a6a041",
    ),
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/chrome-win/chrome.zip.003",
        "2d58643f6b13d1ef88f8caaf860f833e6680d5a933e2d5a345b3396e2d547b7d",
    ),
    (
        "https://raw.githubusercontent.com/mike2367/selenium-up/refs/heads/browser-drivers/chrome-win/chrome.zip.004",
        "da16163d9520fe8bf9db83ef729bee9b01255b5260d89a841a4a261368c87c13",
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
            from settings import CHROMIUM, FIREFOX

            return CHROMIUM, FIREFOX
        except ImportError as e:
            print("Error importing settings:", e)
    print("Settings file not found or incomplete. Please enter extraction paths.")
    chromium_path = (
        input("Enter path for Chrome extraction (default src/main/resources/chrome): ") or "src/main/resources/chrome/"
    )
    firefox_path = (
        input("Enter path for Firefox extraction (default src/main/resources/firefox): ")
        or "src/main/resources/firefox"
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
