import sys
from pathlib import Path

JPEG_IMAGES = []
JPG_IMAGES = []
PNG_IMAGES = []
SVG_IMAGES = []
MP3_AUDIO = []
OGG_AUDIO = []
WAV_AUDIO =[]
AMR_AUDIO = []
AVI_VIDEO = []
MP4_VIDEO = []
MOV_VIDEO =[]
MKV_VIDEO = []

DOC_DOCUMENTS = []
DOCX_DOCUMENTS = []
DOCX_DOCUMENTS1 =[]
TXT_DOCUMENTS = []
PDF_DOCUMENTS = []
XLSX_DOCUMENTS = []
PPTX_DOCUMENTS = []

ZIP_ARCHIV = []
GZ_ARCHIV = []
TAR_ARCHIV = []
MY_OTHER = []

REGISTER_EXTENSIONS = {
    'JPEG': JPEG_IMAGES,
    'PNG': PNG_IMAGES,
    'JPG': JPG_IMAGES,
    'SVG': SVG_IMAGES,
    'MP3': MP3_AUDIO,
    'OGG': OGG_AUDIO,
    'WAV': WAV_AUDIO,
    'AMR': AMR_AUDIO,
    'AVI': AVI_VIDEO,
    'MP4': MP4_VIDEO,
    'MOV': MOV_VIDEO,
    'MKV': MKV_VIDEO,

    'ZIP': ZIP_ARCHIV,
    'GZ': GZ_ARCHIV,
    'TAR': TAR_ARCHIV,
    'DOC': DOC_DOCUMENTS,
    '(DOCX)': DOCX_DOCUMENTS1,
    'DOCX': DOCX_DOCUMENTS,
    'TXT': TXT_DOCUMENTS,
    'PDF': PDF_DOCUMENTS,
    'XLSX': XLSX_DOCUMENTS,
    'PPTX': PPTX_DOCUMENTS
}

SAVE_TO = {
    'JPEG': 'images',
    'PNG': 'images',
    'JPG': 'images',
    'SVG': 'images',
    'MP3': 'audios',
    'OGG': 'audios',
    'WAV': 'audios',
    'AMR': 'audios',
    'AVI': 'videos',
    'MP4': 'videos',
    'MOV': 'videos',
    'MKV': 'videos',

    'ZIP': 'archives',
    'GZ': 'archives',
    'TAR': 'archives',
    'DOC': 'documents',
    'DOCX': 'documents',
    'DOCX': 'documents',
    'TXT': 'documents',
    'PDF': 'documents',
    'XLSX': 'documents',
    'PPTX': 'documents'
}


FOLDERS = []
EXTENSIONS = set()
UNKNOWN = set()


def get_extension(filename: str) -> str:
    # перетворюємо розширення файлу на назву папки .jpg -> JPG
    return Path(filename).suffix[1:].upper()


def scan(folder: Path) -> None:
    for item in folder.iterdir():
        # Якщо це папка то додаємо її зі списку FOLDERS і переходимо до наступного елемента папки
        if item.is_dir():
            # перевіряємо, щоб папка не була тією, в яку ми складаємо вже файли.
            if item.name not in ('archives', 'video', 'audio', 'documents', 'images', 'MY_OTHER'):
                FOLDERS.append(item)
                # скануємо цю вкладену папку - рекурсія
                scan(item)
            # перейти до наступного елемента в сканованій папці
            continue

        # Робота з файлом
        ext = get_extension(item.name)  # взяти розширення
        fullname = folder / item.name  # взяти повний шлях до файлу
        if not ext:  # якщо файл не має розширення додати до невідомих
            MY_OTHER.append(fullname)
        else:
            try:
                # взяти список куди покласти повний шлях до файлу
                container = REGISTER_EXTENSIONS[ext]
                EXTENSIONS.add(ext)
                container.append(fullname)
            except KeyError:
                # Якщо ми не реєстрували розширення у REGISTER_EXTENSIONS, то додати до іншого
                UNKNOWN.add(ext)
                MY_OTHER.append(fullname)


if __name__ == '__main__':

    folder_for_scan = sys.argv[1]
    print(f'Start in folder {folder_for_scan}')

    scan(Path(folder_for_scan))
    print(f'Images jpeg: {JPEG_IMAGES}')
    print(f'Images jpg: {JPG_IMAGES}')
    print(f'Images svg: {SVG_IMAGES}')
    print(f'Audio mp3: {MP3_AUDIO}')
    print(f'Archiv zip: {ZIP_ARCHIV}')


    print(f'Types of files in folder: {EXTENSIONS}')
    print(f'Unknown files of types: {UNKNOWN}')

    print(FOLDERS[::-1])

import re

CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'[()+\-*/<>][^.]', '_', t_name)
    return t_name
import shutil
import sys



def handle_media(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_other(filename: Path, target_folder: Path):
    target_folder.mkdir(exist_ok=True, parents=True)
    filename.replace(target_folder / normalize(filename.name))


def handle_archive(filename: Path, target_folder: Path):
    # Створюємо папку для архіву
    target_folder.mkdir(exist_ok=True, parents=True)
    # Створюємо папку куди розпакуємо архів
    # Беремо суфікс у файла і удаляємо replace(filename.suffix, '')
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, ''))

    # Створюємо папку для архіву з іменем файлу
    folder_for_file.mkdir(exist_ok=True, parents=True)
    try:
        shutil.unpack_archive(str(filename.resolve()), str(folder_for_file.resolve()))

        for item in folder_for_file.iterdir():
            pass
            # if normalize(item.name) is not item.name:
                # item.rename(normalize(item.name))


    except shutil.ReadError:
        print(f'Це не архів {filename}!')
        folder_for_file.rmdir()
        return None
    filename.unlink()


def handle_folder(folder: Path):
    try:
        folder.rmdir()
    except OSError:
        print(f'Помилка видалення папки {folder}')

USE_METHOD = {
    'JPEG': handle_media,
    'PNG': handle_media,
    'JPG': handle_media,
    'SVG': handle_media,
    'MP3': handle_media,
    'OGG': handle_media,
    'WAV': handle_media,
    'AMR': handle_media,
    'AVI': handle_media,
    'MP4': handle_media,
    'MOV': handle_media,
    'MKV': handle_media,
    'DOC': handle_media,
    'DOCX': handle_media,
    'DOCX': handle_media,
    'TXT': handle_media,
    'PDF': handle_media,
    'XLSX': handle_media,
    'PPTX': handle_media,
    'ZIP': handle_archive,
    'GZ': handle_archive,
    'TAR': handle_archive,
}

def main(folder: Path):
    scan(folder)
    save_to_keys = SAVE_TO.keys()

    for path in save_to_keys:
        for file in REGISTER_EXTENSIONS[path]:
            USE_METHOD[path](file, folder / SAVE_TO[path])

    for file in MY_OTHER:
        handle_other(file, folder / 'MY_OTHER')


    # Виконуємо реверс списку для того щоб видалити всі папки
    for folder in FOLDERS[::-1]:
        handle_folder(folder)

def path_function():
    try:
        folder = sys.argv[1]
    except IndexError:
        print('Enter valid path to the folder')
    else:
        folder_for_scan = Path(folder)
        print(f'Start in folder {folder_for_scan.resolve()}')
        main(folder_for_scan.resolve())


if __name__ == '__main__':
    path_function()


# TODO: запускаємо:  python3 main.py `назва_папки_для_сортування`