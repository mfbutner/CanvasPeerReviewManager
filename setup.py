from setuptools import setup, find_packages

setup(
    name="Peer Reviewer",
    version="1.0",
    install_requires=["appdirs>=1.4.4",
                      "py2app",
                      "canvas-api>=0.1",
                      "canvasapi>=0.15.0",
                      "certifi>=2020.6",
                      "chardet>=3.0.4",
                      "distlib>=0.3.0",
                      "filelock>=3.0.12",
                      "methodtools>=0.1.2",
                      "Pillow>=7.1.2",
                      "Pillow-PIL>=0.1.dev0",
                      "virtualenv>=20.0.21",
                      "virtualenv-clone>=0.5.4",
                      "wirerope>=0.3.1"""],
    author="Alireza Havaei",
    author_email="ahavaeishamsabadi@ucdavis.edu",
    package_data={
        # If any package contains *.jpg files, include them:
        "": ["*.jpg"],
    },

    entry_points={
        "gui_scripts": [
            "peer-reviewer = peer_reviewer_program.rungui:run"],
        'console_scripts': ["peer-reviewer-terminal = peer_reviewer_program.runterminal:run"
                            ]
    },
    packages=find_packages(),
)
