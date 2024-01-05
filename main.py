#######################################################################################
#
# Lewis_Short_Headwords
#
# INPUT: lewis-short.txt / A plain-text version of Lewis and Short: A Latin Dictionary
# (available at https://github.com/telemachus/plaintext-lewis-short).
#
# OUTPUT: lewis_short_by_headword.txt
#         lewis_short_by_headword.json
#
# The text output file is formatted in pairs of lines, as follows: The first line begins
# with # and then is a comma-separated list of headwords that link to a dictionary
# entry. The second line is the dictionary entry these headwords link to. In our
# input file, each dictionary entry is on one line (no newlines in an entry).
#
# Line 1: #a,ab,abs
# Line 2: a, ab, abs: preposition, 'from', etc..
#
# The JSON file saves the same information as a Python dictionary.
#
#######################################################################################

import re
import os

INPUT_FILE = 'lewis-short.txt'

TEXT_RESULT_FILE = 'lewis_short_by_headword.txt'
JSON_RESULT_FILE = 'lewis_short_by_headword.json'

# For removing accents and special characters, so we can run simple tests. Accents will 
# be unmodified in final result.
table = {'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a', 'å': 'a', 'ā': 'a', 'ă': 'a',
         'ἅ': 'a', 'ᾷ': 'a', 'ạ': 'a',
         'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'ē': 'e', 'ĕ': 'e', 'ẽ': 'e',
         'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'ī': 'i', 'ĭ': 'i', 'ΐ': 'i', 'ί': 'i',
         'ἰ': 'i', 'ἴ': 'i', 'ϊ': 'i', 'ἶ': 'i',
         'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o', 'ō': 'o', 'ŏ': 'o', 'ὁ': 'o',
         'ὅ': 'o', 'ο': 'o', 'ὀ': 'o', 'ό': 'o', 'ὸ': 'o', 'ὄ': 'o',
         'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u', 'ū': 'u', 'ů': 'u', 'ŭ': 'u',
         'ý': 'y', 'ÿ': 'y', 'ȳ': 'y',
         'æ': 'ae', 'ǽ': 'ae', 'ǣ': 'ae',
         'œ': 'oe'}

trans_table = str.maketrans(table)

class Guess():
  # A system for cataloguing a large number of guesses. Works in a subdirectory, /results/,
  # and creates a different file for each type of guess. Deletes old files each round.
  files = {}
  count = 1
  
  directory_name = 'results'

  # Check if the directory exists
  if not os.path.exists(directory_name):
      # If it doesn't exist, create it
      os.makedirs(directory_name)
  
  def __init__(self):
    # delete any guess files from the past.
    files = os.listdir('results/')
    for file in files:
      os.remove('results/'+file)
    self.count = 1
    self.files = {}
    
  # Records a guess, and pertinent examples thereof.
  def g(self, identifier, items, silent = False):

    # To see all guesses, comment out the next two lines and rerun.
    if silent:
      return
    
    # Start a new file
    if identifier not in self.files:
      try:
        self.files[identifier] = 'results/'+identifier+'.txt'
        with open(self.files[identifier], 'w') as f:
          f.write('this is for '+identifier+'\n\n')
          f.write('\n'+identifier + '\n')
          for item in items: # Record any data sent to us
            f.write(item[0:160] + '\n')
      except:
        # If the identifier failed as a filename, use {count}.txt
        self.files[identifier] = 'results/' + str(self.count) + '.txt'
        self.count += 1
        with open(self.files[identifier], 'w') as f:
          f.write('this is for '+identifier+'\n\n')
          f.write('\n'+identifier + '\n')
          for item in items:
            f.write(item[0:160] + '\n')
    else:
      with open(self.files[identifier], 'a') as f:
          f.write('this is for '+identifier+'\n\n')
          f.write('\n'+identifier + '\n')
          for item in items:
            f.write(item[0:160] + '\n')
    


def add(keyword, entry):
  # For each headword per entry that we discover, we use this function to link
  # that headword to its entry. This includes a little checking to avoid
  # confusing principle parts with variations on headwords.
  
  rejects = {'us','ae', 'li', 'onis'}
  if n(keyword) in rejects:
    return

  concerning = {'ae', 'ii', 'ivi', 'e', 'a', 'es', 'i', 'indecl.', 'are', 'ire', 'ere',
                    'um', 'onis', 'orum', 'ii', 'adv.', 'etis', 'is',
                    'arum', 'ium', 'eris', 'opis', 'icui', 'ixi', 'o', 'ontis',
                    'itis', 'oris', 'teris', 'tri', 'adj.', 'idis', 'elis', 'enis',
                    'uis', 'us', 'inis', 'otis', 'bui', 'adis', 'abl.', 'acis'}

  if n(keyword) in concerning:
    g.g('concerning keyword', [keyword,entry],
       True)
    
  if not keyword:
    return
    
  if keyword and not entry:
    print('keyword',keyword,'has blank entry')
    exit(1)

  keyword = re.sub('[/;,]', '', keyword)
  keyword = re.sub('\W', '', keyword)
  if re.search('\W', keyword):
    g.g('weird keyword', [keyword,entry])
  if '.' in keyword:
    g.g('period', [keyword, entry])
  
  if keyword not in dictionary:
    dictionary[keyword] = {}
  else:
    # The keyword exists.
    # Avoid duplicate entries.
    if entry in dictionary[keyword]:
      #print('skipping',keyword)
      g.g('duplicate keyword-entry combo avoided', [keyword, entry], True)
      return
  #dictionary[keyword].append(entry)
  dictionary[keyword][entry] = ''
  return
  
