
<strong>Introduction</strong>

A French Lemmatizer in Python based on the LEFFF (Lexique des Formes Fléchies du Français / Lexicon of French inflected forms) is a large-scale morphological and syntactic lexicon for French.

<strong>Main reference:</strong>

[Sagot,2010] Sagot, B. (2010). The Lefff, a freely available and large-coverage morphological and syntactic lexicon for French. In 7th international conference on Language Resources and Evaluation (LREC 2010). Retrieved from https://hal.archives-ouvertes.fr/file/index/docid/521242/filename/lrec10lefff.pdf

Benoît Sagot Webpage about LEFFF<br/>
http://alpage.inria.fr/~sagot/lefff-en.html<br/>

More precisely, we use the morphological lexicon only: .mlex file) which has a simple format in CSV (4 fields separated by '\ t')

<a href="https://gforge.inria.fr/frs/download.php/file/34601/lefff-3.4.mlex.tgz">LEFFF download hyperlink</a>

Tagset format FRMG - from the ALPAGE project since 2004<br/>
<a href="http://alpage.inria.fr/frmgwiki/content/tagset-frmg">Tagset</a>

<strong>License</strong>

Copyright (C) 2017-2018 Claude COULOMBE

Licensed under the Apache License, Version 2.0 (the 'License');
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

<a href="http://www.apache.org/licenses/LICENSE-2.0">Apache 2.0 License</a>

-----

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an 'AS IS' BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-----
Warning: Run under Python 3.X but could run with small modifs with Python 2.7X
-----
Installation:

1) Make sure pip is installed (https://packaging.python.org/tutorials/installing-packages/)<br/>
2) Then you can install FrenchLefffLemmatizer:<br/>
`> pip install git+https://github.com/ClaudeCoulombe/FrenchLefffLemmatizer.git`

-----

Small examples:

``` Python
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
french_lemmatizer = FrenchLefffLemmatizer()
print(french_lemmatizer.lemmatize('avions'))
avion
french_lemmatizer.lemmatize('avions','n')
avion
french_lemmatizer.lemmatize('avions','v')
avoir
french_lemmatizer.lemmatize('avions','all')
[('avion', 'nc'), ('avoir', 'auxAvoir'), ('avoir', 'ver')]
french_lemmatizer.lemmatize('vous','all')
[('se', 'clr'), ('le', 'cla'), ('lui', 'pro'), ('il', 'cln'), ('lui', 'cld')]
french_lemmatizer.lemmatize('la','all')
[('la', 'nc'), ('le', 'det'), ('le', 'cla')]
```

Additional examples:

``` Python
from french_lefff_lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer
french_lemmatizer = FrenchLefffLemmatizer(with_additional_file=False, load_only_pos=['nc', 'adj'])
print(french_lemmatizer.lemmatize('avions'))
avion
french_lemmatizer.lemmatize('avions','n')
avion
french_lemmatizer.lemmatize('avions','all')
[('avion', 'nc')]
```

