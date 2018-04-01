from setuptools import setup

setup(name='FrenchLefffLemmatizer',
      version='0.2',
      description='French Lemmatizer based on LEFFF a large-scale morphological and syntactic lexicon for French',
      url='https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer',
      author='Claude Coulombe',
      author_email='claude.coulombe@gmail.com',
      license='Apache 2',
      packages=['FrenchLefffLemmatizer'],
      package_data={
        'data': ['lefff-3.4.mlex', 'lefff-3.4-addition.mlex']
      },
      include_package_data=True,
      zip_safe=False)