def repair_dashed_first_word(string):
  # Entries like ad -firmo, are (that's made up example but typical).
  # Or ad-firmo, are (also made up).
  # This will replace the first occurrence of this phenomenon with a repaired word.
  return re.sub('^(\w+)\s{0,2}\-(\w)', r'\1\2', string, 1, re.MULTILINE)

def sim(s1, s2):
  # I found this online---it compares two strings and gives a pct for how similar they are.
  # Source: https://stackoverflow.com/questions/21219259/longest-common-substring
  def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for i in range(1 + len(s1))]
    longest, x_longest = 0, 0
    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0
    return s1[x_longest - longest: x_longest]
  return 2. * len(longest_common_substring(s1, s2)) / (len(s1) + len(s2)) * 100

def normalize(target):
  # make word lowercase and remove accents
  # We do not modify dictionary contents but when analyzing and comparing
  # possible headwords this enables us to compare apples to apples in a 
  # simple manner.
  return target.lower().translate(trans_table)

def first_words(string):
  # Returns th first (number) words of an entry.
  number = 12
  string = string.replace(',', ' ')
  a = re.split('\s+', string)[0:number]
  return a
  
def apply_change(original, change):
  # This deals with word modifications / variations. For example:
  # suffix changes: Solymus (-on)
  # prefix changes: adfirmo (aff-)
  # mid-word changes: postcaenium (-cen-)
  # and word replacements: spondalium (spondaulium)
  # or coralium or curalium (choral-lum)

  if change == 'adc.':
    change = 'adc-'

  if not change:
    return ''
    
  if '-' not in change:
    return change

  change = change.replace('‡', '')
  original = original.replace('‡', '')
  original = original.replace('-','')

  g.g('changelog', [f'{original} -> {change}'], True)

  # Need to address
  # Acalcĕŏlārĭus (calcĭŏl-), ii, m. calceolus,
    
  # Special Cases
  if change.endswith('-'):
    #aedĭtĭmus (aedĭtŭ-) (an earlier form for aedituus, and first used in the time of Varro; v. the first quotation), i, m., one who keeps or takes care of a temple,
    try:
      temp = n(change)[:-2]
      temp2 = n(original)[:len(temp)]
      if temp == temp2:
        if n(change).endswith('tu-') and temp2.endswith('t'):
          change = change.replace('-', '')
          #print('found',original,' stem is ',end='')
          original = change + original[len(change):]
          #print(change,'changed to ',original)
          return original
    except:
      exit(1)

  if n(change) == '-nunc-':
    if n(original) == 'internuntio':
      return 'internuncĭo'

  if n(change) == '-humer-':
    if original == 'sŭpĕrumerale':
      return 'sŭpĕrhumerale'
      
  if n(change) == '-rr-':
    location = n(original).find('r')
    replacement=original[0:location] + 'r' + original[location:]
    return replacement
  
  if n(change) == '-emt-':
    if n(original).startswith('interemp'):
      change = change.replace('-','')
      last=n(change)[-1]
      location=n(original).rfind(last) +1
      
      replacement = original[0:5] + change + original[location:]
      return replacement
  
  if n(change) == '-tius':
    if n(original).endswith('cius'):
      replacement = original[:-4] + change.replace('-', '')
      return replacement
  if change == '-a':
    if original.endswith('es'):
      replacement = original[:-2] + change.replace('-', '')
      return replacement
  if n(change) == '-iens':
    if n(original).endswith('ies'):
      replacement = original[:-3] + change.replace('-', '')
      return replacement
  if change == '-es':
    if original.endswith('ta'):
      replacement = original[:-1] + change.replace('-', '')
      return replacement
  if n(change) == '-on':
    if n(original).endswith('o'):
      replacement = original[:-1] + change.replace('-', '')
      return replacement
  if change == '-_ia':  #Erythēa or -_ia, ae, f., = Ἐρύθεια, a small island
    if original.endswith('a'):
      replacement = original[:-1] + 'ia'
      return replacement
  if n(change) == '-orus':   #ignĭcŏlor or -ōrus, a, um, adj. ignis-color
    if n(original).endswith('or'):
      replacement = original[:-2] + change.replace('-', '')
      return replacement

  if change.startswith('-') and change.endswith('-'):
    # Words such as sŭpĕr-umerale (-humer-), is, or postcaenium (-cen-)
    new_stem = change.replace('-', '')
    letter=n(new_stem)[0]
    location = n(original).find(letter, 1)
    if location == -1:
      g.g('error in apply_change',[original,change])
    if n(original)[location + 1] == letter:
      location += 1
    letter2 = n(new_stem)[-1]
    location2 = n(original).find(letter2, location + 1)
    if n(original)[location2 + 1] == letter2:
      location2 += 1
    result = original[0:location] + new_stem + original[location2 + 1:]
    return result

  # suffixes or prefixes
  if change.startswith('-') or change.endswith('-'):
    reversal = False
    if change.endswith('-'):
      reversal = True
      original = original[::-1]
      change = change[::-1]
    change = change.replace('-', '')
    suffix = change
    letter = n(suffix)[0]
    
    location = n(original).rfind(letter, 0, len(original) - 1)
    # so in Tenedos or -us, we're searching for u
    if location == -1: # not found.
      # Simply overlay it.
      result = original[:-len(suffix)] + suffix
    # it is found.
    # something like burrĭcus or būrĭcus (-chus)
    elif len(original) - location >= (len(suffix) * 2):
      # I don't like this. 
      # So just overlay it
      result = original[:-len(suffix)] + suffix
    else:
      if location > 2:
        if original[location - 1] == letter:
          location -= 1
      result = original[0:location] + suffix
    if reversal:
      result = result[::-1]
    return result

  if '-' in change:
    # coralium or curalium (coral-lum)
    # delete dash and return the whole word
    return change.replace('-', '')

  print('shouldnt arrive here')
  exit(1)


