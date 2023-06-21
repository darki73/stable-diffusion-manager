from os import getcwd, path, listdir
from yaml import safe_load
from json import dumps, loads
from typing import Dict, List, Any


# Class: DownloadableEntity
class DownloadableEntity:
    # Name of the local entity
    _name: str
    # URL to download from
    _url: str

    # Constructor
    def __init__(self, name: str, url: str):
        self._name = name
        self._url = url

    # Returns the name of the entity
    def get_name(self) -> str:
        return self._name

    # Returns the URL of the entity
    def get_url(self) -> str:
        return self._url

    # Returns TRUE if the entity is valid
    def is_valid(self) -> bool:
        return self.get_name() != "" and self.get_url() != ""

    # Returns the entity as a dictionary
    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.get_name(),
            "url": self.get_url(),
        }

    # Returns the entity as a JSON string
    def to_json(self) -> str:
        return dumps(self.to_dict(), indent=4)

    # Returns the entity as a string
    def __str__(self) -> str:
        return self.to_json()

    # Creates an entity from a dictionary
    @staticmethod
    def from_dict(entity: Dict[str, str]) -> "DownloadableEntity":
        return DownloadableEntity(
            name=entity.get("name", ""),
            url=entity.get("url", "")
        )

    # Creates an entity from a JSON string
    @staticmethod
    def from_json(entity: str) -> "DownloadableEntity":
        return DownloadableEntity.from_dict(loads(entity))


# Class: DownloadableCollection
class DownloadableCollection:
    # Collection of entities
    _entities: List[DownloadableEntity]

    # Constructor
    def __init__(self, entities=None):
        if entities is None:
            entities = []
        self._entities = entities

    # Returns the entities
    def get_entities(self) -> List[DownloadableEntity]:
        return self._entities

    # Adds an entity
    def add_entity(self, entity: DownloadableEntity) -> "DownloadableCollection":
        if entity.is_valid():
            self._entities.append(entity)
        else:
            print(f"Invalid entity: `{entity}`, skipping...")
        return self

    # Adds multiple entities
    def add_entities(self, entities: List[DownloadableEntity]) -> "DownloadableCollection":
        for entity in entities:
            self.add_entity(entity)
        return self

    # Removes an entity
    def remove_entity(self, entity: DownloadableEntity) -> "DownloadableCollection":
        self._entities.remove(entity)
        return self

    # Removes multiple entities
    def remove_entities(self, entities: List[DownloadableEntity]) -> "DownloadableCollection":
        for entity in entities:
            self.remove_entity(entity)
        return self

    # Returns the collection as a dictionary
    def to_dict(self) -> List[Dict[str, str]]:
        return [entity.to_dict() for entity in self.get_entities()]

    # Returns the collection as a JSON string
    def to_json(self) -> str:
        return dumps(self.to_dict(), indent=4)

    # Returns the collection as a string
    def __str__(self) -> str:
        return self.to_json()

    # Creates a collection from a dictionary
    @staticmethod
    def from_dict(collection: List[Dict[str, str]]) -> "DownloadableCollection":
        return DownloadableCollection(
            entities=[DownloadableEntity.from_dict(entity) for entity in collection]
        )

    # Creates a collection from a JSON string
    @staticmethod
    def from_json(collection: str) -> "DownloadableCollection":
        return DownloadableCollection.from_dict(loads(collection))


# Class: SafetensorsEntity
class SafetensorsEntity(DownloadableEntity):

    # Returns the name of the entity
    def get_name(self) -> str:
        if self._name == "":
            return ""

        if "." in self._name:
            file_name, extension = self._name.split(".")
            if extension != "safetensors":
                return f"{file_name}.safetensors"
            return self._name

        return f"{self._name}.safetensors"


# Class: CheckpointEntity
class CheckpointEntity(DownloadableEntity):

    # Returns the name of the entity
    def get_name(self) -> str:
        if self._name == "":
            return ""

        if "." in self._name:
            file_name, extension = self._name.split(".")
            if extension != "pt" or extension != "pth" or extension != "ckpt":
                return f"{file_name}.pth"
            return self._name

        return f"{self._name}.pth"


# Class: CheckpointConfiguration
class CheckpointConfiguration(CheckpointEntity, DownloadableEntity):
    pass


