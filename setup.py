from setuptools import find_packages,setup
import fnmatch
import os
from collections import defaultdict

package_data = defaultdict(list)
filetypes = ["*.csv", "*.csv.gz"]
for root, _, filenames in os.walk(os.path.join(os.getcwd(), "IBL")):  
    matches = []
    for filetype in filetypes:
        for filename in fnmatch.filter(filenames, filetype):
            matches.append(filename)
    if matches:
        package_data[".".join(os.path.relpath(root).split(os.path.sep))] = filetypes
package_data["IBL"].append("py.typed")

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='IBL',
    url='https://github.com/snayeri/IBL',
    author='Siamak Nayeri',
    author_email='siamaknayeri@gmail.com',
    # Needed to actually package something
    packages=find_packages(),
    package_dir={"IBL": "./IBL"},
    zip_safe=False,
    include_package_data=False,
    package_data=package_data,
    # Needed for dependencies
    install_requires=['numpy', 'pandas', 'pandas_datareader', 'scipy'],
    # *strongly* suggested for sharing
    version='0.1',
     # The license can be anything you like
    license='Liam_Nayeri',
    description='personal take on Idzorek Black Litterman', 
)