def examine_or_also_and_with_parenth(line):
  entry = line
  line = repair_dashed_first_word(line)
  # Is it an or / and / also line?
  if re.search('^\w+,{0,1}\sor[,\s]', line) or re.search('^\w+,{0,1}\sand[,\s]', line) or  re.search('^\w+,{0,1}\salso[,\s]', line):
  
    # This establishes it as an 'or' or an 'and'.

    
    first = first_words(line)
    original = first[0]
    second = first[2] # e.g. word1 and word2, second=word2 now.
    

    if second == '‡':
      first.pop(2)
      second = first[2]

    if not second[0].isalpha() and second[0] != '-' and second[0] != '(':
      g.g('second_is_not_alpha', [second,line])

    third = ''
    fourth = ''
    if second.startswith('('):  # word, or (in Augustine etc) word2
      # There are only a handful of these - delete them all.
      # It goes like this:
      # word, or (in Augustine etc) word2
      # So in this case, delete the parenthesis
      # And continue processing same line.
      g.g('deleted_parenth_after_orandalso', [original,second,line], True)
      # This seems to work.
      line = re.sub('\(.*?\)', '', line, 1)
      first = first_words(line)
      second = first[2]

    # We are back to __ or/and/also ___

    # ărātro and contr. artro, āre, v. a.
    if second == 'contr.' or second == 'euphon.' or second == 'uncontr.' or second == 'abbrev.' or second == 'sync.':
      g.g('contr.euphon.uncontr.abbrev.sync.', [first[3], line], True)
      # Repairing second.
      second = first[3]
    if 'ŭtĭquĕ, and that, v. ut (uti) and que.' in line:
      second = ''
    if second == 'derivv.':
      g.g('skipping derivv.', [line], True)
      # Skip this second. This appears to work.
      second = ''
    # circumverto or circum verto (-vorto), ĕre, v. a.,
    if second == 'in':
      g.g('found in', [second,line], True)
      if original == 'caerŭlĕus':
        second = 'caerŭlus'
      if original == 'dēlēnĭo':
        second = 'dēlīnĭo'
      if original == 'dēlonge':
        second = ''
      if original == 'fīglīnus':
        second = 'fĭgŭlīnus'
      if original == 'pējĕro':
        second = 'perjūro'

    
    if n(original) == (n(first[2]) + n(first[3])).replace('-', ''): 
      # ignoring this second because it's the same as headword.
      # antĕāquam or antea quam, v. antea, IV.
      # māterfămĭlĭas and māter fămĭ-lĭas, v. familia
      second = ''
      # We ignore b/c don't want this entry
      # to appear under the single-word
      # version.
      g.g('second is spaced vers. of first', [original,line], True)
    #elif b:=re.search('anal\. to the Gr\., (\S+)',line):
    #  g.g('anal\. to the Gr\., (\S+)', [b.group(1), line])
    if b:=re.search('^\w+,{0,1} (or|and|also) \S+,{0,1} (or|and|also) (\S+?)[\s\.,]', line):
      # Second is done
      # But there's a third.
      third = b.group(3)
      g.g('positively found third', [third,line], True)

      # Here we have a small number of false positives in 'third'.
      
      # lāmĭna or lammĭna, and sync. lamna (e. g. Hor. C. 2, 2, 2; i
      # ărytaena or ărŭtaena, also contr. artaena, ae, f., = ἀρυταινη, a ve
      # effŏdĭo, also exf- and ecf- (cf. Neue, Formenl. 2, 767, 769)
      # also twice not contr. ălĭo-vorsum and ălĭō-versus, adv.  Lit
      if b:=re.search('(twice not contr|sync|contr|arch|uncontracted|several times repeated,)\.{0,1} (\S+?)[\s\(,]', line):
        if b:
          g.g('repaired third', [third, b.group(2), line], True)
          third = re.sub('\W', '', b.group(2))
          
          # In some cases theres yet another or preceded by a keyword
          # lŭcŭmo or lŭcŏmo, and sync. luc-mo or lucmon, ōnis, m. Etrusc.
          # dextrorsum or dextrorsus, or uncontracted dextrovorsum (or -ver-sum), adv. dexter-versus
          if c:=re.search(' '+b.group(2)+' [\(]{0,1}or (\S+?)[\)\s,]', line):
            fourth=c.group(1)
          g.g('found a fourth', [fourth,line], True)
      
          if fourth.startswith('-'):
            # I'm guessing we only apply this as a stem to the previous word????
            g.g('applied fourth stem', [original,second,third,fourth,line], False)
        else:
          print('no b')
          exit(1)
      if third == 'exsŏlo':
        fourth = 'exŏlo'
      if b:=re.search(' '+third+' [\(]{0,1}or (\S+?)[\)\s,]', line):
        # Another shot at a fourth.
        # Parnāsus and -os, also Parnas-sus or -os, i, m., = Παρνασός, afterwards
        fourth = b.group(1)
        g.g('found a fourth', [fourth, line], True)
        g.g('second fourth attempt', [original,second,third,fourth,line], True)
      
      
      second = apply_change(original,second)
      third = apply_change(second, third)
      fourth = apply_change(third,fourth)
      
      g.g('triple_or_and_also',
          [original,second,third,fourth,line],
          True)
    if b:=re.search('or, acc\. to many MSS\., (\S+?)[\s,]',line):
      # dissĭpo, or, acc. to many MSS., dis-sŭpo, āvi, ā
      g.g('or, acc\. to many MSS\., (\S+)',[b.group(1),line], True)
      second = b.group(1)
    if second == 'archaic':
      if b:=re.search('archaic,{0,1} (.*?),', line[0:100]):
        # multātĭcus, or, archaic, ‡ moltā-tĭcus, a, um, adj. i
        second=re.sub('\W', '', b.group(1))
        g.g('archaic with a bad symbol', [second, line], True)
      else:
        print('no archaic')
        exit(1)
    if original=='dēmĭurgus':
      second = 'dāmĭurgus'
    if b:=re.search('or in late Lat\., (\w+),',line):
      second = b.group(1)
      g.g('or in late Lat\., (\w+),',[second,line], True)
    if second == 'abbreviated':
      second = first[3]
      g.g('and abbreviated', [second,line], True)
    if 'or, in the orig. form, perjūro' in line:
      second = 'perjūro'
    if 'or, in the uncontr. primary form, fĭgŭlīnus' in line:
      second = 'fĭgŭlīnus'
    if 'dēlonge, or in two words, de longe, adv.' in line:
      second = ''
    if re.search('separate\w*', second) or re.search('separate\w*', first[3]):
      if b := re.search('separate\w*,{0,1}(.*?)[\(,]', line):
        second = b.group(1)
        second=re.sub('[\s-]', '', second)
        g.g('or_separated_separately_', [second, line], True)
      else:
        print('no separate')
        exit(1)
    if 'necnon, also separately, nec non or nĕquĕ non, partic. of emphatic affirmation' in line:
      #second = 'nĕquĕ non'
      second = ''
    if 'or with d demonstrative (see the letter D), rĕd' in line:
      second = 'rĕd'
    if 'or quĕm ad mŏ-dum, adv., in what manner,' in line:
      second = ''
    if 'anal. to the Gr., Crĕon, ontis' in line:
      second = 'Crĕon'
      # Crĕo, or, anal. to the Gr., Crĕon, ontis, m., = Κρέων.  A king of Corinth
    if second=='os':
      second = '-' + second
    if original == 'nonnumquam':
      # non-numquam or -nunquam, adv., 
      second = 'nonnunquam' # apply_change wouldn't figure this one out.
    if '.' in second:
      g.g('error-period_in_second',[original,second,line])
      second = ''

    # In theory we have a working 'second' word. Maybe a third or fourth.
    # now - so we file it.
    if re.search('\w+-\w+', second):
      # There are only about 20 of these.
      g.g('deleting-mid-dash-in-second', [second, line], True)
      #backup = second.replace('-', '')
      
      new = re.sub('(\w)-(\w)', r'\1\2', second)
      #if second.startswith ('-') or second.endswith('-'):
      #  g.g('changed backups', [second, backup, new, line])
      second = new

    if third:
      g.g('changes',[f'{original}, {second}, {third}, {fourth}', entry], True)
    
    if second:
      original = apply_change(original, second)
      add(original, entry)
    if third:
      original = apply_change(original, third)
      add(original, entry)
    if fourth:
      original = apply_change(original, fourth)
      add(original, entry)

    if second and third and fourth:
      g.g ('approvd_second_found_after_orandalso', 
           [second + '+'+third+"+"+fourth,line],
          True)
    elif second and third:
      g.g ('approvd_second_found_after_orandalso', 
           [second + '+'+third,line], True)
    elif second:
      g.g ('approvd_second_found_after_orandalso', 
           [second,line], True)
    
  
  line = repair_dashed_first_word(entry)
  first = first_words(entry)
  original=first[0]
  second=third=fourth=''
  # Is it word or word followed by ( ?
  
  if any(a.startswith('(') for a in first[1:]):
    # Isolate the contents of the parenthesis.

    # CLEAN UP A BIT
    line = re.sub('\((tri|dis|quadri)syl\.\)', '', line)
    line = re.sub('\(sc\.\)', '', line)

    # If still there..
      
    if b := re.search('^.*?\((.*?)\)', ' '.join(line.split()[0:20])):
      # Found the parenthetical contents.
      c = b.group(1)
      d = c.split()
      g.g('all parentheticals to examine', [b.group(1),line], True)
      if len(d) == 1: # ONE WORD IN PARENTHESES
        e = d[0] 
        #if e in ['poet.', 'post-class.', 'post-Aug.', 'anteclass.', 'class.', 'Ciceron.', 'ante-class.', 'postAug.', 'plur.', 'pentasyl.', 'eccl.', 'Lindem.', 'postclass.', 'Ptol.',
        #        'Plut.', 'iron.', 'Liv.', 'Vitr.', 'obsc.', 'delin.', 'Pseud.', 'Andron.', 'Plautin.', 'Hilar.', 'trop.', 'dissyll.', 'pcet.', 'Class.', 'Appul.', 'Vitruv', 'Hebr. ',
        #        'Plin.', 'trisyll.', 'Plaut.',
        #        'V.', 'jurid.', 'Cic.']:
        # Good stems:
        # adc., adqu.
        #Bad
        # acc.
        # Ignore it
      
        if e=='-caen-,-coen-':
          second='-caen-'
          third='-coen-'
          add(apply_change(original,second), 
             entry)
          add(apply_change(original, third),
             entry)
          e=''
        if '-' in e and not e.startswith('-') and not e.endswith('-') and not first[1].startswith('('):
          e = ''
        if '.' in e:
          if e in ['adc.', 'adqu.']:
            e = e.replace('.', '-')
          else:
            g.g('rejected single parenth w period', [e] + d + [line],True)
            e=''
        # Single word in parenthesis, keep it.
        if 'cătorchītes (vīnum)' in line:
          e = ''
        if (n(e).endswith('um') or n(e).endswith('us')) and n(original).endswith('o'):
          g.g('concerning single', [e,line],True)
          e=''
        if n(e).endswith('i'):
          if n(original).endswith('o'):
            g.g('rejected -i',[e,line], True)
            # ăbŏlĕo, ēvi (ui), ĭtum, 2, v. a., orig. 
            # Skip it
            e = ''
        if e == 'Ache':
          e += '-'
        if e:
          if e[0].isdigit():
            e=''
        if n(e) in ['ilex', 'caelator', 'oe', 'fungos', 'admittebant', 'ei', 'li', 'us', 'is']:
          e = ''
        if 'confĕro, contŭli, collātum (conl-), conferre,' in line:
          e = ''
        if 'ignōbĭlis, e, adj. in-nobilis (gno-)' in line:
          e = ''
        if 'lepton centaurĭum (-ĭon)' in line:
          e = ''
        if 'lĭbet or lŭbet, libuit (lub-)' in line:
          e = ''
        if 'prōvorsus, a, um, Part., from proverto (-vorto).' in line:
          e = ''
        if 'rīvus, i, m. root ri- (li-), to flow, drop;' in line:
          e = ''
        # Hyperbŏrĕi, ōrum, m., = Ὑπερβόρεοι (-ειοι), a fabulous 
        if 'Hyperbŏrĕi, ōrum, m., = Ὑπερβόρεοι (-ειοι), a fabulous' in line:
          e=''
        if 'ĭgĭtur, conj. [pronom. stem i- of is; suffix -ha (-dha);' in line:
          e = ''
        if (e and '-' not in e) and not first[1].startswith('('):
          g.g('rejected single parenth', [e, line], True)
          e = ''
        if e:
          add(apply_change(original, e), entry)
          third = e
          g.g('approved single parenth, keeping', [e, line], True)
          if not first[1].startswith('('):
            g.g('suspect single parenth', [e, line], True)
      elif len(d) == 2:
        if d[0] == 'v.' or d[0] == 'cf.':
          # Skip this. 'vide.'
          pass
        elif 'Hyărōtis, ĭdis, f., = Ὑαρῶτις (or Ὑδραώτης)' in line:
          pass
        elif 'Hylas, ae, m., = Ὕλας, a beautiful youth of Oechalia' in line:
          pass
        elif 'lactĭculārĭus, ‡ lactĭculōsus, λιπογάλακτος,' in line:
          pass
        elif 'pondĕrĭtas, ātis, f. pondus, weight: hominis (or nominis),' in line:
          pass
        elif 'Rhamses, is (or ae), m., an ancient' in line:
          pass
        elif 'Sīon, ōnis (or indecl.), m., f.' in line:
          pass
        elif d[0] == 'for':
          pass
        elif d[0] in {'archaic', 'correctly', 'also', 'or', 'better', 'better,', 'arch.'}:
          if d[1] == 'separately':
            d[1] = ''
          if '(or -οί)' not in line and '(or instruments)' not in line:
            if 'dŭŏdē-vīcēsĭmus (or viges-), a, um, ordin.' in line:
              d[1] = '-viges-'
            if d[1]:
              g.g('parenth..guessing', [d[1],line], True)
              add(apply_change(original, d[1]), entry)
        else:
          g.g('len d is 2, omitting', d + [line], True)
      elif len(d) > 2:
        if d[0] == 'falsely' or c.startswith('the form'):
          g.g('skippinig falsely or form', [d[0],line],True)
        elif b:=re.search('^less correctly written (\S+)[\s,]*',c):
          g.g('less correctly written',[b.group(1),line],True)
          add(apply_change(original, b.group(1)), entry)          
        elif b:=re.search('^less correctly ([\w-]+)[\s,]*',c):
          # (less correctly fēn-, foen-)
          # (less correctly fēn-, foen-, -tius)
          change = b.group(1).replace(';','')
          #rĕpello, reppuli (less correctly repuli)
          if n(change).endswith('i') and n(original).endswith('o'):
            # Guessing this is a third principle part and
            # rejecting it.
            g.g('less correctly-rejected', [original,change,line],True)
            change = ''
          else:
            add(apply_change(original, change), entry)
          change2=change3=''
          #Genāva (less correctly Genna or Genēva), ae, 
          #..(less correctly hoedus, and archaic aedus or ēdus;
          #neglĕgo (less correctly neglĭgo and neclĕgo),
          if b:=re.search('^less correctly \S+( or|, and archaic| and|,) ([\w-]+)', c):
            change2 = b.group(2)
            if change2 in ['v', 'not', 'and']:
              change2 = ''

            elif '-' in change2 or (original[0].islower() and change2[0].islower()) or (change2[0].isalpha() and n(change2)[0].lower() == n(original)[0].lower()):
              add(apply_change(original, change2), entry)
            else:
              change2=''
          #faenĕrātĭcĭus (less correctly fēn-, foen-, -tius),
          if b:=re.search('^less correctly \S+(, and archaic|,) \S+( or|,) ([\w-]+)',c):
            change3 = b.group(3)
            if change3 in ['v', 'not']:
              change3 = ''
            #if '-' in change3:
            add(apply_change(original, change3), entry)
            #else:
            #  change3 = ''
          g.g('less correctly',[change,change2,change3,line],True)
        elif b:=re.search('^collat\. form (\S+?),',c):
          g.g('collat form', [b.group(1),line], True)
          #add(apply_change(original, b.group(1)), entry)
          pass
          ##### SKIPPING: IT MIGHT BE MORE HELPFUL NOT TO RECORD THE COLLATERAL FORM #####
        elif b:=re.search('^or better, (\S+)',c):
          g.g('or better', [b.group(1),line],True)
          add(apply_change(original, b.group(1)), entry)
        elif b:=re.search('in the best MSS\. (also ){0,1}([\w-]+)',c):
          g.g('in the best MSS., guessing', [b.group(2),line], True)
          add(apply_change(original, b.group(2)), entry)
        elif b:=re.search('in MSS\. sometimes ([\w-]+)',c):
          ## PROBABLY SKIP THIS ONE ##
          ##         turn off       ##
          ## IT TURNS CUR INTO COR  ##
          change2 = ''
          if z:=re.search('in MSS\. sometimes [\w-]+ or ([\w-]+)', c):
            change2 = z.group(1)
          g.g('in MSS sometimes', [b.group(1), change2, line],True)
          #add(apply_change(original, b.group(1)), entry)
          if change2:
            #add(apply_change(original, change2), entry)
            pass
        elif b:=re.search('in many MSS\. also( written)* ([\w-]+)',c):
          g.g('in many MSS also written', [b.group(2),line],True)
          add(apply_change(original, b.group(2)), entry)
        elif b:=re.search('also ([\w-]+) and ([\w-]+)',c[0:160]):
          #(also ante- and postclass. form gnārŭris,
          change3=change4=''
          if any(i in ['ante-','postclass.','separately'] for i in [b.group(1), b.group(2)]):
            # Skip
            pass
          else:
            add(apply_change(original, b.group(1)), entry)
            add(apply_change(original, b.group(2)), entry)
            # (also -găno and -găbo, or -găvo, -găo, ōnis, m.
            if z:=re.search('also [\w-]+ and [\w-]+, or ([\w-]+), ([\w-]+),',c[0:160]):
              change3=z.group(1)
              change4=z.group(2)
              add(apply_change(original, change3), entry)
              add(apply_change(original, change4), entry)
            g.g('also___and___', [b.group(1), b.group(2), change3,change4,line],True)
        elif b:=re.search('^anciently written (\S+)',c):
          g.g('anciently written', [b.group(1), line],True)
          add(apply_change(original, b.group(1)), entry)
        elif b:=re.search('^less cor\. rectly (\S+)',c):
          g.g('less cor_rectly', [b.group(1),line],True)
          add(apply_change(original, b.group(1)), entry)
        elif b := re.search('(\S+) or (\S+)',c):
          if len(d) == 3 and any(w.startswith('(') for w in first_words(entry)[0:6]): 
            # Only these two words are parenthzd
            g.g('parenth __ or __', [b.group(1), b.group(2), line], True)
            add(apply_change(original, b.group(1)), entry)
            add(apply_change(original, b.group(2)), entry)
          else:
            # Could revisit this later but it produces
            # almost nothing usable so skip these safely.
            g.g('(___ or ___ .. but len d was not 3, skip',[c,b.group(1),b.group(2),line],True)
        elif b:=re.search('^sync\. (\S+) and (\S+)',c):
          g.g('sync ___ and ___', [b.group(1), b.group(2),line], True)
          add(apply_change(original, b.group(1)), entry)
          add(apply_change(original, b.group(2)), entry)
        else:
          if (d[0].endswith(',') or d[0].endswith(';')) and any ( w.startswith('(') for w in first_words(entry)[0:6]):
            word = d[0][:-1]
            if n(word) in {'better','f.', 'poet.','also','trisyl.',
                       'rare', 'idis', 'post-aug.',
                          'ante-class.','or',
                          'li', 'us', 'o',
                          'in', 'is'}:
              pass
            elif (n(word).endswith('i') or n(word).endswith('um') or n(word).endswith('us')) and n(original).endswith('o'):
              pass
            elif '-' in word:
              # keep it
              g.g('keeping first w in pathen due to dash',
                 [word,line],True)
              add(apply_change(original,word),entry)
            elif sim(n(original), n(word)) <= 25.0:
              g.g('rejectin first w in parenth pct',
                 [original,word,entry],True)
            else:
              g.g('Guessing due to Comma or Semicolon:',
                  [str(sim(n(original),
                  n(d[0][:-1]))),original,
                   d[0][:-1], line], True)
              add(apply_change(original, d[0][:-1]), entry)
          elif d[0] == 'v.' or d[0] == 'cf.':
            g.g('v or cf, passing', [line], True)
          elif c.startswith('a different orthography for'):
            g.g('passing, a diff ortho for', [line], True)
          elif '.' in c or len(d)>10:
            g.g('guessing to skip due to periods or more than 10', [line], True)
            pass
          else:
            g.g('error-len d is more, no periods..', d + [line],
               True)
    

