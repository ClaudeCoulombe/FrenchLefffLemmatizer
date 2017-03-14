# -*- coding: utf-8 -*-
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

    def __init__(self, lefff_file_path=None, lefff_additional_file_path=None):
        if lefff_file_path == None:
            lefff_file_path = "<path_to_LEFFF_file>/lefff-3.4.mlex"
        if lefff_additional_file_path == None:
            lefff_additional_file_path = "<path_to_additional_LEFFF_file>/lefff-3.4-addition.mlex"
        self.LEFFF_FILE_STORAGE = lefff_file_path
        self.LEFFF_ADDITIONAL_DATA_FILE_STORAGE = lefff_additional_file_path
        self.INFLECTED_FORM = 0
        self.POS = 1
        self.LEMMA = 2
        self.MISC = 3
        self.OLD_LEMMA = 4 
        self.TRACE = False
        self.WORDNET_LEFFF_DIC = {'a':'adj','r':'adv','n':'nc','v':'ver'}
        set_POS_triplets = set()
        with open(self.LEFFF_FILE_STORAGE, encoding='utf-8') as lefff_file:
            for a_line in lefff_file:
                a_line = a_line[:-1]
                line_parts = a_line.split('\t')
                if line_parts[self.POS] == 'v':
                    line_parts[self.POS] = 'ver'
                POS_triplet = (line_parts[self.INFLECTED_FORM],line_parts[self.POS],line_parts[self.LEMMA])
                if (POS_triplet not in set_POS_triplets):
                    set_POS_triplets.add(POS_triplet)
        set_POS_triplets_to_remove = set()
        set_POS_triplets_to_add = set()
        index_output = 1
        with open(self.LEFFF_ADDITIONAL_DATA_FILE_STORAGE, encoding='utf-8') as lefff_additional_data_file:
            for line_add in lefff_additional_data_file:
                line_add = line_add[:-1]
                line_add_parts = line_add.split('\t')
                new_POS_triplet = (line_add_parts[self.INFLECTED_FORM],line_add_parts[self.POS],line_add_parts[self.LEMMA])
                try:
                    old_POS_triplet = (line_add_parts[self.INFLECTED_FORM],line_add_parts[self.POS],line_add_parts[self.OLD_LEMMA])
                except IndexError as err:
                        print("Error! ",err)
                        print("Length",len(line_add_parts))
                        print(self.INFLECTED_FORM,self.OLD_LEMMA)
                        print(line_add_parts[self.INFLECTED_FORM])
                set_POS_triplets_to_remove.add(old_POS_triplet)
                set_POS_triplets_to_add.add(new_POS_triplet)
        # Errors found in lefff-3.4.mlex
        set_POS_triplets_to_remove.add(('chiens','nc','chiens'))
        set_POS_triplets_to_add.add(('résidente','nc','résident'))
        set_POS_triplets_to_add.add(('résidentes','nc','résident'))
        set_POS_triplets_to_remove.add(('traductrice','nc','traductrice'))
        set_POS_triplets = (set_POS_triplets - set_POS_triplets_to_remove) | set_POS_triplets_to_add                
        # In order to improve the performance we create
        # a dictionary to store the triplets tuples
        lefff_triplets_dict = dict()
        # a_triplet => a_triplet[self.INFLECTED_FORM], a_triplet[self.POS], a_triplet[self.LEMMA]
        for a_triplet in set_POS_triplets:
            if self.TRACE:
                print(a_triplet)
            if not a_triplet[self.INFLECTED_FORM] in lefff_triplets_dict:
                lefff_triplets_dict[a_triplet[self.INFLECTED_FORM]] = dict()
                lefff_triplets_dict[a_triplet[self.INFLECTED_FORM]][a_triplet[self.POS]] = a_triplet[self.LEMMA] 
            else:
                lefff_triplets_dict[a_triplet[self.INFLECTED_FORM]][a_triplet[self.POS]] = a_triplet[self.LEMMA]   
        # release the temporary set_POS_triples data structure
        # TODO: in order to save memory, combine set_POS_triples and lefff_triplets_dict 
        del set_POS_triplets
        self.LEFFF_TABLE = lefff_triplets_dict  
        
    def isWordnetAPI(self,pos):
        return pos in ['a','n','r','v']

    def isLEFFFAPI(self,pos):
        return pos in ['adj','adv','nc','np','ver','auxAvoir','auxEtre']

    def drawRandomSample(self,sample_size):
        leff_list = list(self.LEFFF_TABLE)
        return [self.LEFFF_TABLE[leff_list[i]] for i in random.sample(range(len(leff_list)), sample_size)]
        
    def showLeffDict(self,end):
        index = 0
        for element in self.LEFF_DICT:
            index += 1
            print(element)
            if index > end:
                break
                
    def lemmatize(self,word,pos="n"):
        raw_word = word
        if ( not (pos == "np") ):
            word = word.lower()
        if word in self.LEFFF_TABLE.keys():
            triplets_dict = self.LEFFF_TABLE[word]
            if self.TRACE:
                print("TRACE: ",triplets_dict)
        else:
            triplets_dict = []
        POS_couples_list = []
        if self.isWordnetAPI(pos):
            if not triplets_dict == []:
                    translated_pos_tag = self.WORDNET_LEFFF_DIC[pos]
                    if translated_pos_tag in triplets_dict.keys():
                        if self.TRACE:
                            print("TRACE: ",pos, translated_pos_tag)
                        return triplets_dict[translated_pos_tag]
        else:
            if not triplets_dict == []:
                if pos in triplets_dict.keys():
                    return [(triplets_dict[pos],pos)]
                elif pos == 'all':
                    for key in triplets_dict.keys():
                        POS_couple = (triplets_dict[key],key)
                        POS_couples_list.append(POS_couple)
                    if raw_word[0].isupper():
                        POS_couples_list.append((raw_word,'np'))
        if (POS_couples_list == []):
            if self.isWordnetAPI(pos):
                return raw_word
            elif raw_word[0].isupper():
                return [(raw_word,'np')]
        return POS_couples_list