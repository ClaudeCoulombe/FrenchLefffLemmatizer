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
                # print('pos_triplet',pos_triplet)
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
                    if a_triplet[self._POS] == 'nc':
                        if not "nc" in lefff_triplets_dict[a_triplet[self._INFLECTED_FORM]].keys():
                            lefff_triplets_dict[a_triplet[self._INFLECTED_FORM]][a_triplet[self._POS]] = a_triplet[self._LEMMA]
                        else:
                            lefff_triplets_dict[a_triplet[self._INFLECTED_FORM]][a_triplet[self._POS]+"_2"] = a_triplet[self._LEMMA]
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

    @staticmethod
    def show_lefff_dict(self, end):
        index = 0
        for element in self.LEFFF_TABLE:
            index += 1
            print(element)
            if index > end:
                break

    # Christopher P. Matthews
    # christophermatthews1985@gmail.com
    # Sacramento, CA, USA
    @staticmethod
    def edit_distance(s, t):
        ''' Also known as Levenshtein distance
            From Wikipedia article; Iterative with two matrix rows '''
        if s == t: return 0
        elif len(s) == 0: return len(t)
        elif len(t) == 0: return len(s)
        v0 = [None] * (len(t) + 1)
        v1 = [None] * (len(t) + 1)
        for i in range(len(v0)):
            v0[i] = i
        for i in range(len(s)):
            v1[0] = i + 1
            for j in range(len(t)):
                cost = 0 if s[i] == t[j] else 1
                v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)
            for j in range(len(v0)):
                v0[j] = v1[j]
        return v1[len(t)]

    # Linguistic heuristic to chose one best nc lemma
    def get_best_lemma(self, lemma_1,lemma_2,inflected_form):
        edit_distance_1 = self.edit_distance(inflected_form,lemma_1)
        edit_distance_2 = self.edit_distance(inflected_form,lemma_2)
        if (inflected_form[-1] == 's'):
            if edit_distance_1 == 1:
                return lemma_1
            elif edit_distance_2 == 1:
                return lemma_2
            else:
                if edit_distance_1 > edit_distance_2:
                    return lemma_1
                else:
                    return lemma_2            
        else:
            if edit_distance_1 < edit_distance_2:
                return lemma_1
            else:
                return lemma_2
    
    def standardize_lemma_pos_couples(self,lemmas_pos_couples):
        standard_lemmas_pos_couples = []
        for lemma,pos in lemmas_pos_couples:
            if pos == 'nc_2':
                pos = 'nc'
            standard_lemmas_pos_couples.append((lemma,pos))
        return standard_lemmas_pos_couples

    def lemmatize(self, word, pos="n"):
        raw_word = word
        if not (pos == self._POS_NP):
            word = word.lower()
        if word in self.LEFFF_TABLE:
            lemmas_pos_dict = self.LEFFF_TABLE[word]
            if self.TRACE:
                print("TRACE: ", lemmas_pos_dict)
        else:
            lemmas_pos_dict = {}
        pos_couples_list = []
        if self.is_wordnet_pos(pos):
            if lemmas_pos_dict:
                translated_pos_tag = self._WORDNET_LEFFF_DIC[pos]
                if translated_pos_tag in lemmas_pos_dict.keys():
                    if self.TRACE:
                        print("TRACE: ", pos, translated_pos_tag)
                    if translated_pos_tag == 'nc':
                        if 'nc_2' in lemmas_pos_dict.keys():
                            lemma_1 = lemmas_pos_dict['nc']
                            lemma_2 = lemmas_pos_dict['nc_2']
                            best_lemma = self.get_best_lemma(lemma_1,lemma_2,word)
                            return best_lemma
                        else:
                            return lemmas_pos_dict[translated_pos_tag]
                    else:
                        return lemmas_pos_dict[translated_pos_tag]
        else:
            if lemmas_pos_dict:
                if pos in lemmas_pos_dict.keys():
                    if pos == 'nc':
                        if 'nc_2' in lemmas_pos_dict.keys():
                            lemma_1 = lemmas_pos_dict['nc']
                            lemma_2 = lemmas_pos_dict['nc_2']
                            best_lemma = self.get_best_lemma(lemma_1,lemma_2,word)
                        else:
                            best_lemma = lemmas_pos_dict['nc']
                    else:
                        best_lemma = lemmas_pos_dict[pos]
                    return [(best_lemma, pos)]
                elif pos == 'all':
                    for lemma in lemmas_pos_dict.keys():
                        pos_couple = (lemmas_pos_dict[lemma], lemma)
                        pos_couples_list.append(pos_couple)
                    if raw_word[0].isupper():
                        pos_couples_list.append((raw_word, self._POS_NP))
                elif pos not in lemmas_pos_dict.keys():
                    return []                    
        if not pos_couples_list:
            if self.is_wordnet_pos(pos):
                return raw_word
            elif raw_word[0].isupper():
                if pos == 'all':
                    return [(raw_word, self._POS_NP)]
                else:
                    return raw_word, self._POS_NP
                return raw_word, self._POS_NP
        return self.standardize_lemma_pos_couples(pos_couples_list)

    @staticmethod
    def triplets_to_add(triplets_to_add):
        # Errors found in lefff-3.4.mlex :
        triplets_to_add.add(('résidente', 'nc', 'résident'))
        triplets_to_add.add(('résidente', 'nc', 'résidente'))
        triplets_to_add.add(('résidentes', 'nc', 'résident'))
        triplets_to_add.add(('résidentes', 'nc', 'résidente'))
        return triplets_to_add

    @staticmethod
    def triplets_to_remove(triplets_to_remove):
        triplets_to_remove.add(('chiens', 'nc', 'chiens'))
        #triplets_to_remove.add(('saisie', 'nc', 'saisi'))        
        #triplets_to_remove.add(('traductrice', 'nc', 'traductrice'))
        return triplets_to_remove
