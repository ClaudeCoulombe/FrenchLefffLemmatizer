import os
import unittest

from lemmatizer.french_lefff_lemmatizer import FrenchLefffLemmatizer


class TestFrenchLefffLemmatizer(unittest.TestCase):
    path_file = 'path_to_file'

    def setUp(self):
        open(self.path_file, "w").close()

    def tearDown(self):
        if os.path.exists(self.path_file):
            os.remove(self.path_file)

    def test_french_lefff_lemmatizer_when_lefff_files_are_empty_expect_empty_table(self):
        lemmatizer = FrenchLefffLemmatizer(lefff_file_path=self.path_file, lefff_additional_file_path=self.path_file)
        self.assertEqual(2,  # Corresponds to the triplets to add
                         len(lemmatizer.LEFFF_TABLE))

    def test_french_lefff_lemmatizer_when_load_only_lefff_additional(self):
        lemmatizer = FrenchLefffLemmatizer(lefff_file_path=self.path_file)
        self.assertEqual(56843, len(lemmatizer.LEFFF_TABLE))

    def test_french_lefff_lemmatizer_when_lefff_additional_file_path_is_not_none_and_empty_expect_only_lefff_file(self):
        lemmatizer = FrenchLefffLemmatizer(lefff_additional_file_path=self.path_file)
        self.assertEqual(455787, len(lemmatizer.LEFFF_TABLE))

    def test_french_lefff_lemmatizer_lexicon_data_length(self):
        lemmatizer = FrenchLefffLemmatizer()
        self.assertEqual(455789, len(lemmatizer.LEFFF_TABLE))


class TestIsWordnetApi(unittest.TestCase):
    def setUp(self):
        # To make the test faster, we load an empty file.
        self.lemmatizer = FrenchLefffLemmatizer(open('file.txt', 'w').close())

    def tearDown(self):
        if os.path.exists('file.txt'):
            os.remove('file.txt')

    def test_is_wordnet_api_when_pos_expect_true(self):
        self.assertTrue(self.lemmatizer.is_wordnet_pos('a'))
        self.assertTrue(self.lemmatizer.is_wordnet_pos('n'))
        self.assertTrue(self.lemmatizer.is_wordnet_pos('r'))
        self.assertTrue(self.lemmatizer.is_wordnet_pos('v'))

    def test_is_wordnet_api_when_not_pos_expect_false(self):
        self.assertFalse(self.lemmatizer.is_wordnet_pos('adj'))


class TestLemmatize(unittest.TestCase):
    lemmatizer = FrenchLefffLemmatizer()

    def test_lemmatize_when_pos_default_expect_correct_lemmatized_word(self):
        self.assertEqual('voiture', self.lemmatizer.lemmatize('voitures'))

    def test_lemmatize_when_pos_n_expect_correct_lemmatized_word(self):
        self.assertEqual('abbaye', self.lemmatizer.lemmatize('abbayes', pos='n'))

    def test_lemmatize_when_pos_np_expect_correct_couple(self):
        self.assertEqual([('Nantes', 'np')],
                         self.lemmatizer.lemmatize('Nantes', pos='np'))

    def test_lemmatize_when_pos_does_not_correspond_expect_raw_word(self):
        self.assertEqual('Nantes', self.lemmatizer.lemmatize('Nantes', pos='n'))

    def test_lemmatize_when_pos_does_not_exist_expect_correct_couple(self):
        self.assertEqual(('Nantes', 'np'), self.lemmatizer.lemmatize('Nantes', pos='x'))

    def test_lemmatize_when_word_does_not_exists_expect_raw_word(self):
        self.assertEqual('bliblis', self.lemmatizer.lemmatize('bliblis'))

    def test_lemmatize_when_word_and_pos_do_not_exist_expect_empty_list(self):
        self.assertEqual(list(), self.lemmatizer.lemmatize('bliblis', pos='x'))

    def test_lemmatize_when_pos_a_expect_correct_lemmatized_word(self):
        self.assertEqual('court', self.lemmatizer.lemmatize('courtes', pos='a'))

    def test_lemmatize_when_pos_r_expect_correct_lemmatized_word(self):
        self.assertEqual('dernièrement', self.lemmatizer.lemmatize('dernièrement', pos='r'))

    def test_lemmatize_when_pos_v_expect_correct_lemmatized_word(self):
        self.assertEqual('manger', self.lemmatizer.lemmatize('manges', pos='v'))

    def test_lemmatize_when_uncorrect_pos_expect_list_of_couples(self):
        expected_result = set(x for x in [('voiture', 'nc'), ('voiturer', 'v')])
        self.assertEqual(expected_result,
                         set(self.lemmatizer.lemmatize('voitures', pos='x')))


class TestUpdateLefffLexicon(unittest.TestCase):
    def setUp(self):
        self.path_file = 'path_to_file'
        with open(self.path_file, "w") as f:
            f.write("avoir	v	avoir")  # triplet with no old lemma

    def tearDown(self):
        if os.path.exists(self.path_file):
            os.remove(self.path_file)

    def test_update_lefff_lexicon_when_no_old_lemma_expect_exception(self):
        with self.assertRaises(IndexError):
            FrenchLefffLemmatizer(lefff_additional_file_path=self.path_file).update_lefff_lexicon()