def examine_subsequent_additions(line):
  entry = line
  line = repair_dashed_first_word(line)
  # That's the end of the searching round.
  # The first and/or/also is done.
  # The parenthetical is done.
  # Now we need to delete parentheticals and examine
  # whether more 'and,also,or's are present.
  line=re.sub('\(.*?\)', '', line)

  if 'of or belonging' in line:
    line = re.sub('of or belonging', '', line)
  first = first_words(line)
  original = first[0]
  c = ' '.join(first)

  if b:=re.search('and more usu\. in the plur\.: (\S+),', line):
    g.g('and more usu in the pl', [b.group(1), line], True)
    add(apply_change(original, b.group(1)), entry)
  elif b:=re.search(', and ([\w-]+),', ' '.join(line.split()[0:8])):
    word = b.group(1)
    if n(word) == 'in':
      word=''
    elif n(word).endswith('um') and n(original).endswith('o'):
      pass
    elif n(word) in ['quando','in','ae']:
      pass
    elif sim(n(word), n(original)) < 30.0:
      pass
    else:
      g.g(', and S..', [str(sim(n(word), n(original))), b.group(1),line], True)
      add(apply_change(original, word), entry)

  # Examples for this;
  # ălo, ălŭi, altum, and ălĭtum, 3, v. a. ; alitus seems to have been first 
  # something like: if first endswith o and the and endswith um, and the word before the and
  # endswith um, skip.
  # For this:
  # Alcmaeo, Alcmaeon, ŏnis, and Alcmaeus, i, m. , = Ἀλκμαίων,
  # Just wading in.. if 1 is 1 more than 0, and followed by onis, then and, then anothe that
  # is one more than 0, then keep all three..
  # For this:
  # alternē, alternīs, and alternă, advv., v. alternus fin.
  # similarly: 'a, b, and c,' is a structure to pay attention to..
  if b:=re.search('^([\w-]+), ([\w-]+), (and|or|also) ([\w-]+),', line):
    d = [b.group(1), b.group(2), b.group(4)]
    result = []
    for item in d:
      if n(original).endswith('cox') and n(item) == 'cocis':
        continue
      if n(original).endswith('or') and n(item).endswith('ri') and ' dep.' in line:
        g.g('excluding deponent', [item,line], True)
        continue
      if n(original).endswith('cor') and n(item) == 'coris':
        g.g('excluding 3rd decl', [item,line], True)
        continue
      if item.startswith('-'):
        if n(item).endswith('us') and n(original).endswith('or'):
          g.g('excluding deponent', [item,line], True)
          continue
        else:
          result.append(item)
        continue
      if n(item) in {'ae', 'ii', 'ivi', 'e', 'a', 'es', 'i', 'indecl.', 'are', 'ire', 'ere',
                    'um', 'onis', 'orum', 'ii', 'adv.', 'etis', 'is',
                    'arum', 'ium', 'eris', 'opis', 'icui', 'ixi', 'o', 'ontis',
                    'itis', 'oris', 'teris', 'tri', 'adj.', 'idis', 'elis', 'enis',
                    'uis', 'us', 'inis', 'otis', 'bui', 'adis', 'abl.', 'acis'}:
        # skip this one
        g.g('rejected a,b,and c', [item,line], True)
        continue
      result.append(item)
    #result.append(line)
    g.g('a, b, and c,', result + [line], True) 
    for item in result:
      original = apply_change(original, item)
      add(original, entry)
    # Once we're this deep we should also check for
    # items like:
    # albĭcēris, e, or albĭcērus, a, um, also albĭcērātus, a, um, adj. 
    # Tĭbĕris, is, also contr., Tibris , is or ĭdis,
    # FOR LATER.
    
  elif 'or' in first or 'and' in first and (first[1] not in {'or', 'and', 'also'}):
    if len(first) < 3:
      return
    if first[2] == 'or' or first[2] == 'and':
      if 'ivi or ii' in n(c):
        pass
      elif n(first[1]).endswith('urri') and n(first[3]).endswith('urri') and n(first[0]).endswith('o'):
        pass
      elif n(first[0]).endswith('or') and n(first[1]).endswith('us') and n(first[3]).endswith('us'):
        pass
      elif b:=re.search(' or (\w+) or (\w+) ',c):
        g.g('or __ or ____', [b.group(1), b.group(2), line], True)
        for item in [b.group(1), b.group(2)]:
          original = apply_change(original, item)
          add(original, entry)
      elif len(first[3]) >= len(first[0]) and n(first[3][0:len(first[0])-2]) == n(first[0][0:len(first[0])-2]):
        if '.' in first[3]:
          pass
        elif n(first[3])[-2] in {'um', 'us'} and n(original).endswith('o'):
          pass
        elif n(first[3]).endswith('i') and n(original).endswith('o'):
          pass
        else:
          g.g('measuring trick', [first[3], line], True)
          add(apply_change(original, first[3]), entry)
      else:
        g.g('no solution found after __ or', [line], True)
        pass
    # LEFT OFF HERE
    if re.search('\w+ \w+ (and|or) \w+ \w+',line):
      #print('guessing to EXCLUDE:',line[0:80],'\n')
      #reject(line)
      pass

