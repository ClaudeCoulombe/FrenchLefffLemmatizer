from setuptools import setup

setup(name='FrenchLefffLemmatizer',
      version='0.1',
      description='French Lemmatizer based on LEFFF a large-scale morphological and syntactic lexicon for French',
      url='https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer',
      author='Claude Coulombe',
      author_email='claude.coulombe@gmail.com',
      license='Apache 2',
      packages=['FrenchLefffLemmatizer'],
      package_data={
      'FrenchLefffLemmatizer': ['lefff-3.4.mlex','lefff-3.4-addition.mlex','LICENCE','lefff-tagset-0.1.2.pdf']},
      zip_safe=False)

