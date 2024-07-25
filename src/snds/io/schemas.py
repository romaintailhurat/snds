import httpx
import pathlib
import os
import datetime
import logging
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

GITLAB_BASE_REPO_URL = "https://gitlab.com/api/v4/projects/11935694/repository/"
GITLAB_BASE_REPO_FILES_URL = (
    "https://gitlab.com/healthdatahub/applications-du-hdh/schema-snds/-/raw/master/"
)

PATH_TO_CACHE_FILE = pathlib.Path.cwd() / "temp" / "schemas" / "download.cache"
PATH_TO_SCHEMAS_DIR = pathlib.Path.cwd() / "temp" / "schemas"

CACHE_DURATION_IN_DAYS = 7


def cache_is_over(cache_file_path: pathlib.Path) -> bool:
    """Check if the cache file is older than a certain amount of time"""
    logger.debug("Checking cache duration.")
    tt = os.path.getmtime(cache_file_path)
    delta = datetime.datetime.now() - datetime.datetime.fromtimestamp(tt)
    logger.debug(f"Cache file is {delta.days} days old.")
    return delta.days > CACHE_DURATION_IN_DAYS


def create_cache_file(path: pathlib.Path):
    logger.debug(f"Creating cache file at {path}")
    with open(path, "w") as cache_file:
        cache_file.write("This is the cache file.")


def get_schemas_urls() -> list[str]:
    """Get the list of schemas paths on the Gitlab repo"""
    resp_tree = httpx.get(f"{GITLAB_BASE_REPO_URL}tree?path=schemas")
    schemas_sub_dirs = [o["path"] for o in resp_tree.json()]
    all_schemas_path = []

    for sub_dir in schemas_sub_dirs:
        # TODO filter on sub_dir if we dont want everything
        resp_sub_dir = httpx.get(
            f"https://gitlab.com/api/v4/projects/11935694/repository/tree?path={sub_dir}"
        )
        paths = [
            f"{GITLAB_BASE_REPO_FILES_URL}{o["path"]}" for o in resp_sub_dir.json()
        ]
        all_schemas_path = all_schemas_path + paths

    return all_schemas_path


def clean_schemas_dir(path_to_schemas_dir: pathlib.Path):
    for file in path_to_schemas_dir.iterdir():
        os.remove(file)  # we should only have files here


def get_last_part_of_url(url):
    return url.split("/")[-1]


def download_schemas(urls: list[str], path_to_write_to: pathlib.Path):
    for url in urls:
        logger.debug(f"Downloading schema file at {url}")
        resp = httpx.get(url)
        if resp.status_code == httpx.codes.OK:
            data = resp.json()
            name = get_last_part_of_url(url)
            file_path = PATH_TO_SCHEMAS_DIR / name
            logger.debug(f"Writing data to {file_path}")
            with open(PATH_TO_SCHEMAS_DIR / name, "w") as data_file:
                json.dump(data, data_file)


def get_schemas_files():
    """
    Download SNDS schema files if we don't have them already or if the cache is stale.
    Storage location for files is decided by the `PATH_TO_SCHEMAS_DIR` constant.
    """
    logger.info("Getting SNDS schema files.")
    schemas_dir_exists = PATH_TO_SCHEMAS_DIR.exists()
    schema_cache_file_exists = PATH_TO_CACHE_FILE.exists()
    if schemas_dir_exists:
        if schema_cache_file_exists:
            with open(PATH_TO_CACHE_FILE) as cache_file:
                logger.debug("Cache file exists.")
                if cache_is_over(PATH_TO_CACHE_FILE):
                    logger.info("Cache is over, downloading schemas.")
                    clean_schemas_dir(PATH_TO_SCHEMAS_DIR)
                    download_schemas(get_schemas_urls(), PATH_TO_SCHEMAS_DIR)
                    create_cache_file(PATH_TO_CACHE_FILE)
                else:
                    logger.info("Cache is still valid, no download.")
        else:
            logger.info("There is no cache file, downloading.")
            clean_schemas_dir(PATH_TO_SCHEMAS_DIR)
            download_schemas(get_schemas_urls(), PATH_TO_SCHEMAS_DIR)
            create_cache_file(PATH_TO_CACHE_FILE)
    else:
        logger.info(
            "Schemas dir and cache don't exist, creating them and downloading files."
        )
        os.makedirs(PATH_TO_SCHEMAS_DIR)  # try catch?
        download_schemas(get_schemas_urls(), PATH_TO_SCHEMAS_DIR)
        create_cache_file(PATH_TO_CACHE_FILE)
