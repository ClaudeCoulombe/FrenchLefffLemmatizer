from setuptools import setup

setup(name='FrenchLefffLemmatizer',
      version='0.2',
      description='French Lemmatizer based on LEFFF a large-scale morphological and syntactic lexicon for French',
      keywords='french lefff lemmatizer lexicon',
      url='https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer',
      author='Claude Coulombe',
      author_email='claude.coulombe@gmail.com',
      license='Apache 2',
      packages=['french_lefff_lemmatizer'],
      package_data={'french_lefff_lemmatizer': ['data/*.mlex']},
      include_package_data=True,
      zip_safe=False)

