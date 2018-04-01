from setuptools import setup

setup(name='FrenchLefffLemmatizer',
      version='0.1',
      description='French Lemmatizer based on LEFFF a large-scale morphological and syntactic lexicon for French',
      url='https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer',
      author='Claude Coulombe',
      author_email='claude.coulombe@gmail.com',
      license='Apache 2',
      packages=['lemmatizer', 'tests'],
      package_data={
        'data': ['lefff-3.4.mlex','lefff-3.4-addition.mlex']
      },
      zip_safe=False)

