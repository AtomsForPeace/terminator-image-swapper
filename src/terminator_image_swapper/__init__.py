import random
from pathlib import Path
from enum import Enum
from dataclasses import dataclass

import click
from configobj import ConfigObj


TERMINATOR_CONFIG_FILE = "~/.config/terminator/config"
IMAGE_WRAPPER_CONFIG_FILE = "~/.config/terminator/image_swapper/config"


class TerminatorImageSwapperError(Exception):
    pass


class BackgroudImageNode(Enum):
    scale_and_fit = 1
    scale_and_crop = 2
    stretch_and_fill = 3
    tiling = 4


@dataclass
class Profile:
    background_darkness: float
    background_type: str
    background_image: Path
    background_image_mode: BackgroudImageNode


def get_image_folder() -> Path:
    config = get_image_swapper_config()
    if 'image_folder' not in config:
        raise TerminatorImageSwapperError(
            "Missing 'image_folder' setting in config file"
            f"({IMAGE_WRAPPER_CONFIG_FILE})."
        )
    image_folder = config['image_folder']
    image_folder_path = Path(image_folder)
    if not image_folder_path.is_dir():
        raise TerminatorImageSwapperError(
            "Given 'image_folder' folder in config file does not exist: "
            f"{image_folder_path}."
        )
    return image_folder_path


def get_image_swapper_config() -> ConfigObj:
    file_path = Path(IMAGE_WRAPPER_CONFIG_FILE).expanduser()
    if not file_path.is_file():
        if not file_path.parent.is_dir():
            file_path.parent.mkdir()
        file_path.touch()
    file_path_str = str(file_path)
    return ConfigObj(file_path_str)


def get_terminator_config() -> ConfigObj:
    file_path = Path(TERMINATOR_CONFIG_FILE).expanduser()
    if not file_path.is_file():
        raise TerminatorImageSwapperError(
            f"Missing terminal config. Looking here: {TERMINATOR_CONFIG_FILE}"
        )
    file_path_str = str(file_path)
    return ConfigObj(file_path_str)


def random_image() -> None:
    profile = read_config_file()
    image_folder = get_image_folder()
    new_image = get_random_file(image_folder, profile.background_image)
    profile.background_image = new_image
    write_config_file(profile)


def read_config_file() -> Profile:
    config = get_terminator_config()
    profiles = config['profiles']
    default = profiles['default']
    background_darkness: float = default['background_darkness']
    background_type: str = default['background_type']
    background_image = Path(default['background_image'])
    background_image_mode: str = default['background_image_mode']
    return Profile(
        background_darkness=background_darkness,
        background_type=background_type,
        background_image=background_image,
        background_image_mode=BackgroudImageNode[background_image_mode]
    )


def write_config_file(profile: Profile) -> None:
    config = get_terminator_config()
    config['profiles']['default']['background_darkness'] = \
        profile.background_darkness
    config['profiles']['default']['background_type'] = \
        profile.background_type
    config['profiles']['default']['background_image'] = \
        profile.background_image
    config['profiles']['default']['background_image_mode'] = \
        profile.background_image_mode
    config.write()


def get_random_file(folder: Path, previous_image: Path) -> Path:
    images = list(folder.iterdir())
    if len(images) == 1:
        return previous_image
    elif len(images) == 0:
        raise TerminatorImageSwapperError(
            f"Image folder given is empty: {folder}"
        )
    image = random.choice(images)
    while image == previous_image:
        image = random.choice(images)
    return image


@ click.command()
@ click.argument('image-folder')
def set_image_folder(image_folder: str) -> None:
    image_folder_path = Path(image_folder)
    if not image_folder_path.is_dir():
        raise TerminatorImageSwapperError(
            "Given 'image_folder' folder in config file does not exist: "
            f"{image_folder_path}."
        )
    config = get_image_swapper_config()
    config['image_folder'] = image_folder_path
    config.write()
