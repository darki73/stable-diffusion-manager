import requests
from time import time
from os import path
from sys import stdout
from .storage import Storage
from .helpers import bytes_to_readable, seconds_to_readable
from .configuration import CheckpointConfiguration, LoraConfiguration, UpscalerConfiguration


# Class: Downloader
class Downloader:
    # Storage instance
    _storage: Storage

    # Constructor
    def __init__(self, storage: Storage):
        self._storage = storage

    # Returns the storage instance
    def get_storage(self) -> Storage:
        return self._storage

    # Downloads checkpoint file
    def download_checkpoint(self, checkpoint: CheckpointConfiguration) -> None:
        file_path = self.get_storage().get_checkpoint_file_path(checkpoint.get_name())
        self.download_file(checkpoint.get_url(), file_path)

    # Downloads lora file
    def download_lora(self, lora: LoraConfiguration) -> None:
        file_path = self.get_storage().get_lora_file_path(lora.get_name())
        self.download_file(lora.get_url(), file_path)

    # Downloads upscaler file
    def download_upscaler(self, upscaler: UpscalerConfiguration) -> None:
        file_path = self.get_storage().get_upscaler_file_path(upscaler.get_name())
        self.download_file(upscaler.get_url(), file_path)

    # Downloads a file if it doesn't exist or if it's outdated
    def download_file(self, url: str, file_path: str) -> None:
        local_file_size = self._get_local_file_size(file_path)
        remote_file_size = self._get_remote_file_size(url)

        if local_file_size != remote_file_size:
            self._download_file(url, file_path)

    # Returns the file size of the remote file
    def _get_remote_file_size(self, url: str) -> int:
        response = requests.get(url, stream=True)
        file_size = int(response.headers.get('content-length', 0))
        response.close()
        return file_size

    # Returns the file size of the local file
    def _get_local_file_size(self, file_path: str) -> int:
        if path.exists(file_path):
            return path.getsize(file_path)
        return 0

    # Downloads a file
    def _download_file(self, url: str, file_path: str) -> None:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_size = int(response.headers.get('content-length', 0))
            file_size_readable = bytes_to_readable(file_size)
            chunk_size = 1024
            downloaded_size = 0
            start_time = time()

            with open(file_path, 'wb') as file:
                for data in response.iter_content(chunk_size=chunk_size):
                    file.write(data)

                    downloaded_size += len(data)
                    downloaded_size_readable = bytes_to_readable(downloaded_size)

                    progress = (downloaded_size / file_size) * 100
                    elapsed_time = time() - start_time
                    download_speed = downloaded_size / elapsed_time if elapsed_time > 0 else 0
                    remaining_size = file_size - downloaded_size
                    eta = remaining_size / download_speed if download_speed > 0 else 0

                    stdout.write(
                        f"\rDownloading: {url} - {downloaded_size_readable} / {file_size_readable} - {seconds_to_readable(eta)} - {progress:.2f}%")
                    stdout.flush()
            stdout.write('\n')
        else:
            print(f"Unable to download: {url}")