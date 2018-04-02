from setuptools import setup

setup(name='FrenchLefffLemmatizer',
      version='0.1',
      description='French Lemmatizer based on LEFFF a large-scale morphological and syntactic lexicon for French',
      url='https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer',
      author='Claude Coulombe',
      author_email='claude.coulombe@gmail.com',
      license='Apache 2',
      packages=['french_lefff_lemmatizer'],
      package_data={
          'french_lefff_lemmatizer': ['data/lefff-3.4.mlex', 'data/lefff-3.4-addition.mlex']},
      zip_safe=False)
