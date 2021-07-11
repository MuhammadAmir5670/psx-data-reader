from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="psx-data-reader",                      # This is the name of the package
    version="0.0.1",                             # The initial release version
    license='MIT',                               # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description="Pakistan Stock Exchange's Data Downloader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Muhammad Amir Abbasi",               # Full name of the author
    author_email = 'muhammadamir5670@gmail.com', # Type in your E-Mail
    url = 'https://github.com/MuhammadAmir5670/psx-data-reader',   # Provide either the link to your github or to your website
    download_url = 'https://github.com/MuhammadAmir5670/psx-data-reader/archive/refs/tags/0.0.1.tar.gz',    # I explain this later on
    keywords = ['psx', 'Pakistan stock exchange', 'stocks data downloader', 'Pakistan stock exchange data'],   # Keywords that define your package best


    classifiers=[                                # Information to filter the project on PyPi website
        'Development Status :: 3 - Alpha',                  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',                  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',           # Again, pick a license
        'Programming Language :: Python :: 3',              # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        "Operating System :: OS Independent",
    ],                                      

    python_requires='>=3',                       # Minimum version requirement of the package
    packages=find_packages(),         # List of all python modules to be installed
    package_dir={'': 'src'},                     # Directory of the source code of the package
    install_requires=[                           # Install other dependencies if any
        "pandas", 
        "tqdm", 
        "beautifulsoup4",
        "requests"
    ],
)