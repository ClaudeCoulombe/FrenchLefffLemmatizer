# Creation of an Additional Lefff Data File firstly in memory then saved on disk
# usage
# INPUT_FILE_PATH = ""<path_to_LEFFF_file>/lefff-3.4.mlex""
# OUTPUT_FILE_PATH = "<path_to_additional_LEFFF_file>/lefff-3.4-addition.mlex"
# create_additional_lefff_datafile(INPUT_FILE_PATH,OUTPUT_FILE_PATH)

import re

TRACE = False


def print_carac_on_the_same_line(index_output=1, carac='.', line_length=100):
    i = index_output
    if i == line_length:
        print(carac)
        return 1
    else:
        print(carac, end='')
        return i + 1


# find inflected_form with POS equals adj and suffix is «r» or «re»
# dict => { "inflected_form_POS":[inflected_form,POS,old_lemma,misc],...}
# ([^\d\s]*)\tadj\t([^\d\s]*[r]+)\t[^\d\s]*|([^\d\s]*)\tadj\t([^\d\s]*re+)\t[^\d\s]*

inflected_i = 0
pos_i = 1
lemma_i = 2
misc_i = 3
old_lemma_i = 4


def extract_inflected_from_key(a_key, dict_lefff):
    return dict_lefff[a_key][inflected_i]


def extract_pos_from_key(a_key, dict_lefff):
    return dict_lefff[a_key][pos_i]


def extract_lemma_from_key(a_key, dict_lefff):
    return dict_lefff[a_key][lemma_i]


def extract_misc_from_key(a_key, dict_lefff):
    return dict_lefff[a_key][misc_i]


def extract_old_lemma_from_key(a_key, dict_lefff):
    return dict_lefff[a_key][old_lemma_i]


def create_verbal_key(a_key, dict_lefff):
    return extract_lemma_from_key(a_key, dict_lefff) + "_v_" + extract_misc_from_key(a_key, dict_lefff)


def is_verb_inf_lemma_for_adj(dict_key, dict_lefff):
    current_pos = extract_pos_from_key(dict_key, dict_lefff)
    if TRACE:
        print(current_pos)
    if not current_pos == 'adj':
        if TRACE:
            print('Should be an adj:', current_pos)
        return False
    else:
        verbal_key = create_verbal_key(dict_key, dict_lefff)
        if TRACE:
            print(verbal_key)
        if verbal_key in dict_lefff.keys():
            return dict_lefff[verbal_key][lemma_i] == dict_lefff[dict_key][lemma_i]
        else:
            if TRACE:
                print('Should be an infinitive verb:', verbal_key)
            return False


def find_lemma_adj_masc_sing(dict_key, dict_lefff):
    lemmatized_form = extract_lemma_from_key(dict_key, dict_lefff)
    new_key = lemmatized_form + "_adj_Kms"
    if new_key in dict_lefff.keys():
        if TRACE:
            print('new_key:', new_key, 'inflected_i:', inflected_i)
            print(dict_lefff[new_key])
        return dict_lefff[new_key][inflected_i]
    return "not found"


INPUT_FILE_PATH = "/Users/claudecoulombe/git/semantron/notebooks/lefff-3.4.mlex/lefff-3.4.mlex"

clitic_pronouns = ["-elle", "-elles", "-en", "-il", "-ils", "-je", "-la", "-le", "-les",
                   "-leur", "-lui", "-m'", "-moi", "-nous", "-on", "-t'", "-t-elle", "-t-elles",
                   "-t-en", "-t-il", "-t-ils", "-t-on", "-t-y", "-toi", "-tu", "-vous", "-vs",
                   "-y", "_error", "ch'", "elle", "elles", "en", "il", "ils", "j'", "je", "l'",
                   "l'on", "la", "le", "les", "leur", "lui", "m'", "me", "moi", "nous", "on",
                   "s'", "se", "t'", "te", "toi", "tu", "vous", "vs", "y"]


