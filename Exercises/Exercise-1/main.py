"""
main
~~~~

Solutions to exercise 1, generally:


1. create the directory `downloads` if it doesn't exist
2. download the files one by one.
3. split out the filename from the uri, so the file keeps its original filename.
4. Each file is a `zip`, extract the `csv` from the `zip` and delete the `zip` file.
5. For extra credit, download the files in an `async` manner using the `Python` package `aiohttp`. Also try using `ThreadPoolExecutor` in `Python` to download the files. Also write unit tests to improve your skills.
"""

from __future__ import annotations

__author__ = 'Max Drexler'
__email__ = 'mndrexler@gmail.com'

import os
import logging

import requests as re
from tqdm import tqdm


LOG = logging.getLogger('exercise1')

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]


def init():
    """Initialize the script."""
    logging.basicConfig(level=logging.INFO)


def download_file(uri: str, filepath: str) -> None:
    """Downloads a uri to a local filepath. Prints a status bar for
    the download.
    """
    block_size = 1024
    LOG.debug("Getting %s", uri)

    resp = re.get(uri, stream=True)
    resp.raise_for_status()

    total = int(resp.headers.get('content-length', 0))

    with tqdm(total=total, unit="B", unit_scale=True) as bar:
        with open(filepath, 'wb') as d_file:
            for chunk in resp.iter_content(chunk_size=block_size):
                bar.update(len(chunk))
                d_file.write(chunk)


def main():
    init()

    # 1. create 'downloads' directory if it doesn't exist
    download_dir = os.path.join(os.curdir, 'downloads')
    os.makedirs(download_dir, exist_ok=True)

    # 2. download the files one by one
    for uri in download_uris:
        download_path = os.path.join(download_dir, os.path.basename(uri))
        download_file(uri, download_path)
        LOG.info("Wrote to: %s", download_path)

if __name__ == "__main__":
    main()
