from sys import executable

from cx_Freeze import setup, Executable

executables = [Executable("main.py")]

setup(
    name="FlowerGirl",
    version="1.0",
    description="Flower Girl App",
    options={"build.exe": {"packages": ["pygame", "json"]}},
    executables=executables
)

