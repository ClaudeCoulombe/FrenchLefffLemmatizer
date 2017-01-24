# -*- coding: utf-8 -*-
import random

class FrenchLefffLemmatizer(object):
    """
    Lefff Lemmatizer

    Lemmatize using Lefff's extension file .mlex
    
    Lefff (Lexique des Formes Fléchies du Français) under LGPL-LR (Lesser General Public License For Linguistic Resources).

    Sagot (2010). The Lefff, a freely available and large-coverage morphological and syntactic lexicon for French. In Proceedings of the 7th international conference on Language Resources and Evaluation (LREC 2010), Istanbul, Turkey
    
    Could be used with the same API than the WordNetLemmatizer included in the NLTK library
   
    Input: (word, pos_tag) where the pos_tag is among the set (a, r, n, v)
           To get all the original LEFFF pos tags use lemmatize(word,pos='all')
    Output: returns the lemma found in LEFFF or the input word unchanged if it cannot be found in LEFFF.
    
    """

    def __init__(self, lefff_file_path=None, lefff_additional_file_path=None):
        if lefff_file_path == None:
            lefff_file_path = "<path to>/lefff-3.4.mlex"
        if lefff_additional_file_path == None:
            lefff_additional_file_path = "<path to>/lefff-3.4.mlex/lefff-3.4-addition.mlex"
        self.LEFFF_FILE_STORAGE = lefff_file_path
        self.LEFFF_ADDITIONAL_DATA_FILE_STORAGE = lefff_additional_file_path
        self.INFLECTED_FORM = 0
        self.POS = 1
        self.LEMMA = 2
        self.MISC = 3
        self.OLD_LEMMA = 4 
        self.WORDNET_LEFFF_DIC = {'adj':'a','adv':'r','nc':'n','np':'n','v':'v','auxAvoir':'v','auxEtre':'v'}
        set_POS_triplets = set()
        with open(self.LEFFF_FILE_STORAGE, encoding='utf-8') as lefff_file:
            for a_line in lefff_file:
                a_line = a_line[:-1]
                line_parts = a_line.split('\t')
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
        for a_triplet in set_POS_triplets:
            if not a_triplet[self.INFLECTED_FORM] in lefff_triplets_dict:
                lefff_triplets_dict[a_triplet[self.INFLECTED_FORM]] = set()
                lefff_triplets_dict[a_triplet[self.INFLECTED_FORM]].add(a_triplet)
            else:
                lefff_triplets_dict[a_triplet[self.INFLECTED_FORM]].add(a_triplet)    
        # release the temporary set_POS_triples data structure
        # TODO: in order to save memory, combine set_POS_triples and lefff_triplets_dict 
        del set_POS_triplets
        self.LEFFF_TABLE = lefff_triplets_dict  
        
    def isWordnetAPI(self,pos):
        return pos in ['a','n','r','v']

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
            triplets_list = self.LEFFF_TABLE[word]
        else:
            triplets_list = []
        POS_couples_list = []
        if self.isWordnetAPI(pos):
            for triplet in triplets_list:
                if triplet[self.POS] in self.WORDNET_LEFFF_DIC.keys():
                    translated_POS_tag = self.WORDNET_LEFFF_DIC[triplet[self.POS]]
                    if translated_POS_tag == pos:
                        return triplet[self.LEMMA]
        else:
            for triplet in triplets_list:
                POS_couple = (triplet[self.LEMMA],triplet[self.POS])
                if (POS_couple not in POS_couples_list):
                    POS_couples_list.append(POS_couple)
        if (POS_couples_list == []):
            if self.isWordnetAPI(pos):
                return raw_word
            elif raw_word[0].isupper():
                POS_couples_list = (raw_word,'np')
        return POS_couples_list
