from setuptools import find_packages,setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='IBL',
    url='https://github.com/snayeri/Portfolio_Management/Idzorek_Black_Litterman',
    author='Siamak Nayeri',
    author_email='siamaknayeri@gmail.com',
    # Needed to actually package something
    packages=find_packages(),
    description='personal take on Idzorek Black Litterman'
