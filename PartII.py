# Linneus3.py
# Implements storage and inference on an ISA hierarchy
# This Python program goes with the book "The Elements of Artificial
# Intelligence".
# This version runs under Python 3.x.

# Steven Tanimoto
# (C) 2012.

# The ISA relation is represented using a dictionary, ISA.
# There is a corresponding inverse dictionary, INCLUDES.
# Each entry in the ISA dictionary is of the form
#  ('turtle' : ['reptile', 'shelled-creature'])

"""PartII.py
Ziming Guo, CSE 415, Spring 2015, University of Wahsington
Instructor:  S. Tanimoto.

Assignment 2 Part II.  ISA Hierarchy Manipulation
Status of the implementation of new features:

1. (Cycle detection) implemented and working.
2. (Cycle processing) implemented and working.
3. (Why, with antisymmetry) implemented and working.
4. (Retraction of inferrable consequences) Not implemented.
5. (Persistence) Not implemented.
"""

from re import *   # Loads the regular expression module.

ISA = {}
INCLUDES = {}
ARTICLES = {}
ALIAS = {}

def store_isa_fact(category1, category2):
    'Stores one fact of the form A BIRD IS AN ANIMAL'
    # That is, a member of CATEGORY1 is a member of CATEGORY2
    try :
        c1list = ISA[category1]
        c1list.append(category2)
    except KeyError :
        ISA[category1] = [category2]
    try :
        c2list = INCLUDES[category2]
        c2list.append(category1)
    except KeyError :
        INCLUDES[category2] = [category1]

def get_isa_list(category1):
    'Retrieves any existing list of things that CATEGORY1 is a'
    try:
        c1list = ISA[category1]
        return c1list
    except:
        return []

def get_includes_list(category1):
    'Retrieves any existing list of things that CATEGORY1 includes'
    try:
        c1list = INCLUDES[category1]
        return c1list
    except:
        return []

def isa_test1(category1, category2):
    'Returns True if category 2 is (directly) on the list for category 1.'
    c1list = get_isa_list(category1)
    return c1list.__contains__(category2)

def isa_test(category1, category2, depth_limit = 10):
    'Returns True if category 1 is a subset of category 2 within depth_limit levels'
    if category1 == category2 : return True
    if isa_test1(category1, category2) : return True
    if depth_limit < 2 : return False
    for intermediate_category in get_isa_list(category1):
        if isa_test(intermediate_category, category2, depth_limit - 1):
            return True
    return False

def store_article(noun, article):
    'Saves the article (in lower-case) associated with a noun.'
    ARTICLES[noun] = article.lower()

def get_article(noun):
    'Returns the article associated with the noun, or if none, the empty string.'
    try:
        article = ARTICLES[noun]
        return article
    except KeyError:
        return ''

def whole_name(noun):
    return get_article(noun) + " " + noun

def linneus():
    'The main loop; it gets and processes user input, until "bye".'
    print('This is Linneus.  Please tell me "ISA" facts and ask questions.')
    print('For example, you could tell me "An ant is an insect."')
    while True :
        info = input('Enter an ISA fact, or "bye" here: ')
        print(info)
        if info == 'bye': return 'Goodbye now!'
        process(info)

