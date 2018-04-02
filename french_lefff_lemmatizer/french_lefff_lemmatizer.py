# -*- coding: utf-8 -*-
import os
import random

from enum import Enum


class WordCharacteristic(Enum):
    INFLECTED_FORM = 0
    POS = 1
    LEMMA = 2
    MISC = 3
    OLD_LEMMA = 4


class PartOfSpeech(Enum):
    ADJ = 'a'
    ADJ_SAT = 's'
    ADV = 'r'
    NOUN = 'n'
    VERB = 'v'


class FrenchLefffLemmatizer(object):
    """
    Lefff Lemmatizer. Lemmatize using Lefff's extension file .mlex.
    Lefff (Lexique des Formes Fléchies du FranÃ§ais) under LGPL-LR  (Lesser General Public License For Linguistic
        Resources).
    Sagot (2010). The Lefff, a freely available and large-coverage morphological and syntactic lexicon for French.
    In Proceedings of the 7th international conference on Language Resources and Evaluation (LREC 2010),
        Istanbul, Turkey.

    Could be used with the same API than the WordNetLemmatizer included in the NLTK library.

    Input: (word, pos_tag) where the pos_tag is among the set (a, r, n, v)
           To get all the original LEFFF pos tags use lemmatize(word,pos='all')
    Output: returns the lemma found in LEFFF or the input word unchanged if it cannot be found in LEFFF.
    """

    _LEFFF_WORDNET_POS_CORRESPONDENCES = {
        'adj': PartOfSpeech.ADJ.value,
        'adv': PartOfSpeech.ADV.value,
        'nc': PartOfSpeech.NOUN.value,
        'np': PartOfSpeech.NOUN.value,
        'v': PartOfSpeech.VERB.value,
        'auxAvoir': PartOfSpeech.VERB.value,
        'auxEtre': PartOfSpeech.VERB.value
    }

    _POS_NP = 'np'

    def __init__(self, lefff_file_path=None, lefff_additional_file_path=None):
        # TODO: make loading of additional file optional
        # TODO: allow to load lefff with only chosen pos tag
        base_dir = os.path.dirname(os.path.dirname(__file__))
        if lefff_file_path is None:
            lefff_file_path = os.path.join(base_dir, "french_lefff_lemmatizer", "data", "lefff-3.4.mlex")
        if lefff_additional_file_path is None:
            lefff_additional_file_path = os.path.join(base_dir, "french_lefff_lemmatizer", "data", "lefff-3.4-addition.mlex")

        self.LEFFF_DATA_FILE = lefff_file_path
        self.LEFFF_ADDITIONAL_DATA_FILE = lefff_additional_file_path

        self.LEFFF_TABLE = dict()
        # {
        #  "chaises": {"n": "chaise"},
        #  "courtes": {"a": "court"}
        # }
        with open(self.LEFFF_DATA_FILE, encoding='utf-8') as lefff_data_file:
            for a_line in lefff_data_file:
                line_parts = a_line[:-1].split('\t')
                a_triplet = (line_parts[WordCharacteristic.INFLECTED_FORM.value],
                             line_parts[WordCharacteristic.POS.value],
                             line_parts[WordCharacteristic.LEMMA.value])
                self.add_triplet_to_dict(a_triplet)

        # Add forgotten triplets.
        for a_triplet in self.triplet_to_add():
            self.add_triplet_to_dict(a_triplet)

        if self.LEFFF_ADDITIONAL_DATA_FILE:
            self.update_lefff_lexicon()

    @staticmethod
    def is_wordnet_pos(pos):
        return pos in ['a', 'n', 'r', 'v']

    def draw_random_sample(self, sample_size):
        leff_list = list(self.LEFFF_TABLE)
        return [self.LEFFF_TABLE[leff_list[i]] for i in random.sample(range(len(leff_list)), sample_size)]

    def show_lefff_dict(self, end):
        for index, element in enumerate(self.LEFFF_TABLE):
            if index < end:
                print(element)

    def lemmatize(self, word, *, pos=PartOfSpeech.NOUN.value):
        raw_word = word
        word = word.lower() if not (pos == FrenchLefffLemmatizer._POS_NP) else word
        triplets_list = self.LEFFF_TABLE[word] if word in self.LEFFF_TABLE else list()  # a dict
        pos_couples_list = list()

        if self.is_wordnet_pos(pos):
            for triplet in triplets_list:
                if triplet in \
                        FrenchLefffLemmatizer._LEFFF_WORDNET_POS_CORRESPONDENCES:
                    translated_pos_tag = \
                        FrenchLefffLemmatizer._LEFFF_WORDNET_POS_CORRESPONDENCES[triplet]
                    if translated_pos_tag == pos:
                        return triplets_list[triplet]
        else:
            for triplet in triplets_list:
                pos_couple = (triplets_list[triplet], triplet)
                if pos_couple not in pos_couples_list:
                    pos_couples_list.append(pos_couple)
        if not pos_couples_list:  # empty list
            if self.is_wordnet_pos(pos):
                return raw_word
            elif raw_word[0].isupper():
                pos_couples_list = (raw_word, FrenchLefffLemmatizer._POS_NP)
        return pos_couples_list

    def add_triplet_to_dict(self, a_triplet):
        if not a_triplet[WordCharacteristic.INFLECTED_FORM.value] in self.LEFFF_TABLE \
                and a_triplet not in self.triplets_to_remove():
            self.LEFFF_TABLE[a_triplet[WordCharacteristic.INFLECTED_FORM.value]] = {a_triplet[WordCharacteristic.POS.value]:
                                                                                    a_triplet[WordCharacteristic.LEMMA.value]}
        else:
            self.LEFFF_TABLE[a_triplet[WordCharacteristic.INFLECTED_FORM.value]][a_triplet[WordCharacteristic.POS.value]] = a_triplet[WordCharacteristic.LEMMA.value]

    def update_lefff_lexicon(self):
        """
        Updates lexicon according to additional data.
        :return: Updated triplets dictionary.
        """
        with open(self.LEFFF_ADDITIONAL_DATA_FILE, encoding='utf-8') as file:
            for a_line in file:
                line_parts = a_line[:-1].split('\t')
                try:
                    old_pos_triplet = (line_parts[WordCharacteristic.INFLECTED_FORM.value],
                                       line_parts[WordCharacteristic.POS.value],
                                       line_parts[WordCharacteristic.OLD_LEMMA.value])
                    if old_pos_triplet[WordCharacteristic.INFLECTED_FORM.value] in self.LEFFF_TABLE and \
                       old_pos_triplet in self.LEFFF_TABLE[old_pos_triplet[WordCharacteristic.INFLECTED_FORM.value]]:
                        self.LEFFF_TABLE[old_pos_triplet[WordCharacteristic.INFLECTED_FORM.value]].remove(old_pos_triplet)
                except IndexError as err:
                    raise IndexError("Error! %s\nLength %s\n%s" % (err, len(line_parts), line_parts))

                new_pos_triplet = (line_parts[WordCharacteristic.INFLECTED_FORM.value],
                                   line_parts[WordCharacteristic.POS.value],
                                   line_parts[WordCharacteristic.LEMMA.value])
                self.add_triplet_to_dict(new_pos_triplet)

    @staticmethod
    def triplets_to_remove():
        # Errors found in lefff-3.4.mlex : triplets to remove
        return {
            ('chiens', 'nc', 'chiens'),
            ('traductrice', 'nc', 'traductrice')
        }

    @staticmethod
    def triplet_to_add():
        # Errors found in lefff-3.4.mlex : triplets to add
        return {
            ('résidente', 'nc', 'résident'),
            ('résidentes', 'nc', 'résident')
        }
