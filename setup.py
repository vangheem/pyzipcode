from setuptools import setup, find_packages

setup(
    name="pyzipcode",
    version=open("VERSION").read().strip(),
    description="query zip codes and location data",
    long_description=open("README.md").read() + "\n\n" + open("CHANGES.md").read(),
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="zip code distance",
    author="Nathan Van Gheem",
    author_email="vangheem@gmail.com",
    url="https://github.com/vangheem/pyzipcode",
    license="MIT",
    packages=find_packages(exclude=["ez_setup", "examples", "tests"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
    python_requires='>=3.6',
    entry_points="""
      # -*- Entry points: -*-
      """,
)
