from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")
setup(name="walk_app",
      version="0.1",
      packages=[],
      url="https://github.com/froebbm/walk_app",
      license="MIT License",
      author="Brian Froeb",
      author_email="brian.froeb@gmail.com",
      description="walkability app",
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=[])