from setuptools import setup, find_packages

requirements = [
      'typer',
      'unidecode',
      'df-raw-decoder @ https://github.com/dfint/df_raw_decoder/archive/master.zip'
]

setup(name='df_gettext_toolkit',
      version='0.1.1',
      # description='',
      url='https://github.com/dfint/df-gettext-toolkit',
      author='insolor',
      author_email='insolor@gmail.com',
      license='MIT',
      packages=find_packages(),
      zip_safe=False,
      install_requires=requirements)
