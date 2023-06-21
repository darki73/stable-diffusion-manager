from typing import List
from os import path, makedirs, getcwd, listdir
from .configuration import Configuration


# Class: Storage
class Storage:
    # Configuration instance
    _configuration: Configuration
    # List of supported image extensions
    _supported_image_extensions: List[str] = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    ]

    # Constructor
    def __init__(self, configuration: Configuration):
        self._configuration = configuration

    # Returns the configuration instance
    def get_configuration(self) -> Configuration:
        return self._configuration

    # Returns the stable diffusion root directory
    def get_stable_diffusion_path(self) -> str:
        return self._configuration.stable_diffusion().get_directory()

    # Returns the list of supported image extensions
    def get_supported_image_extensions(self) -> List[str]:
        return self._supported_image_extensions

    # Adds a new supported image extension
    def add_supported_image_extension(self, extension: str) -> "Storage":
        if not extension.startswith("."):
            extension = f".{extension}"
        self._supported_image_extensions.append(extension)
        return self

    # Removes a supported image extension
    def remove_supported_image_extension(self, extension: str) -> "Storage":
        if not extension.startswith("."):
            extension = f".{extension}"
        self._supported_image_extensions.remove(extension)
        return self

    # Sets the list of supported image extensions
    def set_supported_image_extensions(self, extensions: List[str]) -> "Storage":
        self._supported_image_extensions = []
        for extension in extensions:
            if not extension.startswith("."):
                self._supported_image_extensions.append(f".{extension}")
        return self

    # Returns the models directory
    def get_models_path(self) -> str:
        return self._get_directory_path(self.get_stable_diffusion_path(), "models")

    # Returns the embeddings directory
    def get_embeddings_path(self) -> str:
        return self._get_directory_path(self.get_stable_diffusion_path(), "embeddings")

    # Returns the scripts directory
    def get_scripts_path(self) -> str:
        return self._get_directory_path(self.get_stable_diffusion_path(), "scripts")

    # Returns the extensions directory
    def get_extensions_path(self) -> str:
        return self._get_directory_path(self.get_stable_diffusion_path(), "extensions")

    # Returns the checkpoints directory
    def get_checkpoints_path(self) -> str:
        return self._get_directory_path(self.get_models_path(), "Stable-diffusion")

    # Returns the loras directory
    def get_loras_path(self) -> str:
        return self._get_directory_path(self.get_models_path(), "Lora")

    # Returns the upscalers directory
    def get_upscalers_path(self) -> str:
        return self._get_directory_path(self.get_models_path(), "ESRGAN")

    # Returns the outputs directory
    def get_outputs_path(self) -> str:
        return self._get_directory_path(self.get_stable_diffusion_path(), "outputs")

    # Returns the images directory
    def get_images_path(self) -> str:
        return self._get_directory_path(self.get_outputs_path(), "txt2img-images")

    # Returns the list of folders in the provided directory
    def get_folders(self, directory: str) -> List[str]:
        folders: List[str] = []

        for item in listdir(directory):
            item_path = path.join(directory, item)
            if path.isdir(item_path):
                folders.append(item)

        return folders

    # Returns list of files in the directory
    def get_files(self, directory: str) -> List[str]:
        files: List[str] = []

        for item in listdir(directory):
            item_path = path.join(directory, item)
            if path.isfile(item_path):
                item_extension = path.splitext(item_path)[1]
                if item_extension in self.get_supported_image_extensions():
                    files.append(item)

        files.sort(key=lambda x: path.getmtime(path.join(directory, x)), reverse=True)

        return files

    # Returns the templates directory
    def get_templates_path(self) -> str:
        return self._get_directory_path(getcwd(), "templates")

    # Returns the checkpoint file path
    def get_checkpoint_file_path(self, checkpoint: str) -> str:
        return path.join(self.get_checkpoints_path(), checkpoint)

    # Returns the lora file path
    def get_lora_file_path(self, lora: str) -> str:
        return path.join(self.get_loras_path(), lora)

    # Returns the upscaler file path
    def get_upscaler_file_path(self, upscaler: str) -> str:
        return path.join(self.get_upscalers_path(), upscaler)

    # Returns the script file path
    def get_script_file_path(self, script: str) -> str:
        return path.join(self.get_scripts_path(), script)

    # Returns the extension file path
    def get_extension_file_path(self, extension: str) -> str:
        return path.join(self.get_extensions_path(), extension)

    # Returns the embeddings file path
    def get_embedding_file_path(self, embeddings: str) -> str:
        return path.join(self.get_embeddings_path(), embeddings)

    # Creates a directory
    def create_directory(self, directory_path: str) -> None:
        if not path.exists(directory_path):
            makedirs(directory_path)

    # Returns TRUE if directory exists
    def directory_exists(self, directory_path: str) -> bool:
        return path.exists(directory_path)

    # Returns TRUE if file exists
    def file_exists(self, file_path: str) -> bool:
        return path.isfile(file_path)

    # Returns the directory path and created directory if it does not exist
    def _get_directory_path(self, main_directory: str, sub_directory: str) -> str:
        directory_path = path.join(main_directory, sub_directory)
        if not self.directory_exists(directory_path):
            self.create_directory(directory_path)
        return directory_path
