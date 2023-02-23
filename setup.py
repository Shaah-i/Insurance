from setuptools import find_packages, setup
from typing import List

requirement_file_name = "requirements.txt"
remove_package = "-e ."

def get_requirements()->List[str]:
    with open(requirement_file_name) as requirement_file:
        requirement_list = requirement_file.readline()
    # requirement_list = [requirement_name.replace("\n", "") for requirement_name in requirement_list]

    if remove_package in requirement_list:
        requirement_list.remove(remove_package)
    return requirement_list

setup(name= 'Insurance',
      version= '0.0.1',
      description= 'Insurance premium predictor',
      author= 'Shubham Shaah',
      author_email= 'shubbh9@gmail.com',
      packages= find_packages(),
      install_requires = get_requirements()
      )