# Some regular expressions used to parse the user sentences:    
assertion_pattern = compile(r"^(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
confirm_pattern = compile(r"^I\s+insist\s+that\s+(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)

def process(info) :
    'Handles the user sentence, matching and responding.'
    result_match_object = assertion_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        # print(items)
        store_article(items[1], items[0])
        store_article(items[3], items[2])
        items1 = get_alias(items[1])
        items3 = get_alias(items[3])
        if not detect_loop(items1, items3):
            store_isa_fact(items1, items3)
            if items[1] != items1 or items[3] != items3:
                print("I'll remember that {0} is {1}.".format(whole_name(items1), whole_name(items3)))
            else:
                print("I understand.")
        else:
            try:
                print("Yes, but {0} is {1}, because {2} I'm not going to remember that {1} is {0} unless you insist."\
                      .format(whole_name(items3), whole_name(items1), report_chain(items3, items1)))
            except TypeError:
                print("Yes, but {0} is {1}, because you told me that."
                      " I'm not going to remember that {1} is {0} unless you insist."
                      .format(whole_name(items3), whole_name(items1)))
        return

    result_match_object = query_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        items1 = get_alias(items[1])
        items3 = get_alias(items[3])
        answer = isa_test(items1, items3)
        if answer :
            if items[1] != items1 or items[3] != items3:
                print("Yes, {0} is {1}.".format(whole_name(items1), whole_name(items3)))
            else:
                print("Yes, it is.")
        else :
            print("No, as far as I have been informed, it is not.")
        return

    result_match_object = what_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        supersets = get_isa_list(items[1])
        if supersets != [] :
            first = supersets[0]
            a1 = get_article(items[1]).capitalize()
            a2 = get_article(first)
            print(a1 + " " + items[1] + " is " + a2 + " " + first + ".")
            return
        elif items[1] in ALIAS.keys():
            print(items[1].capitalize() + " is another name for " + ALIAS[items[1]] + ".")
            return
        else:
            subsets = get_includes_list(items[1])
            if subsets != [] :
                first = subsets[0]
                a1 = get_article(items[1]).capitalize()
                a2 = get_article(first)
                print(a1 + " " + items[1] + " is something more general than " + a2 + " " + first + ".")
                return
            else :
                print("I don't know.")
        return

    result_match_object = why_pattern.match(info)
    if result_match_object != None :
        items = result_match_object.groups()
        if not isa_test(get_alias(items[1]), get_alias(items[3])) :
            print("But that's not true, as far as I know!")
        else:
            answer_why(items[1], items[3])
        return

    result_match_object = confirm_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        a = get_alias(items[1])
        b = get_alias(items[3])
        same = []
        for i in find_chain(b, a):
            same.append(i[0])
        same.insert(0, a)
        for i in same:
            if i in list(ISA.keys()) and i != a:
                for j in ISA[i]:
                    if j != a:
                        try:
                            if j not in ISA[a]:
                                ISA[a].append(j)
                        except KeyError:
                            ISA[a] = [j]
                ISA.pop(i)
            if i in INCLUDES.keys():
                for j in INCLUDES[i]:
                    try:
                        if j not in INCLUDES[a] and j not in same:
                            INCLUDES[a].append(j)
                    except KeyError:
                        INCLUDES[a] = [j]
                if i != a:
                    INCLUDES.pop(i)
            if i != a:
                ALIAS[i] = a
        for i in ISA.keys():
            for j in ISA[i]:
                if j in same:
                    ISA[i].remove(j)
                    if i != a:
                        ISA[i].append(a)
        for i in list(INCLUDES.keys()):
            for j in INCLUDES[i]:
                if j in same[1:]:
                    INCLUDES[i].remove(j)
            if INCLUDES[i] == []:
                INCLUDES.pop(i)
        if len(same) == 2:
            numbers = 'both'
        else:
            numbers = 'all'
        print('Then I am inferring that {0} are {1} names for the same thing.'\
              .format(connect_phrase(same), numbers))
        print("I will use the name " + a + " for this class, and I will consider the others to be aliases for it.")
        return

    print("I do not understand.  You entered: ")
    print(info)

def get_alias(item):
    if item in ALIAS.keys():
        return ALIAS[item]
    return item


def detect_loop(a, b):
    result = False
    if b not in ISA.keys():
        return False
    if a in ISA[b]:
        return True
    for i in ISA[b]:
        result = result or detect_loop(a, i)
    return result

def answer_why(x, y):
    'Handles the answering of a Why question.'
    if x == y:
        print("Because they are identical.")
        return
    newx = get_alias(x)
    newy = get_alias(y)
    if isa_test1(x, y):
        print("Because you told me that.")
        return
    if isa_test1(newx, newy):
        if newx != x:
            print("Because {1} is another name for {0}, {2} is {3}"
                  .format(newx, x, whole_name(newx), whole_name(newy)), end='')
        else:
            print("{0} is {1}".format(whole_name(newx).capitalize(), whole_name(newy)), end='')
        if newy != y:
            print(", and {1} is another name for {0}.".format(newy, y))
        else:
            print(".")
        return
    if newx != x or newy != y:
        if newx != x:
            print("Because {1} is another name for {0}, {2}"
                  .format(newx, x, report_chain(newx, newy)), end='')
        else:
            print("{0}".format(report_chain(newx, newy).capitalize()), end='')
        if newy != y:
            print(", and {1} is another name for {0}.".format(newy, y))
        else:
            print(".")
        return
    print("Because " + report_chain(x, y))
    return

from functools import reduce
def report_chain(x, y):
    'Returns a phrase that describes a chain of facts.'
    chain = find_chain(x, y)
    all_but_last = chain[0:-1]
    last_link = chain[-1]
    main_phrase = reduce(lambda x, y: x + y, map(report_link, all_but_last))
    last_phrase = " and " + report_link(last_link)
    new_last_phrase = last_phrase[0:-2] + '.'
    return main_phrase + new_last_phrase

def connect_phrase(alias):
    main_phrase = reduce(lambda x, y: x + ', ' + y, alias[0:-1])
    last_phrase = " and " + alias[-1]
    return main_phrase + last_phrase

def report_link(link):
    'Returns a phrase that describes one fact.'
    x = link[0]
    y = link[1]
    a1 = get_article(x)
    a2 = get_article(y)
    return a1 + " " + x + " is " + a2 + " " + y + ", "

def find_chain(x, z):
    'Returns a list of lists, which each sublist representing a link.'
    if isa_test1(x, z):
        return [[x, z]]
    else:
        for y in get_isa_list(x):
            if isa_test(y, z):
                temp = find_chain(y, z)
                temp.insert(0, [x,y])
                return temp

def test() :
    process("A turtle is a reptile.")
    process("A turtle is a shelled-creature.")
    process("A reptile is an animal.")
    process("An animal is a thing.")
    # process("A being is a creature")
    # process("A creature is an animal")
    # process("I insist that an animal is a being")
    # process("A creature is an organism")
    # process("An organism is a living-thing")
    # process("A living-thing is an organism")
    # process("I insist that a living-thing is an organism")

test()
linneus()

