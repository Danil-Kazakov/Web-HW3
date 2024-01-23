import concurrent.futures
from pathlib import Path
import sys
import shutil
from normalize import normalize
from file_parser import scan, JPEG_IMAGES, JPG_IMAGES, PNG_IMAGES, SVG_IMAGES, AVI_VIDEO, MP4_VIDEO, MOV_VIDEO, MKV_VIDEO, DOC_DOCUMENT, DOCX_DOCUMENT, TXT_DOCUMENT, PDF_DOCUMENT, XLSX_DOCUMENT, PPTX_DOCUMENT, MP3_AUDIO, OGG_AUDIO, WAV_AUDIO, AMR_AUDIO, ZIP_ARCHIVES, GZ_ARCHIVES, TAR_ARCHIVES, MY_OTHER, FOLDERS

def handle_media(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    file_name.replace(target_folder / normalize(file_name.name))

def handle_archive(file_name: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    folder_for_file = target_folder / normalize(file_name.name.replace(file_name.suffix, ''))
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(file_name.absolute()), str(folder_for_file.absolute()))
    except shutil.ReadError:
        folder_for_file.rmdir()
        return
    file_name.unlink()

def process_files(files, target_folder, handle_func):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(handle_func, file, target_folder): file for file in files}
        concurrent.futures.wait(futures)

def main(folder: Path):
    scan(folder)


    process_files(JPEG_IMAGES, folder / 'images' / 'JPEG', handle_media)
    process_files(JPG_IMAGES, folder / 'images' / 'JPG', handle_media)
    process_files(PNG_IMAGES, folder / 'images' / 'PNG', handle_media)
    process_files(SVG_IMAGES, folder / 'images' / 'SVG', handle_media)


    process_files(AVI_VIDEO, folder / 'video' / 'AVI', handle_media)
    process_files(MP4_VIDEO, folder / 'video' / 'MP4', handle_media)
    process_files(MOV_VIDEO, folder / 'video' / 'MOV', handle_media)
    process_files(MKV_VIDEO, folder / 'video' / 'MKV', handle_media)


    process_files(DOC_DOCUMENT, folder / 'documents' / 'DOC', handle_media)
    process_files(DOCX_DOCUMENT, folder / 'documents' / 'DOCX', handle_media)
    process_files(TXT_DOCUMENT, folder / 'documents' / 'TXT', handle_media)
    process_files(PDF_DOCUMENT, folder / 'documents' / 'PDF', handle_media)
    process_files(XLSX_DOCUMENT, folder / 'documents' / 'XLSX', handle_media)
    process_files(PPTX_DOCUMENT, folder / 'documents' / 'PPTX', handle_media)


    process_files(MP3_AUDIO, folder / 'audio' / 'MP3', handle_media)
    process_files(OGG_AUDIO, folder / 'audio' / 'OGG', handle_media)
    process_files(WAV_AUDIO, folder / 'audio' / 'WAV', handle_media)
    process_files(AMR_AUDIO, folder / 'audio' / 'AMR', handle_media)


    process_files(ZIP_ARCHIVES, folder / 'ZIP', handle_archive)
    process_files(GZ_ARCHIVES, folder / 'GZ', handle_archive)
    process_files(TAR_ARCHIVES, folder / 'TAR', handle_archive)


    process_files(MY_OTHER, folder / 'MY_OTHER', handle_media)


    for folder in FOLDERS[::-1]:
        try:
            folder.rmdir()
        except OSError:
            print(f'Error during remove folder {folder}')

if __name__ == "__main__":
    folder_process = Path(sys.argv[1])
    main(folder_process.resolve())
