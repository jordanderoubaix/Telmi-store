import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path
import glob
import zipfile
import os
import re
from unidecode import unidecode
from config import settings


log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
logging.basicConfig(level=getattr(logging, log_level, logging.INFO))


def clean_filename(filename: str) -> str:
    filename = unidecode(filename)
    filename = re.sub(r'[^a-zA-Z0-9_-]', '_', filename)
    return filename

def collect_data():
    data_list = []
    shared_path = Path(settings.SHARED_DIRECTORY_PATH)
    image_path = settings.LIBRARY_LINK + '/data'
    
    logging.info(f"Shared directory path: {shared_path}")
    
    if not shared_path.exists():
        logging.error(f"Shared directory path does not exist: {shared_path}")
        return data_list
    
    # Search all archives files in specified directory
    zip_files = glob.glob(str(shared_path / '*.zip'))

    # Files to be extracted
    files_to_extract = ['metadata.json', 'story.json', 'thumbnail.png', 'title.png', 'cover.png']

    # Destination directory
    destination_parent_path = shared_path / 'data'

    # Create the parent directory if it doesn't exist
    destination_parent_path.mkdir(parents=True, exist_ok=True)

    for zip_file in zip_files:
        # Clean the filename
        original_name = Path(zip_file).stem
        clean_name = clean_filename(original_name)
        
        # Renommer le fichier ZIP s'il contient des caractères spéciaux
        if clean_name != original_name:
            clean_zip_file = shared_path / f"{clean_name}.zip"
            os.rename(zip_file, clean_zip_file)
            zip_file = clean_zip_file
            logging.info(f"Renamed {original_name}.zip to {clean_name}.zip")

        # Name of the destination directory based on the cleaned archive name
        destination_path = destination_parent_path / clean_name

        # Check if the destination directory already exists
        if not destination_path.exists():
            # Create the destination directory
            destination_path.mkdir(parents=True, exist_ok=True)

            # Open the .zip file and extract the specified files
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                # List the contents of the archive
                zip_contents = zip_ref.namelist()
                logging.info(f"Contents of {zip_file}: {zip_contents}")

                for file_name in files_to_extract:
                    # Search for the file in the archive regardless of its location
                    for zip_file_name in zip_contents:
                        if zip_file_name.endswith(file_name):
                            # Extract the file while preserving the directory structure
                            destination_file_path = destination_path / Path(zip_file_name).name
                            with zip_ref.open(zip_file_name) as source, open(destination_file_path, 'wb') as target:
                                target.write(source.read())
                            logging.info(f"Extracted {zip_file_name} to {destination_file_path}")
                            break
                    else:
                        logging.info(f"{file_name} not found in {zip_file}")

        # Read metadata.json or story.json
        metadata_file = destination_path / 'metadata.json'
        story_file = destination_path / 'story.json'

        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                title = metadata.get("title", "Titre par défaut")
                description = metadata.get("description", "Description par défaut")
                version = metadata.get("version", 1)
                image_small = f"{image_path}/{clean_name}/title.png"
                image_medium = f"{image_path}/{clean_name}/cover.png"
        elif story_file.exists():
            with open(story_file, 'r', encoding='utf-8') as f:
                story = json.load(f)
                title = story.get("title", "Titre par défaut")
                description = story.get("description", "Description par défaut")
                version = story.get("version", 1)
                image_small = f"{image_path}/{clean_name}/thumbnail.png"
                image_medium = f"{image_path}/{clean_name}/thumbnail.png"
        else:
            logging.error(f"Neither metadata.json nor story.json found in {destination_path}")
            continue

        # if age = 0, get it from current folder name
        age = metadata.get("age", 0) if metadata_file.exists() else story.get("age", 0)

        # If age is 0, extract it from the current directory name
        if age == 0:
            match = re.search(r'^(\d+)__', clean_name)
            if match:
                age = int(match.group(1))
            else:
                logging.error(f"Could not extract age from directory name {clean_name}")

        # Extract age from the title if it exists and update title without age
        title_match = re.search(r'^(\d+)\+\](.+)', title)
        if title_match:
            age = int(title_match.group(1))
            title = title_match.group(2).strip()

        data_item = {
            "age": age,
            "title": title,
            "description": description,
            "thumbs": {
                "small": image_small,
                "medium": image_medium
            },
            "download": f"{settings.LIBRARY_LINK}/{clean_name}.zip",
            "awards": metadata.get("awards", ["default award"]) if metadata_file.exists() else story.get("awards", ["default award"]),
            "created_at": metadata.get("created_at", datetime.utcnow().isoformat()) if metadata_file.exists() else story.get("created_at", datetime.utcnow().isoformat()),
            "updated_at": metadata.get("updated_at", datetime.utcnow().isoformat()) if metadata_file.exists() else story.get("updated_at", datetime.utcnow().isoformat())
        }

        data_list.append(data_item)
        logging.info(f"Added data item: {data_item}")

    result = {
        "banner": {
            "image": settings.BANNER_IMAGE,
            "link": settings.BANNER_LINK,
            "background": settings.BANNER_BACKGROUND
        },
        "data": data_list
    }
    
    logging.info(f"Final result: {result}")
    return result

