#!/usr/bin/env python3
"""
ARGO Float Data Downloader
Downloads data from ftp.ifremer.fr/ifremer/argo with backup options
"""

import ftplib
import requests
import time
import random
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

class ArgoDownloader:
    def __init__(self, data_dir="C:/Users/Lenovo/Desktop/OceanResearch/data/raw"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.ftp_server = "ftp.ifremer.fr"
        self.ftp_path = "/ifremer/argo"
        
        self.backup_urls = [
            "https://data-argo.ifremer.fr/dac/bodc/6901930/profiles/D6901930_001.nc",
            "https://data-argo.ifremer.fr/dac/aoml/1900722/profiles/D1900722_001.nc",
            "https://data-argo.ifremer.fr/dac/coriolis/6901758/profiles/D6901758_001.nc",
            "https://data-argo.ifremer.fr/dac/aoml/5906300/profiles/D5906300_001.nc",
            "https://data-argo.ifremer.fr/dac/coriolis/6904112/profiles/D6904112_001.nc"
        ]
    
    def download_data(self, max_attempts=3):
        """Download ARGO float data"""
        print("ARGO Float Data Downloader")
        print("Server: ftp.ifremer.fr/ifremer/argo")
        print("=" * 50)
        
        downloaded_files = []
        
        # Try FTP first
        print("Connecting to FTP server...")
        ftp_files = self._try_ftp_download(max_attempts)
        downloaded_files.extend(ftp_files)
        
        # Use HTTP if FTP unavailable
        if not ftp_files:
            print("FTP server unavailable, using HTTP access...")
            http_files = self._download_via_http()
            downloaded_files.extend(http_files)
        
        return downloaded_files
    
    def _try_ftp_download(self, max_attempts):
        """Attempt FTP download with retry logic"""
        downloaded_files = []
        
        for attempt in range(max_attempts):
            try:
                if attempt > 0:
                    delay = min(2 ** attempt, 300)
                    jitter = random.uniform(0.5, 1.5)
                    actual_delay = delay * jitter
                    
                    print(f"Retrying in {actual_delay:.1f}s (attempt {attempt+1})")
                    time.sleep(actual_delay)
                
                ftp = ftplib.FTP()
                ftp.connect(self.ftp_server, timeout=30)
                ftp.login()
                
                print(f"Connected successfully (attempt {attempt + 1})")
                
                files = self._download_from_ftp(ftp, max_files=2)
                downloaded_files.extend(files)
                
                ftp.quit()
                
                if files:
                    print(f"Downloaded {len(files)} files via FTP")
                    break
                    
            except ftplib.error_temp as e:
                if "too many" in str(e).lower():
                    print(f"Server busy (attempt {attempt+1})")
                    if attempt == max_attempts - 1:
                        print("FTP server remains busy")
                    continue
                else:
                    print(f"FTP error: {e}")
                    break
                    
            except Exception as e:
                print(f"Connection failed: {e}")
                if attempt < 3:
                    continue
                else:
                    break
        
        return downloaded_files
    
    def _download_from_ftp(self, ftp, max_files=2):
        """Download files from FTP server"""
        files = []
        
        try:
            ftp.cwd(self.ftp_path)
            ftp.cwd("dac")
            
            dacs = ftp.nlst()[:3]
            
            for dac in dacs:
                if len(files) >= max_files:
                    break
                    
                try:
                    ftp.cwd(f"{self.ftp_path}/dac/{dac}")
                    floats = ftp.nlst()[:3]
                    
                    for float_dir in floats:
                        if len(files) >= max_files:
                            break
                            
                        try:
                            if float_dir.isdigit():
                                profiles_path = f"{self.ftp_path}/dac/{dac}/{float_dir}/profiles"
                                ftp.cwd(profiles_path)
                                
                                nc_files = [f for f in ftp.nlst() if f.endswith('.nc')][:1]
                                
                                if nc_files:
                                    filename = nc_files[0]
                                    local_path = self.data_dir / filename  # Use same naming as HTTP
                                    
                                    with open(local_path, 'wb') as f:
                                        ftp.retrbinary(f"RETR {filename}", f.write)
                                    
                                    files.append(local_path)
                                    print(f"Downloaded: {filename}")
                                    
                        except Exception:
                            continue
                            
                except Exception:
                    continue
        
        except Exception as e:
            print(f"FTP download error: {e}")
        
        return files
    
    def _download_via_http(self):
        """Download from HTTP sources"""
        downloaded_files = []
        
        def download_single(url, retry=False):
            try:
                response = requests.get(url, timeout=20)
                if response.status_code == 200:
                    filename = url.split('/')[-1]
                    local_path = self.data_dir / filename
                    
                    with open(local_path, 'wb') as f:
                        f.write(response.content)
                    
                    return local_path
                else:
                    print(f"HTTP error for {url}: Status {response.status_code}")
            except requests.exceptions.Timeout:
                print(f"Timeout for {url}")
                if not retry:
                    return download_single(url, retry=True)
            except requests.exceptions.RequestException as e:
                print(f"HTTP request failed for {url}: {e}")
            return None
        
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(download_single, url): url for url in self.backup_urls}
            
            for future in as_completed(futures, timeout=60):
                try:
                    result = future.result()
                    if result:
                        downloaded_files.append(result)
                        print(f"Downloaded: {result.name}")
                        
                        if len(downloaded_files) >= 2:
                            break
                            
                except Exception as e:
                    print(f"Future error for {futures[future]}: {e}")
                    continue
        
        return downloaded_files

def main():
    """Main execution function"""
    downloader = ArgoDownloader()
    
    files = downloader.download_data()
    
    print(f"\nResults:")
    print(f"Downloaded {len(files)} files")
    for f in files:
        size_kb = f.stat().st_size / 1024
        print(f"  {f.name} ({size_kb:.1f} KB)")
    
    if files:
        print("Data ready for processing")
    else:
        print("No files downloaded")
    
    return files

if __name__ == "__main__":
    main()