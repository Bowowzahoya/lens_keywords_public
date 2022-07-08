from setuptools import setup, find_packages

setup(
    name='lens_keywords',
    packages=["lens_keywords"],
    package_dir={"":"src"},
    url='https://github.com/Bowowzahoya/lens_keywords',
    description='Analysis of keywords in Lens exports',
    long_description=open('README.md', encoding="utf-8").read(),
    install_requires=[
        "pandas",
        "whoosh",
        ],
    include_package_data=True,
)