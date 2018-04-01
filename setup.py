from setuptools import setup

setup(name='FrenchLefffLemmatizer',
      version='0.2',
      description='French Lemmatizer based on LEFFF a large-scale morphological and syntactic lexicon for French',
      url='https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer',
      author='Claude Coulombe',
      author_email='claude.coulombe@gmail.com',
      license='Apache 2',
      packages=['french_lefff_lemmatizer'],
      data_files=[('data', ['data/*.mlex'])],
      include_package_data=True,
      zip_safe=False)

