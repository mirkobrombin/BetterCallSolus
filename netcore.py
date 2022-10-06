# mirkobrombin <send@mirko.pm>
# ------------------------------
# Install .NET Core on Solus OS
# License: MIT


import os
import re
import pathlib
import shutil
import tarfile
import urllib.request
import sys

DOTNET_REPO_URL = "https://dotnet.microsoft.com"
DOTNET_REPO_INDEX = f"{DOTNET_REPO_URL}/download/dotnet"
DOTNET_STORE_DIR = f"{pathlib.Path.home()}/.netcore"
DOTNET_STORE_TEMP_DIR = f"{pathlib.Path.home()}/.netcore/temp"


class DotNetModel:
    def __init__(self, version, url):
        self.version = version
        self.url = url


class DotNetManager:
    def __init__(self):
        self.versions = list(self.__fetch_versions())
        self.__check_installation()
        self.__check_dir()
        self.__start_ui()

    @staticmethod
    def __check_installation():
        dotnet_path = shutil.which("dotnet")
        if dotnet_path is not None:
            print("dotnet is already installed")

    @staticmethod
    def __check_dir():
        if not os.path.isdir(DOTNET_STORE_DIR):
            os.mkdir(DOTNET_STORE_DIR)
        if not os.path.isdir(DOTNET_STORE_TEMP_DIR):
            os.mkdir(DOTNET_STORE_TEMP_DIR)

    def __start_ui(self):
        self.__menu_title(".NET Core Manager")
        self.__select_version()
        self.__select_package()
        self.__install_package()

    def __select_version(self):
        self.__menu_title("Select version:")
        for i, version in enumerate(self.versions):
            print(f"{i}. {version.version}")

        try:
            selection = int(input("Select version: "))
            if selection < 0 or selection > len(self.versions):
                raise ValueError
            self.__selected_version = self.versions[selection]
        except ValueError:
            print("Invalid input")
            self.__select_version()

    def __select_package(self):
        self.__menu_title("Select package:")
        print("1. SDK")
        print("2. Runtime")
        print("0. Exit")

        try:
            selection = int(input("Select package: "))
            if selection < 0 or selection > 2:
                raise ValueError
            elif selection == 1:
                self.__selected_package = "sdk"
            elif selection == 2:
                self.__selected_package = "runtime"
            else:
                exit()
        except ValueError:
            print("Invalid input")
            self.__select_package()

    def __install_package(self):
        package_path = f"{DOTNET_STORE_TEMP_DIR}/{self.__selected_version.version}-{self.__selected_package}.tar.gz"
        install_path = f"{DOTNET_STORE_DIR}/{self.__selected_version.version}-{self.__selected_package}".replace(
            " ", "-")

        print("\n")
        print("Downloading package...")
        print("Please wait...")
        url = self.__get_package_url()
        urllib.request.urlretrieve(url, package_path, reporthook=self.__download_progress)

        print("\n")
        print("Extracting package...")
        print("Please wait...")
        with tarfile.open(package_path) as tar:
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(tar, install_path)
        os.remove(package_path)

        print("\n")
        print("Installing...")
        print("Please wait...")
        os.symlink(f"{install_path}/dotnet",
                   f"{pathlib.Path.home()}/.local/bin/dotnet")

        print("\n")
        print("Testing dotnet binary...")
        print("Please wait...")
        test = shutil.which("dotnet")
        if test is None:
            print("dotnet binary not in PATH, adding...")
            path = "PATH=$PATH:~/.local/bin"
            with open(f"{pathlib.Path.home()}/.profile", "a") as f:
                f.write(f"export {path}")
            if os.environ["SHELL"] == "/bin/bash":
                with open(f"{pathlib.Path.home()}/.bashrc", "a") as f:
                    f.write(f"export {path}")
            elif os.environ["SHELL"] == "/bin/zsh":
                with open(f"{pathlib.Path.home()}/.zshrc", "a") as f:
                    f.write(f"export {path}")

        print("\n")
        print("Installation complete")
        print("Please restart your terminal")
        exit()

    def __download_progress(self, count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        bar = "■" * int(percent / 2) + "□" * (50 - int(percent / 2))
        sys.stdout.write(f"\r{bar} {percent}%")
        sys.stdout.flush()
        if percent == 100:
            sys.stdout.write("\n")
            sys.stdout.flush()

    def __get_package_url(self):
        url = f"{DOTNET_REPO_URL}{self.__selected_version.url}"
        with urllib.request.urlopen(url) as r:
            source = r.read().decode("utf-8")

            if self.__selected_package == "sdk":
                pattern = re.compile(
                    r"<table[^>]*aria-labelledby=\"download-release-sdk-[^\"]*\"[^>]*>(.*?)</table>", re.DOTALL)
                content = pattern.findall(source)[0]
                pattern = r"<a[^>]*href=\"/download/dotnet/thank-you/sdk-(.*?)-linux-x64-binaries*\"[^>]*>.*?</a>"
                url = re.compile(pattern).findall(content)[0]
                url = f"{DOTNET_REPO_URL}/download/dotnet/thank-you/sdk-{url}-linux-x64-binaries"

            elif self.__selected_package == "runtime":
                pattern = re.compile(
                    r"<table[^>]*aria-labelledby=\"download-release-runtime-desktop-[^\"]*\"[^>]*>(.*?)</table>", re.DOTALL)
                content = pattern.findall(source)[0]
                pattern = r"<a[^>]*href=\"/download/dotnet/thank-you/runtime-(.*?)-linux-x64-binaries*\"[^>]*>.*?</a>"
                url = re.compile(pattern).findall(content)[0]
                url = f"{DOTNET_REPO_URL}/download/dotnet/thank-you/runtime-{url}-linux-x64-binaries"

            with urllib.request.urlopen(url) as r:
                source = r.read().decode("utf-8")
                pattern = re.compile(
                    r"<a[^>]*id=\"directLink\"[^>]*href=\"(.*?)\"[^>]*>.*?</a>", re.DOTALL)
                direct_link = pattern.findall(source)[0]
                return direct_link

    @staticmethod
    def __fetch_versions():
        with urllib.request.urlopen(DOTNET_REPO_INDEX) as r:
            source = r.read().decode("utf8")
            pattern = re.compile(r"<table.*?>(.*?)</table>", re.DOTALL)
            content = pattern.findall(source)[0]

            pattern = re.compile(
                r"<a.*?href=\"(.*?)\".*?>(.*?)</a>", re.DOTALL)
            links = pattern.findall(content)

            for l in links:
                yield DotNetModel(l[1], l[0])

        return []

    @staticmethod
    def __menu_title(title):
        print("\n")
        print(f"\33[1m\33[30m{title}\033[0m")
        print("-" * len(title))

dn_manager = DotNetManager()
