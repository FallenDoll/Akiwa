from typing import List, Optional

import tomli
from creart import exists_module
from creart.creator import AbstractCreator, CreateTargetInfo
from pydantic import BaseModel


class Listening(BaseModel):
    room: List[int]
    user: List[int]


class Jieba(BaseModel):
    words: List[str]
    ignore_words: List[str]
    stop_words: List[str]


class PostPlatform(BaseModel):
    name: str
    data: dict


class PlatformConfig(BaseModel):
    name: str
    template: str
    data: Optional[dict]
    post_platform: Optional[PostPlatform]


class Platform(BaseModel):
    name: List[str]
    config: List[PlatformConfig]

    def find_platform_config(self, name: str):
        for i in self.config:
            if i.name == name:
                return i
        return None


class ConfigModel(BaseModel):
    listening: Listening
    jieba: Jieba
    platform: Platform
    conn_str: str
    database_name: str
    commands: List[str]


class Config:
    config: ConfigModel

    def __init__(self) -> None:
        with open("config.toml", "rb") as f:
            self.config = ConfigModel.parse_obj(tomli.load(f))


class ConfigCreator(AbstractCreator):
    targets = (CreateTargetInfo("src.config", "Config"),)

    @staticmethod
    def available() -> bool:
        return exists_module("src.config")

    @staticmethod
    def create(create_type: type[Config]) -> Config:
        return create_type()