# Class: CheckpointsConfiguration
class CheckpointsConfiguration(DownloadableCollection):

    # Creates a collection from a dictionary
    @staticmethod
    def from_dict(collection: List[Dict[str, str]]) -> "CheckpointsConfiguration":
        return CheckpointsConfiguration(
            entities=[CheckpointConfiguration.from_dict(entity) for entity in collection]
        )

    # Creates a collection from a JSON string
    @staticmethod
    def from_json(collection: str) -> "CheckpointsConfiguration":
        return CheckpointsConfiguration.from_dict(loads(collection))


# Class: LoraConfiguration
class LoraConfiguration(SafetensorsEntity, DownloadableEntity):
    pass


# Class: LorasConfiguration
class LorasConfiguration(DownloadableCollection):

    # Creates a collection from a dictionary
    @staticmethod
    def from_dict(collection: List[Dict[str, str]]) -> "LorasConfiguration":
        return LorasConfiguration(
            entities=[LoraConfiguration.from_dict(entity) for entity in collection]
        )

    # Creates a collection from a JSON string
    @staticmethod
    def from_json(collection: str) -> "LorasConfiguration":
        return LorasConfiguration.from_dict(loads(collection))


# Class: UpscalerConfiguration
class UpscalerConfiguration(SafetensorsEntity, DownloadableEntity):
    pass


# Class: UpscalersConfiguration
class UpscalersConfiguration(DownloadableCollection):

    # Creates a collection from a dictionary
    @staticmethod
    def from_dict(collection: List[Dict[str, str]]) -> "UpscalersConfiguration":
        return UpscalersConfiguration(
            entities=[UpscalerConfiguration.from_dict(entity) for entity in collection]
        )

    # Creates a collection from a JSON string
    @staticmethod
    def from_json(collection: str) -> "UpscalersConfiguration":
        return UpscalersConfiguration.from_dict(loads(collection))

# Class: GalleryConfiguration
class GalleryConfiguration:
    # Listen address
    _listen_address: str
    # Listen port
    _listen_port: int

    # Constructor
    def __init__(self, listen_address: str, listen_port: int):
        self._listen_address = listen_address
        self._listen_port = listen_port

    # Returns the listen address
    def get_listen_address(self) -> str:
        return self._listen_address

    # Returns the listen port
    def get_listen_port(self) -> int:
        return self._listen_port

    # Returns the configuration as a dictionary
    def to_dict(self) -> Dict[str, Any]:
        return {
            "listen_address": self.get_listen_address(),
            "listen_port": self.get_listen_port(),
        }

    # Returns the configuration as a JSON string
    def to_json(self) -> str:
        return dumps(self.to_dict(), indent=4)

    # Returns the configuration as a string
    def __str__(self) -> str:
        return self.to_json()

    # Creates a configuration from a dictionary
    @staticmethod
    def from_dict(configuration: Dict[str, Any]) -> "GalleryConfiguration":
        return GalleryConfiguration(
            listen_address=configuration.get("listen_address", "0.0.0.0"),
            listen_port=configuration.get("listen_port", 5000),
        )

    # Creates a configuration from a JSON string
    @staticmethod
    def from_json(configuration: str) -> "GalleryConfiguration":
        return GalleryConfiguration.from_dict(loads(configuration))


