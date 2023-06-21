#!/usr/bin/env python3

import argparse
from application import Configuration, Storage, Downloader, Server

configuration = Configuration.from_yaml()
storage = Storage(configuration)


# Starts the server
def server_handler() -> None:
    server = Server(configuration, storage)
    server.start()


# Downloads all the missing data
def downloader_handler() -> None:
    downloader = Downloader(storage)

    for checkpoint in configuration.stable_diffusion().get_checkpoints().get_entities():
        downloader.download_checkpoint(checkpoint)

    for lora in configuration.stable_diffusion().get_loras().get_entities():
        downloader.download_lora(lora)

    for upscaler in configuration.stable_diffusion().get_upscalers().get_entities():
        downloader.download_upscaler(upscaler)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["server", "download"], help="Specify the command to run")

    args = parser.parse_args()

    if args.command == "server":
        server_handler()
    else:
        downloader_handler()


if __name__ == "__main__":
    main()