def load_lefff_dict(input_file_path):
    additional_dict_lefff = {}
    line_number = 0
    index_output = 1
    with open(input_file_path, mode='r', encoding='utf-8') as input_file:
        for input_line in input_file:
            line_number += 1
            if line_number % 1000 == 0:
                index_output = print_carac_on_the_same_line(index_output)
            # Process exceptions - for instance the adjective «bée» like in « bouche bée »
            # and the adjective «messis» which has no masculine singular form
            if re.search('^bée\t|^dû\t|^dûs\t|^due\t|^dues\t|^dus\t|^inf\.\.\t|^messis\t|^messise\t|^messises\t|^pu\t|^sup\.\.\t',
                         input_line, flags=0) is not None:
                pass
                # For the in memory processing, all the LEFFF dictionary is loaded other than the above exceptions
                # thus the line below which is filtering only the 'adj' with lemma suffix in 'r' or 're' is commented
            #           elif ( re.search("([^\d\s]*)\tadj\t([^\d\s]*[r]+)\t([^\d\s]*)|([^\d\s]*)\tadj\t([^\d\s]*re+)\t([^\d\s]*)",input_line, flags=0) != None ):
            else:
                # Important remove the \n at the end
                line_data = re.split('\t', input_line[:-1])
                inflected_form = line_data[inflected_i]
                pos_tag = line_data[pos_i]
                lemma = line_data[lemma_i]
                misc = line_data[misc_i]
                # The old_lemma is initialized to lemma
                old_lemma = line_data[lemma_i]
                # Test if we have a clitic pronoun
                clitic_pronoun = re.search(
                    '\tcla\t(cla)\t|\tclar\t(clar)\t|\tcld\t(cld)\t|\tcldr\t(cldr)\t|\tclg\t(clg)\t|\tcll\t(cll)\t|\tcln\t(cln)\t|\tclr\t(clr)\t|\tilimp\t(ilimp)\t|\tpro\t(pro)\t',
                    input_line, flags=0)
                if clitic_pronoun is not None:
                    pos_tag = [clitic_pronoun.group(i_group) for i_group in range(1, 11) if not clitic_pronoun.group(i_group) is None][0]
                    old_lemma = pos_tag
                    if TRACE:
                        print(line_number, '\t', input_line, '\t', pos_tag)
                    if pos_tag in ['cla', 'clar']:
                        lemma = 'le'
                    elif pos_tag == 'cld':
                        lemma = 'lui'
                    elif pos_tag == 'clg':
                        lemma = 'en'
                    elif pos_tag == 'cll':
                        lemma = 'y'
                    elif pos_tag in ['cln', 'ilimp']:
                        lemma = 'il'
                    elif pos_tag in ['clr', 'cldr']:
                        lemma = 'se'
                    else:
                        lemma = 'UNKNOWN'
                    entry_key = lemma + '_' + pos_tag + '_' + misc + inflected_form
                else:
                    entry_key = lemma + '_' + pos_tag + '_' + misc
                if TRACE and (pos_tag == "ilimp"):
                    print({entry_key: [inflected_form, pos_tag, lemma, misc, old_lemma]})
                if TRACE and (inflected_form in clitic_pronouns):
                    print({entry_key: [inflected_form, pos_tag, lemma, misc, old_lemma]})
                additional_dict_lefff.update({entry_key: [inflected_form, pos_tag, lemma, misc, old_lemma]})
    print()
    print("Last line: ", line_number, "\t", input_line)
    print("End processing file: ", input_file_path)
    print("Closing file: ", input_file_path)
    return additional_dict_lefff


def transform_additional_lefff_dict(additional_dict_lefff):
    new_additional_dict_lefff = {}
    line_number = 0
    trace = False
    for dict_key, dict_value in additional_dict_lefff.items():
        line_number += 1
        if trace and (line_number % 10000 == 0):
            print(dict_key, extract_inflected_from_key(dict_key, additional_dict_lefff),
                  extract_pos_from_key(dict_key, additional_dict_lefff), dict_value)
        if is_verb_inf_lemma_for_adj(dict_key, additional_dict_lefff):
            if trace and (line_number % 10000 == 0):
                print("New dict entry:")
            new_lemma = find_lemma_adj_masc_sing(dict_key, additional_dict_lefff)
            if trace and (line_number % 10000 == 0):
                print("new_lemma: ", new_lemma)
            if not new_lemma == "not found":
                if trace and (line_number % 10000 == 0):
                    print("   ", "dict_key: ", dict_key)
                new_inflected_form = extract_inflected_from_key(dict_key, additional_dict_lefff)
                if trace and (line_number % 10000 == 0):
                    print("   ", "inflected_form: ", new_inflected_form)
                new_pos = extract_pos_from_key(dict_key, additional_dict_lefff)
                if trace and (line_number % 10000 == 0):
                    print("   ", "POS: ", new_pos)
                    print("   ", "lemma: ", new_lemma)
                new_misc = extract_misc_from_key(dict_key, additional_dict_lefff)
                old_lemma = extract_old_lemma_from_key(dict_key, additional_dict_lefff)
                if trace and (line_number % 10000 == 0):
                    print("   ", "misc: ", new_misc)
                    print("   ", "old_lemma: ", old_lemma)
                new_additional_dict_lefff.update(
                    {dict_key: [new_inflected_form, new_pos, new_lemma, new_misc, old_lemma]})
        else:
            new_inflected_form = extract_inflected_from_key(dict_key, additional_dict_lefff)
            new_pos = extract_pos_from_key(dict_key, additional_dict_lefff)
            new_lemma = extract_lemma_from_key(dict_key, additional_dict_lefff)
            new_misc = extract_misc_from_key(dict_key, additional_dict_lefff)
            old_lemma = extract_old_lemma_from_key(dict_key, additional_dict_lefff)
            if trace and (line_number % 10000 == 0):
                print({dict_key: [new_inflected_form, new_pos, new_lemma, new_misc, old_lemma]})
            new_additional_dict_lefff.update({dict_key: [new_inflected_form, new_pos, new_lemma, new_misc, old_lemma]})
    return new_additional_dict_lefff