# Class: StableDiffusionConfiguration
class StableDiffusionConfiguration:
    # Stable Diffusion directory
    _stable_diffusion_directory: str
    # Stable Diffusion checkpoints
    _stable_diffusion_checkpoints: CheckpointsConfiguration
    # Stable Diffusion Loras
    _stable_diffusion_loras: LorasConfiguration
    # Stable Diffusion upscalers
    _stable_diffusion_upscalers: UpscalersConfiguration

    # Constructor
    def __init__(
        self,
        directory: str,
        checkpoints: CheckpointsConfiguration,
        loras: LorasConfiguration,
        upscalers: UpscalersConfiguration,
    ):
        self._stable_diffusion_directory = directory
        self._stable_diffusion_checkpoints = checkpoints
        self._stable_diffusion_loras = loras
        self._stable_diffusion_upscalers = upscalers

    # Returns the Stable Diffusion directory
    def get_directory(self) -> str:
        return self._stable_diffusion_directory

    # Returns the Stable Diffusion checkpoints
    def get_checkpoints(self) -> CheckpointsConfiguration:
        return self._stable_diffusion_checkpoints

    # Returns the Stable Diffusion Loras
    def get_loras(self) -> LorasConfiguration:
        return self._stable_diffusion_loras

    # Returns the Stable Diffusion upscalers
    def get_upscalers(self) -> UpscalersConfiguration:
        return self._stable_diffusion_upscalers

    # Returns the configuration as a dictionary
    def to_dict(self) -> Dict[str, Any]:
        return {
            "directory": self.get_directory(),
            "checkpoints": self.get_checkpoints().to_dict(),
            "loras": self.get_loras().to_dict(),
            "upscalers": self.get_upscalers().to_dict(),
        }

    # Returns the configuration as a JSON string
    def to_json(self) -> str:
        return dumps(self.to_dict(), indent=4)

    # Returns the configuration as a string
    def __str__(self) -> str:
        return self.to_json()

    # Creates a configuration from a dictionary
    @staticmethod
    def from_dict(configuration: Dict[str, Any]) -> "StableDiffusionConfiguration":
        return StableDiffusionConfiguration(
            directory=configuration.get("path", ""),
            checkpoints=CheckpointsConfiguration.from_dict(
                configuration.get("checkpoints", [])
            ),
            loras=LorasConfiguration.from_dict(
                configuration.get("loras", [])
            ),
            upscalers=UpscalersConfiguration.from_dict(
                configuration.get("upscalers", [])
            ),
        )

    # Creates a configuration from a JSON string
    @staticmethod
    def from_json(configuration: str) -> "StableDiffusionConfiguration":
        return StableDiffusionConfiguration.from_dict(loads(configuration))


# Class: Configuration
class Configuration:
    # Gallery configuration
    _gallery_configuration: GalleryConfiguration
    # Stable Diffusion configuration
    _stable_diffusion_configuration: StableDiffusionConfiguration

    # Constructor
    def __init__(
        self,
        gallery: GalleryConfiguration,
        stable_diffusion: StableDiffusionConfiguration,
    ):
        self._gallery_configuration = gallery
        self._stable_diffusion_configuration = stable_diffusion

    # Returns the gallery configuration
    def gallery(self) -> GalleryConfiguration:
        return self._gallery_configuration

    # Returns the Stable Diffusion configuration
    def stable_diffusion(self) -> StableDiffusionConfiguration:
        return self._stable_diffusion_configuration

    # Returns the configuration as a dictionary
    def to_dict(self) -> Dict[str, Any]:
        return {
            "gallery": self.gallery().to_dict(),
            "stable_diffusion": self.stable_diffusion().to_dict(),
        }

    # Returns the configuration as a JSON string
    def to_json(self) -> str:
        return dumps(self.to_dict(), indent=4)

    # Returns the configuration as a string
    def __str__(self) -> str:
        return self.to_json()

    # Creates a configuration from a dictionary
    @staticmethod
    def from_dict(configuration: Dict[str, Any]) -> "Configuration":
        return Configuration(
            gallery=GalleryConfiguration.from_dict(configuration.get("gallery", {})),
            stable_diffusion=StableDiffusionConfiguration.from_dict(
                configuration.get("stable_diffusion", {})
            ),
        )

    # Creates a configuration from a JSON string
    @staticmethod
    def from_json(configuration: str) -> "Configuration":
        return Configuration.from_dict(loads(configuration))

    # Creates a configuration from a YAML file
    @staticmethod
    def from_yaml_file(file_path: str) -> "Configuration":
        with open(file_path, "r") as file:
            return Configuration.from_dict(safe_load(file))

    # Creates a configuration from YAML
    @staticmethod
    def from_yaml():
        directory = getcwd()
        files = [file for file in listdir(directory) if file.endswith(".yaml") or file.endswith(".yml")]
        filtered_files = [file for file in files if "conf" in file or "config" in file or "configuration" in file]
        if len(filtered_files) == 0:
            raise FileNotFoundError("No configuration file found")
        elif len(filtered_files) > 1:
            raise FileExistsError("Multiple configuration files found")
        else:
            return Configuration.from_yaml_file(filtered_files[0])