# Start of program
g=Guess() # Initialize guess logging
n = lambda string : normalize(string) # quick code for accent removal

dictionary = {} # Where we store all our headwords and entries.
# NB for a word like 'a,ab,abs, prep, 'from', etc...', we will create
# three entries in 'dictionary', one for a, one for ab, one for abs.
# Then, in the final lines of the program, we can output / save this 
# in whatever manner is convenient or desired. The VALUES in this 
# dictionary will be stored as a list[] because
# one headword may link to multiple L&S dictionary entries.

# Open and read Lewis and Short text dictionary.
with open(INPUT_FILE, 'r') as f:
  ls_input = f.read().splitlines()

print(f'{INPUT_FILE} opened. {len(ls_input)} lines in file. Scanning..')

remainders = []
entry_count = 0
start = False

# Begin main parsing loop.

# This will examine each entry and make some initial guesses.
# It will subsequently call examine_or_also_and_with_parenth()
# and examine_subsequent_additions() for different kinds of
# analysis. Along the way, any headword variations are stored
# as keys in dictionary{} pointing to a list: Since one headword
# can of course point to multiple dictionary entries, the
# dictionary value is stored as a list. Each entry pointed to
# by an already existing headword is added to the list.
for line in ls_input:
  if line.strip() == 'A':
    start = True
  if not start:
    continue
  if len(line.strip()) == 1: # Each new letter of the alphabet is introduced
    print(line)
    continue                 # by a line with a single letter.

  # This is if the whole entry is in parentheses.
  if line.startswith('('):
    line = line[1:-1]

  if line.startswith('-'):
    # Skip these for now.
    continue

  # if the line starts with space, or a special ch.
  if line:
    while not line[0].isalpha():
      line=line[1:]

  entry_count += 1
    
  if 'condictīcĭus- or tĭus, a, um' in line:
    line = re.sub('condictīcĭus- or tĭus', 'condictīcĭus or -tĭus', line)
  if 'Iālysus- or -os, i, m.' in line:
    line = re.sub('Iālysus- or -os, i, m.', 'Iālysus or -os, i, m.', line)
  if 'īcĭo and īco), īci, ictum' in line:
    line = re.sub('īcĭo and īco\), īci, ictum', 'īcĭo and īco, īci, ictum', line)
  
  entry = line
  line = repair_dashed_first_word(line)
  first = first_words(line)

  if 'dextrorsum or dextrorsus, or uncontracted dextrovorsum (or -ver-sum), adv.' in line:
    add('dextrorsum', entry)
    add('dextrorsus', entry)
    add('dextrovorsum', entry)
    add('dextroversum', entry)
    continue
  if 'ăb, ā, abs, prep. with abl.' in line:
    add('ăb', entry)
    add('ā', entry)
    add('abs', entry)
    continue

  # File away the first word
  g.g('first_word', [first[0],line], True)
  first_keyword = first[0]
    
  if '.' in first_keyword:
    first_keyword = first_keyword.replace('.','')
  if ':' in first_keyword:
    first_keyword = first_keyword.replace(':', '')

  if first_keyword.strip().endswith('-'):
    # Many entries are just explanations of prefixes. We will not include these
    # for now.
    continue

  if '-' in first_keyword:
    first_keyword = first_keyword.replace('-', '')
  if '/' in first_keyword:
    first_keyword = first_keyword.replace('/', '')
  
  add(first_keyword, entry)

  # There are two of these.
  if b:=re.search('and usu\. plur\. (\w+)', line):
    add(b.group(1), entry)

  # File away potential other words in the header:
  # a or b, and c, sometimes d, etc
  # a or b (c or d) et alia
  examine_or_also_and_with_parenth(entry)

  # and this looks for or/and/also that comes after all that.
  examine_subsequent_additions(entry)
