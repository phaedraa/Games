'''
Word Wrangler game

Word Wrangler is a game that generates all possible words from a user's input word

'''

import urllib2
import codeskulptor
import poc_wrangler_provided as wrangler

WORDFILE = "assets_scrabble_words3.txt"

def remove_duplicates(list1):
    '''
    Eliminate duplicates in a sorted list.
    Returns a new sorted list with the same elements in list1, but
    with no duplicates.
    '''
    list2 = list(list1)
    count_vals_dict = {}
    for val in list1:
        if count_vals_dict.get(val) == None:
            count_vals_dict[val] = 1
        else:
            list2.remove(val)
    return list2

def intersect_nonempty_list(list1, list2):
    '''
    Generates the intersection of two sorted non-empty lists
    Returns a list
    '''
    same_vals = []
    idx2 = 0
    for val in list1:
        while idx2 < len(list2) and list2[idx2] < val:
            idx2 += 1
        if idx2 < len(list2):
            if val == list2[idx2]:
                same_vals.append(val)
    return same_vals

def intersect(list1, list2):
    '''
    Generates the intersection of two sorted lists. Lists can be empty.
    Returns a list
    '''
    if not list1 or not list2:
        return []
    else:
        return intersect_nonempty_list(list1, list2)
        
def initial_merge(list1, list2):
    '''
    Merge sorted list1 and list2 up to whichever list has minimum length
    '''
    l1_idx = 0
    l2_idx = 0
    merged = []
    while l1_idx < len(list1) and l2_idx < len(list2):
        if list1[l1_idx] < list2[l2_idx]:
            merged.append(list1[l1_idx])
            l1_idx += 1
        else:
            merged.append(list2[l2_idx])
            l2_idx += 1
    return {'l1_idx': l1_idx, 'l2_idx': l2_idx, 'merged': merged}

def final_merge(list1, list2):
    '''
    Merge remaining values of whichever list1 or list2 has maximum length
    '''
    initial_result = initial_merge(list1, list2)
    l1_idx = initial_result['l1_idx']
    l2_idx = initial_result['l2_idx']
    merged = initial_result['merged']
    rem_idx = max(l1_idx, l2_idx)
    remaining = []
    if l1_idx < len(list1):
        rem_idx = l1_idx
        remaining = list1
    elif l2_idx < len(list2):
        rem_idx = l2_idx
        remaining = list2
    while rem_idx < len(remaining):
        merged.append(remaining[rem_idx])
        rem_idx += 1
    return merged

def merge(list1, list2):
    '''
    Merge two sorted lists.
    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.
    ''' 
    if len(list1) == 0:
        return list(list2)
    elif len(list2) == 0:
        return list(list1)
    
    return final_merge(list1, list2)

def merge_sort(alist):
    '''
    Sort an unsorted list by breaking the list into sorted lists and merging
    Return the sorted list
    '''
    if len(alist) > 1:
        mid = len(alist) / 2
        left = merge_sort(alist[:mid])
        right = merge_sort(alist[mid:])
        return merge(left, right)
    else:
        return alist

def gen_word_combs(first_letter, rest_strings):
    '''
    Generate all word combinations given the first letter of a word and a list
    of words
    Return a list of all possible combinations
    '''
    gen_comb = [first_letter]
    for string in rest_strings:
        for idx in range(len(string) + 1):
            new_string = string[:idx] + first_letter + string[idx:] 
            gen_comb.append(new_string)
    
    return gen_comb + rest_strings

def gen_all_strings_initial(word):
    '''
    Generate all strings that can be composed from the letters in word
    in any order.
    Returns a list of all strings that can be formed from the letters
    in word.
    '''
    if len(word) <= 1:
        return [word]
    else:
        first = word[0]
        rest = word[1:]
        rest_strings = gen_all_strings_initial(rest)
        all_strings = gen_word_combs(first, rest_strings)
    return all_strings

def gen_all_strings(word):
    '''
    Generates all possible strings of a word. Treats each letter as distinct, so
    if the same letter appears twice in the word, then the output will have 
    duplicate strings.
    Returns a list of strings
    '''
    idx = 0
    has_empty_str = False
    all_strings = gen_all_strings_initial(word)
    while not has_empty_str and idx < len(all_strings):
        if all_strings[idx] == '':
            has_empty_str = True
        idx += 1
    if not has_empty_str:
        return all_strings + ['']
    else:
        return all_strings

def load_words(filename):
    '''
    Load word list from the file named filename.
    Returns a list of strings.
    '''
    words = []
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    for line in netfile.readlines():
        words.append(line[:-1])
    return words

def run():
    '''
    Run game.
    '''
    words = load_words(WORDFILE)
    wrangler = wrangler.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    wrangler.run_game(wrangler)

run()