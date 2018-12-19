from setuptools import setup

install_requires = [
    'ebaysdk==2.1.5'
]

setup(name='eprices',
      version='1.0.5',
      description='Display sold and available auctions',
      author='Alan So',
      author_email='alansoandso@gmail.com',
      scripts=['eprices', 'prices.py'],
      install_requires=install_requires
      )
