import sys
from pathlib import Path
import re
import shutil
from concurrent.futures import ThreadPoolExecutor
import os

JPEG_IMAGES = []
PNG_IMAGES = []
JPG_IMAGES = []
SVG_IMAGES = []

AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO = []
MKV_VIDEO = []

DOC_DOCUMENT = []
DOCX_DOCUMENT = []
TXT_DOCUMENT = []
PDF_DOCUMENT = []
XLSX_DOCUMENT = []
PPTX_DOCUMENT = []

MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO = []
AMR_AUDIO = []

ZIP_ARCHIVES = []
GZ_ARCHIVES = []
TAR_ARCHIVES = []

MY_OTHER = []

REGISTER_EXTENSION = {
    'JPEG': JPEG_IMAGES,
    'JPG': JPG_IMAGES,
    'PNG': PNG_IMAGES,
    'SVG': SVG_IMAGES,
    "AVI": AVI_VIDEO,
    "MP4": MP4_VIDEO,
    "MOV": MOV_VIDEO,
    "MKV": MKV_VIDEO,
    "DOC": DOC_DOCUMENT,
    "DOCX": DOCX_DOCUMENT,
    "TXT": TXT_DOCUMENT,
    "PDF": PDF_DOCUMENT,
    "XLSX": XLSX_DOCUMENT,
    "PPTX": PPTX_DOCUMENT,
    'MP3': MP3_AUDIO,
    "OGG": OGG_AUDIO,
    "WAV": WAV_AUDIO,
    "AMR": AMR_AUDIO,
    'ZIP': ZIP_ARCHIVES,
    "GZ": GZ_ARCHIVES,
    "TAR": TAR_ARCHIVES,
}

FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(name: str) -> str:
    return Path(name).suffix[1:].upper()


def scan(folder: Path):
    with ThreadPoolExecutor() as executor:
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                    FOLDERS.append(item)
                    executor.submit(scan, item)
                continue

            extension = get_extension(item.name)
            full_name = folder / item.name
            if not extension:
                MY_OTHER.append(full_name)
            else:
                try:
                    ext_reg = REGISTER_EXTENSION[extension]
                    ext_reg.append(full_name)
                    EXTENSIONS.add(extension)
                except KeyError:
                    UNKNOWN.add(extension)
                    MY_OTHER.append(full_name)


def move_file(file_path: Path, output_folder: Path):
    try:
        _, extension = os.path.splitext(file_path)
        extension = extension[1:].upper()
        output_path = output_folder / extension

        if not output_path.exists():
            output_path.mkdir(parents=True)

        shutil.move(file_path, output_path / file_path.name)
        print(f"Moved: {file_path} to {output_path}")

    except Exception as e:
        print(f"Error moving {file_path}: {e}")


def process_folder(folder_path: Path, output_folder: Path):
    if not output_folder.exists():
        output_folder.mkdir(parents=True)

    with ThreadPoolExecutor() as executor:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = Path(root) / file
                executor.submit(move_file, file_path, output_folder)


if __name__ == "__main__":
    input_folder = Path(sys.argv[1])
    output_folder = Path("Сортовано")

    scan(input_folder)

    with ThreadPoolExecutor() as executor:
        for folder in FOLDERS:
            executor.submit(scan, folder)


    def process_files(file_list, output_folder, subfolder):
        with ThreadPoolExecutor() as executor:
            for file in file_list:
                executor.submit(move_file, file, output_folder / subfolder / get_extension(file.name))


    # Для зображень
    image_types = ['JPEG', 'JPG', 'PNG', 'SVG']
    for image_type in image_types:
        process_files(REGISTER_EXTENSION[image_type], output_folder / 'images', image_type)

    # Для відео
    video_types = ['AVI', 'MP4', 'MOV', 'MKV']
    for video_type in video_types:
        process_files(REGISTER_EXTENSION[video_type], output_folder / 'video', video_type)

    # Для документів
    document_types = ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX']
    for document_type in document_types:
        process_files(REGISTER_EXTENSION[document_type], output_folder / 'documents', document_type)

    # Для аудіо
    audio_types = ['MP3', 'OGG', 'WAV', 'AMR']
    for audio_type in audio_types:
        process_files(REGISTER_EXTENSION[audio_type], output_folder / 'audio', audio_type)

    # Для архівів
    archive_types = ['ZIP', 'GZ', 'TAR']
    for archive_type in archive_types:
        process_files(REGISTER_EXTENSION[archive_type], output_folder, archive_type)

    # Для інших файлів
    process_files(MY_OTHER, output_folder / 'MY_OTHER', 'other')

    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')
