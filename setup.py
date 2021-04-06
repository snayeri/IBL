from setuptools import find_packages,setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='IBL',
    url='https://github.com/snayeri/Idzorek_Black_Litterman',
    author='Siamak Nayeri',
    author_email='siamaknayeri@gmail.com',
    # Needed to actually package something
    packages=['IBL'],
    # Needed for dependencies
    install_requires=['numpy', 'pandas', 'pandas_datareader', 'scipy.optimize'],
    # *strongly* suggested for sharing
    version='0.1',
     # The license can be anything you like
    license='Liam_Nayeri',
    description='personal take on Idzorek Black Litterman'
