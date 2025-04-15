from setuptools import setup, find_packages

setup(
    name="wazuh-sdk",
    version="0.1.0",
    description="A flexible Python SDK for interacting with the Wazuh API (currently supporting 4 version 4).",
    author="Moad Ennagi",
    author_email="moad.ennagi@gmail.com",
    url="https://github.com/moadennagi/wazuh-api-sdk",
    packages=find_packages(),
    install_requires=[
        "requests>=2.20.0",
        "httpx==0.28.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