OUTPUT_FILE_PATH = "/Users/claudecoulombe/git/semantron/notebooks/lefff-3.4.mlex/lefff-3.4-addition.mlex"

GENERATE_NEW_LEFFF = False


def save_lefff_addition_datafile(additional_dict_lefff, output_file_path):
    line_number = 0
    if GENERATE_NEW_LEFFF:
        output_file_path = "/Users/claudecoulombe/git/semantron/notebooks/lefff-3.4.mlex/lefff-3.4-new.mlex"
    with open(output_file_path, mode='w', encoding='utf-8') as output_file:
        index_output = 1
        for dict_key, dict_value in additional_dict_lefff.items():
            line_number += 1
            if line_number % 1000 == 0:
                index_output = print_carac_on_the_same_line(index_output)
            inflected_form = extract_inflected_from_key(dict_key, additional_dict_lefff)
            pos_tag = extract_pos_from_key(dict_key, additional_dict_lefff)
            lemma = extract_lemma_from_key(dict_key, additional_dict_lefff)
            old_lemma = extract_old_lemma_from_key(dict_key, additional_dict_lefff)
            misc = extract_misc_from_key(dict_key, additional_dict_lefff)
            if GENERATE_NEW_LEFFF:
                output_file.write(
                    inflected_form + "\t" + pos_tag + "\t" + lemma + "\t" + misc + "\t" + old_lemma + '\n')
            elif pos_tag in ['adj', 'cla', 'clar', 'cld', 'cldr', 'clg', 'cll', 'cln', 'clr', 'ilimp', 'pro']:
                output_file.write(
                    inflected_form + "\t" + pos_tag + "\t" + lemma + "\t" + misc + "\t" + old_lemma + '\n')
        output_file.write('bée' + "\t" + 'adj' + "\t" + 'bée' + "\t" + 'Kfs' + "\t" + 'béer' + '\n')
        output_file.write('dû' + "\t" + 'adj' + "\t" + 'dû' + "\t" + 'Kms' + "\t" + 'devoir' + '\n')
        output_file.write('dûs' + "\t" + 'adj' + "\t" + 'dû' + "\t" + 'Kmp' + "\t" + 'devoir' + '\n')
        output_file.write('dus' + "\t" + 'adj' + "\t" + 'dû' + "\t" + 'Kmp' + "\t" + 'devoir' + '\n')
        output_file.write('due' + "\t" + 'adj' + "\t" + 'dû' + "\t" + 'Kfs' + "\t" + 'devoir' + '\n')
        output_file.write('dues' + "\t" + 'adj' + "\t" + 'dû' + "\t" + 'Kfp' + "\t" + 'devoir' + '\n')
        output_file.write('messis' + "\t" + 'adj' + "\t" + 'messis' + "\t" + 'Km' + "\t" + 'messeoir' + '\n')
        output_file.write('messise' + "\t" + 'adj' + "\t" + 'messis' + "\t" + 'Kfs' + "\t" + 'messeoir' + '\n')
        output_file.write('messises' + "\t" + 'adj' + "\t" + 'messis' + "\t" + 'Kfp' + "\t" + 'messeoir' + '\n')
        output_file.write('pu' + "\t" + 'adj' + "\t" + 'pu' + "\t" + 'K' + "\t" + 'pouvoir' + '\n')
        # Difficult decision to add an entry to process «au» which in fact is the contraction of
        # «à le», «à la», «à l'», «à les», where «à» is a preposition (préposition)
        # and «le, la, l, les» a determiner (déterminant ou article)
        output_file.write('au' + "\t" + 'det' + "\t" + 'ms' + "\t" + 'au' + "\t" + 'au' + '\n')
        output_file.write('aux' + "\t" + 'det' + "\t" + 'p' + "\t" + 'au' + "\t" + 'aux' + '\n')
    print()
    print("Last line: ", line_number)
    print("Closing file: ", output_file_path)


def create_additional_lefff_datafile(input_file_path, output_file_path):
    initial_additional_dict_lefff = load_lefff_dict(input_file_path)
    new_additional_dict_lefff = transform_additional_lefff_dict(initial_additional_dict_lefff)
    save_lefff_addition_datafile(new_additional_dict_lefff, output_file_path)


print("Create LefffAdditionDatafile code ready!")
