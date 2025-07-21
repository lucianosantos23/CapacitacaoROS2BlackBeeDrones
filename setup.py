from setuptools import find_packages, setup
import os
from glob import glob

package_name = "meu_drone"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        ("share/" + package_name, ["package.xml"]),
        (
            os.path.join("share", package_name, "launch"),
            glob("launch/*.py"),
        ),  # <- adiciona os arquivos de launch
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="luciano23",
    maintainer_email="lucianoaraujodossantosfilho@gmail.com",
    description="TODO: Package description",
    license="TODO: License declaration",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "controle_drone = meu_drone.controle_drone:main",
            "posicao_drone = meu_drone.posicao_drone:main",
            "movimentacao = meu_drone.movimentacao:main",
            "obstaculo = meu_drone.obstaculo:main",
        ],
    },
)
