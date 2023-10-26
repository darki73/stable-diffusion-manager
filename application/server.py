from os import path, remove
from application import Configuration, Storage
from flask import Flask, render_template, jsonify, request, redirect, url_for, Response
from PIL import Image


# Class: Server
class Server:
    # Flask application instance
    _app: Flask
    # Configuration instance
    _configuration: Configuration
    # Storage instance
    _storage: Storage
    # Debug mode
    _debug: bool

    # Constructor
    def __init__(self, configuration: Configuration, storage: Storage, debug: bool = False):
        self._app = Flask(
            __name__,
            template_folder=storage.get_templates_path(),
            static_folder=storage.get_images_path(),
        )
        self._configuration = configuration
        self._storage = storage
        self._debug = debug
        self._register_routes()

    # Returns the Flask application instance
    def get_app(self) -> Flask:
        return self._app

    # Returns the configuration instance
    def get_configuration(self) -> Configuration:
        return self._configuration

    # Returns the storage instance
    def get_storage(self) -> Storage:
        return self._storage

    # Returns the debug mode
    def get_debug(self) -> bool:
        return self._debug

    # Starts the server
    def start(self) -> None:
        self._app.run(
            host=self.get_configuration().gallery().get_listen_address(),
            port=self.get_configuration().gallery().get_listen_port(),
            debug=self.get_debug(),
        )

    # Register application routes
    def _register_routes(self) -> None:
        self._app.add_url_rule("/", view_func=self._index_route)
        self._app.add_url_rule("/<folder>", view_func=self._images_route)
        self._app.add_url_rule(
            "/<folder>/<image>", view_func=self._image_route, methods=["GET"]
        )
        self._app.add_url_rule(
            "/delete", view_func=self._delete_image_route, methods=["POST"]
        )

    # Index Route: /
    def _index_route(self) -> str:
        folders = self.get_storage().get_folders(
            self.get_storage().get_images_path(),
        )
        return render_template("index.html", folders=folders)

    # Images Route: /<folder>
    def _images_route(self, folder: str) -> str:
        images_directory = self.get_storage().get_images_path()
        folder_directory = path.join(images_directory, folder)
        images = self.get_storage().get_files(folder_directory)
        return render_template("folder.html", folder=folder, images=images)

    # Image Route: /<folder>/<image>
    def _image_route(self, folder: str, image: str) -> str:
        file_path = path.join(
            self.get_storage().get_images_path(),
            folder,
            image
        )

        if not path.exists(file_path):
            return redirect(url_for("_index_route"))
        
        image_handle = Image.open(file_path)
        
        metadata = image_handle.info

        if 'parameters' in metadata:
            parameters = metadata['parameters'].replace("\n", "\n\n").replace(", ", ",\n").replace("Negative prompt: ", "Negative prompt:\n")
        else:
            parameters = None

        image_handle.close()

        return render_template("image.html", folder=folder, image=image, parameters=parameters)

    # Delete Image Route: /delete
    def _delete_image_route(self) -> Response:
        data = request.get_json()
        folder = data.get("folder")
        image = data.get("image")
        image_path = path.join(
            self.get_storage().get_images_path(),
            folder,
            image
        )

        if path.exists(image_path):
            remove(image_path)
            return jsonify({'status': 'success'})
        else:
            return jsonify({'status': 'error'})
