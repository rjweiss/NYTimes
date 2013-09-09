import os
import sys
import json
from collections import defaultdict
from lxml import etree
#import prettyprint
import random

def tree():
    return defaultdict(tree)

def inc(t):
    if not t.has_key('size'):
        t['size'] = 1
    else:
        t['size'] += 1
                        
def add(t, keys):
    for key in keys:
        inc(t)
        t = t[key]
    inc(t)


def d3ify(key, val):
    '''
    Takes in a tree with a taxonomic classifier structure and with associated counts of observations in a given NYT subset
    Produces an object that can be dumped into JSON structure expected by d3.js default dendrogram and sunburst examples.
    
    @param key: empty string
    @type key: string
    @param val: a tree of taxonomic structure
    @type val: tree
    @rtype: defaultdict
    @return: a defaultdict of d3 format
    
    
    '''
    node = defaultdict()
    node['name'] = key
    node['children'] = [d3ify(k, v) for k, v in val.iteritems() if k != 'size'] #otherwise halts at int
    
    if val.has_key('size'):
        node['size'] = val['size']

    return node
    
def etcMLify(taxonomic_label, body_string, data_dir, filename):
    '''
    Creates directory of taxonomic labels and related NYT articles
    This is the .zip file directory format expected by etcML
    
    @param filename: current file to be added to etcML data directory
    @type filename: string
    @param data_dir: home directory of NYT Anno Corpus
    @type data_dir: string
    @param body_string: full_text of current file
    @type body_string: string
    @param taxonomic_label: the taxonomic label of current file
    @type taxonomic_label: string
    '''
    
    etcML_label = '_'.join(taxonomic_label.split('/')).replace(' ','_')
    etcMLdir = os.path.join(data_dir + 'etcML' + os.sep + etcML_label)

    if not os.path.exists(etcMLdir):
        try:
            os.makedirs(etcMLdir)
        except OSError:
            print "Skipping creation of %s because it exists already." % etcMLdir
    
    with open(os.path.join(etcMLdir + os.sep + filename.split('.')[0] + '.txt'), 'wb' ) as outfile:
        outfile.write(body_string)

def main(date_dir, data_dir):
    
    classifier_tree = tree()
    
    for root, dirs, infiles in os.walk(date_dir):
        for infile in infiles:            
            if infile.endswith('.xml'):
                nytfile = os.path.join(root, infile)
                
                try:
                    with open(nytfile, 'rb') as nytfile:
                        parsetree = etree.parse(nytfile)
                except IOError as e:
                    print "I/O error({0}): {1}".format(e.errno, e.strerror)
                    
                docroot = parsetree.getroot()
                nytfile_body = ' '.join(map(str, docroot.xpath("body/body.content/block[@class='full_text']/p/text()")))
                classifiers = docroot.findall('head/docdata/identified-content/classifier')
                
                for el in classifiers:               
                    if el.attrib['type'] == 'taxonomic_classifier':
                        keys = el.text.split('/')
                        add(classifier_tree, keys)
                        
                        tossup = random.randint(1, 4)
                        if len(keys) == 3 and tossup == 1: #h4x0r random sampling, etcML only takes 50mb archives for now
                            etcMLify(el.text, nytfile_body, data_dir, infile)
                            
    d3ified_tree = d3ify('', classifier_tree)
            
    with open(os.path.join(date_dir +  '_data.json'), 'w') as outfile:
        json.dump(d3ified_tree, outfile)
#    
if __name__ == '__main__':
       
#    data_dir = sys.argv[1]
    data_dir = '/Users/rweiss/Documents/nytimes_data/'
    for f in os.listdir(data_dir):
        if len(f) == 4: #make sure it's the directories that are year-length
            year_dir = os.path.join(data_dir, f)
            print 'Beginning year ' + f
            main(year_dir, data_dir)
            break #test a single year
