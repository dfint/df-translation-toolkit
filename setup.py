from setuptools import setup, find_packages

setup(name='df_gettext_toolkit',
      version='0.1',
      # description='',
      url='http://bitbucket.org/dfint/df-gettext-toolkit',
      author='insolor',
      author_email='insolor@gmail.com',
      # license='MIT',
      packages=find_packages(),
      zip_safe=False, install_requires=['click'])
