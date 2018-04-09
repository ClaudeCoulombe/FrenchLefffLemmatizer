# -*- coding: utf-8 -*-
import os
import random


class FrenchLefffLemmatizer(object):
    """
    Lefff Lemmatizer

    Lemmatize using Lefff's extension file .mlex
    
    Lefff (Lexique des Formes Fléchies du Français) under LGPL-LR (Lesser General Public License For Linguistic Resources).

    Sagot (2010). The Lefff, a freely available and large-coverage morphological and syntactic lexicon for French. In Proceedings of the 7th international conference on Language Resources and Evaluation (LREC 2010), Istanbul, Turkey
    
    Could be used with the same API than the WordNetLemmatizer included in the NLTK library
   
    Input: (word, pos_tag) where the pos_tag is among the set (a, r, n, v) for WordNet API
           or pos_tag in the set ('adj','adv','nc','np','ver','auxAvoir','auxEtre') for LEFFF API
           To get all the original LEFFF pos tags use lemmatize(word,pos='all')
    Output: returns the lemma found in LEFFF or the input word unchanged if it cannot be found in LEFFF.
    
    """

    _INFLECTED_FORM = 0
    _POS = 1
    _LEMMA = 2
    _MISC = 3
    _OLD_LEMMA = 4

    _WORDNET_LEFFF_DIC = {
        'a': 'adj',
        'r': 'adv',
        'n': 'nc',
        'v': 'v'
    }

    _POS_NP = 'np'

    def __init__(self, lefff_file_path=None, lefff_additional_file_path=None, *,
                 with_additional_file=None, load_only_pos=None):
        """
        :param with_additional_file: Allows to load LEFFF without the additional file. (Default: True)
        :type with_additional_file: bool
        :param load_only_pos: Allows to load LEFFF with only some pos tags: WordNet pos tags [a, r, n, v]. (Default: all)
        :type load_only_pos: list
        """
        data_file_path = os.path.dirname(os.path.realpath(__file__))
        if lefff_file_path is None:
            lefff_file_path = data_file_path + "/data/lefff-3.4.mlex"
        if lefff_additional_file_path is None:
            lefff_additional_file_path = data_file_path + "/data/lefff-3.4-addition.mlex"
        with_additional_file = True if with_additional_file is None else with_additional_file
        load_only_pos = self.filter_lefff_pos(load_only_pos) if load_only_pos is not None else None

        self.LEFFF_FILE_STORAGE = lefff_file_path
        self.LEFFF_ADDITIONAL_DATA_FILE_STORAGE = lefff_additional_file_path

        self.TRACE = False
        set_pos_triplets = set()
        with open(self.LEFFF_FILE_STORAGE, encoding='utf-8') as lefff_file:
            for a_line in lefff_file:
                line_parts = a_line[:-1].split('\t')
                pos_triplet = (line_parts[self._INFLECTED_FORM], line_parts[self._POS], line_parts[self._LEMMA])
                if pos_triplet not in set_pos_triplets:
                    set_pos_triplets.add(pos_triplet)
        set_pos_triplets_to_remove = set()
        set_pos_triplets_to_add = set()
        if with_additional_file:
            with open(self.LEFFF_ADDITIONAL_DATA_FILE_STORAGE, encoding='utf-8') as lefff_additional_data_file:
                for line_add in lefff_additional_data_file:
                    line_add_parts = line_add[:-1].split('\t')
                    new_pos_triplet = (
                        line_add_parts[self._INFLECTED_FORM],
                        line_add_parts[self._POS],
                        line_add_parts[self._LEMMA]
                    )
                    try:
                        old_pos_triplet = (
                            line_add_parts[self._INFLECTED_FORM],
                            line_add_parts[self._POS],
                            line_add_parts[self._OLD_LEMMA]
                        )
                    except IndexError as err:
                        raise IndexError("Error! %s\nLength %s\n%s" % (err, len(line_add_parts), line_add_parts))
                    set_pos_triplets_to_remove.add(old_pos_triplet)
                    set_pos_triplets_to_add.add(new_pos_triplet)

        # Errors found in lefff-3.4.mlex
        set_pos_triplets_to_remove = self.triplets_to_remove(set_pos_triplets_to_remove)
        set_pos_triplets_to_add = self.triplets_to_add(set_pos_triplets_to_add)
        set_pos_triplets = (set_pos_triplets - set_pos_triplets_to_remove) | set_pos_triplets_to_add

        # In order to improve the performance we create a dictionary to store the triplets tuples
        lefff_triplets_dict = dict()
        # a_triplet => a_triplet[self._INFLECTED_FORM], a_triplet[self._POS], a_triplet[self._LEMMA]
        for a_triplet in set_pos_triplets:
            if self.TRACE:
                print(a_triplet)
            if not load_only_pos or a_triplet[self._POS] in load_only_pos:
                if not a_triplet[self._INFLECTED_FORM] in lefff_triplets_dict:
                    lefff_triplets_dict[a_triplet[self._INFLECTED_FORM]] = dict()
                    lefff_triplets_dict[a_triplet[self._INFLECTED_FORM]][a_triplet[self._POS]] = a_triplet[self._LEMMA]
                else:
                    lefff_triplets_dict[a_triplet[self._INFLECTED_FORM]][a_triplet[self._POS]] = a_triplet[self._LEMMA]
                    # release the temporary set_POS_triples data structure
        # TODO: in order to save memory, combine set_POS_triples and lefff_triplets_dict 
        del set_pos_triplets
        self.LEFFF_TABLE = lefff_triplets_dict

    @staticmethod
    def is_wordnet_pos(pos):
        return pos in ['a', 'n', 'r', 'v']

    @staticmethod
    def is_lefff_pos(pos):
        return pos in ['adj', 'adv', 'nc', 'np', 'v', 'auxAvoir', 'auxEtre']

    def filter_lefff_pos(self, list_pos):
        """
        To prevent from giving incorrect POS tags.
        :return Set of LEFFF pos tags or None
        """
        return {self._WORDNET_LEFFF_DIC[pos] for pos in list_pos if self.is_wordnet_pos(pos)} or None

    def draw_random_sample(self, sample_size):
        leff_list = list(self.LEFFF_TABLE)
        return [self.LEFFF_TABLE[leff_list[i]] for i in random.sample(range(len(leff_list)), sample_size)]

    def show_lefff_dict(self, end):
        index = 0
        for element in self.LEFFF_TABLE:
            index += 1
            print(element)
            if index > end:
                break

    def lemmatize(self, word, pos="n"):
        raw_word = word
        if not (pos == self._POS_NP):
            word = word.lower()
        if word in self.LEFFF_TABLE:
            triplets_dict = self.LEFFF_TABLE[word]
            if self.TRACE:
                print("TRACE: ", triplets_dict)
        else:
            triplets_dict = []
        pos_couples_list = []
        if self.is_wordnet_pos(pos):
            if triplets_dict:
                translated_pos_tag = self._WORDNET_LEFFF_DIC[pos]
                if translated_pos_tag in triplets_dict:
                    if self.TRACE:
                        print("TRACE: ", pos, translated_pos_tag)
                    return triplets_dict[translated_pos_tag]
        else:
            if triplets_dict:
                if pos in triplets_dict:
                    return [(triplets_dict[pos], pos)]
                elif pos == 'all' or pos not in triplets_dict:
                    for key in triplets_dict:
                        pos_couple = (triplets_dict[key], key)
                        pos_couples_list.append(pos_couple)
                    if raw_word[0].isupper():
                        pos_couples_list.append((raw_word, self._POS_NP))
        if not pos_couples_list:
            if self.is_wordnet_pos(pos):
                return raw_word
            elif raw_word[0].isupper():
                return raw_word, self._POS_NP
        return pos_couples_list

    @staticmethod
    def triplets_to_add(triplets_to_add):
        # Errors found in lefff-3.4.mlex :
        triplets_to_add.add(('résidente', 'nc', 'résident'))
        triplets_to_add.add(('résidentes', 'nc', 'résident'))
        return triplets_to_add

    @staticmethod
    def triplets_to_remove(triplets_to_remove):
        triplets_to_remove.add(('chiens', 'nc', 'chiens'))
        triplets_to_remove.add(('traductrice', 'nc', 'traductrice'))
        return triplets_to_remove