# End of for loop

print(f'Completed scan of {INPUT_FILE}.')
print(f'{entry_count} dictionary entries processed.')
print(f'{len(dictionary)} headwords and variations of headwords found.')
count = sum(len(dictionary[item]) for item in dictionary)
print(f'These headwords effect {count} citations.')
print('')

note = '(One entry can be cited by multiple headwords, and one headword can cite multiple entries. E.g. five entries are cited by "a", one of which is also cited by both "ab" and "abs", and another by "ah", thus in five entries, there are four headwords, and eight citations.)'

import textwrap
print('\n'.join(textwrap.wrap(note, width=60)) + '\n')

# Write the dictionary to a JSON file
import json
with open(JSON_RESULT_FILE, 'w') as json_file:
    d = {}
    for key in dictionary:
      d[key] = list(dictionary[key])
    json.dump(d, json_file, indent=4)
    print(f"Saved to {JSON_RESULT_FILE}.")

# now flip the dictionary inside out, and save as text
# file per notes above.
result = {}
for key, values in dictionary.items():
    for item in values:
        result.setdefault(item, []).append(key)

with open(TEXT_RESULT_FILE, 'w') as f:
  for key, values in result.items():
    # File format: pairs of lines.
    # Line1: # followed by comma,separated,keywords
    # Line2: entry these keywords point to.
    f.write(f'#{",".join(values)}\n{key}\n')

print(f'Saved to {TEXT_RESULT_FILE}.')

# Verify results

KEYWORD = 'dŭcentĭens' # This is a variant of a listed headword.

print('')
print(f'Verifying JSON file, searching for {KEYWORD}:')

import json
with open(JSON_RESULT_FILE, 'r') as json_file:
    loaded_dict = json.load(json_file)
print(loaded_dict['dŭcentĭens'])


LS_DICTIONARY = {}
lines = 0
with open(TEXT_RESULT_FILE, 'r') as f:
  content = f.read().splitlines()

  for line in content:
    lines += 1
    line = line.strip()
    if line.startswith('#'):
      # This is a keyword line.
      keywords = dict.fromkeys(keyword for keyword in line[1:].split(','))
    else:
      # This is an entry line.
      for keyword in keywords:
        if keyword not in LS_DICTIONARY:
          LS_DICTIONARY[keyword] = []
        LS_DICTIONARY[keyword].append(line)


print('')
print(f'Verifying text file, searching for {KEYWORD}:')
#dŭcentĭes or -ĭens
print(LS_DICTIONARY['dŭcentĭens']) # Again, should find the variant.

print('')
print('Execution complete.')
