import hashlib
import os

DEV_FILES = [".py", ".cpp", ".ini"]
MUSIC_FILES = [".mp3"]
VIDEO_FILES = [".mp4"]


# class File:
#     pass


def get_checksum(file_name: str) -> str:
    """Returns checksum of the file"""
    sha_hash = hashlib.sha224()
    a_file = open(file_name, "rb")
    content = a_file.read()
    sha_hash.update(content)
    digest = sha_hash.hexdigest()
    return digest


def parser(startpath: str) -> tuple:
    """Utility method to parse the filesystem"""
    file_and_hash = {}
    dirs_list = []
    files_lst = []

    def parse(startpath1: str) -> tuple:
        for root, dirs, files in os.walk(startpath1):
            dir_content = []
            for dir in dirs:
                if dir[0] != ".":
                    go_inside = os.path.join(startpath1, dir)
                    dirs_list.append(go_inside)
                    dir_content.append(parse(go_inside))
            for f in files:
                ffile = os.path.join(startpath1, f)
                if os.path.isfile(ffile):
                    hash = get_checksum(ffile)
                    file = {}
                    file["name"] = f
                    file["hash"] = hash
                    file["extension"] = os.path.splitext(f)[-1]
                    files_lst.append(file)
                    if file_and_hash.get(hash) is None:
                        file_and_hash[hash] = [(root, f)]
                    else:
                        file_and_hash[hash].append((root, f))
            return file_and_hash, dirs_list, files_lst

    parsed_data = parse(startpath)
    return parsed_data[0], parsed_data[1], parsed_data[2]


class FileManager:
    """filemanager class having APIs to manger filesystem"""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = parser(self.file_path)

    def get_dupliacte(self) -> dict:
        """Returs a list of list having duplicate files"""
        ans = []
        files = {}
        for i in self.data[0].values():
            if len(i) > 1:
                ans.append(i)
        for i in ans:
            for j in i:
                if files.get(j[1]) is None:
                    files[j[1]] = [j[0]]
                else:
                    files[j[1]].append(j[0])
        return files

    def get_directories(self) -> list:
        """Returns list of directories present inside the directory you fired this command"""
        return self.data[1]

    def get_files(self) -> list:
        """Returns files present in the directory you fired this command"""
        files = []
        for i in self.data[2]:
            files.append(i["name"])
        return files


if __name__ == "__main__":
    input_param = os.getcwd()
    print(input_param)
    file_mgr = FileManager(input_param)
    pfiles = file_mgr.get_files()
    print(pfiles)

    s = file_mgr.get_directories()
    print(s)

    p = file_mgr.get_dupliacte()
    print(p)
