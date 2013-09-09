import os, sys
import json
from collections import defaultdict
from lxml import etree
import prettyprint

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
    takes tree nodes and returns in d3 format
    '''
    node = defaultdict()
    node['name'] = key
    node['children'] = [d3ify(k, v) for k, v in val.iteritems() if k != 'size']
    
    if val.has_key('size'):
        node['size'] = val['size']

    return node

def create_d3_tree(fullpath, classifier_tree):
    
    with open(fullpath, 'rb') as nytfile:
        parsetree = etree.parse(nytfile)
                    
    docroot = parsetree.getroot()
    classifiers = docroot.findall('head/docdata/identified-content/classifier')
                
    for el in classifiers:
        if el.attrib['type'] == 'taxonomic_classifier':
            add(classifier_tree, el.text.split('/'))
     
    d3ified_tree = d3ify('', classifier_tree)
    
    return d3ified_tree
    
def main():

    #workpath = 'path/to/data/dir'
    workpath = '/Users/rweiss/Documents/nytimes_data/'
    
    for root, dirs, infile in os.walk(workpath):
        
        current_year = root[-(len(root)-len(workpath)):len(root)]
        print current_year
#        for el in os.listdir(workpath):
#            if os.path.isdir(el):
#                print 'year: ' + current_year
            
        #current_year = root.split('/')[-3]
        #print root
        #print 'wp: %d' % len(workpath)
        #print 'r: %d' % len(root)
        #print 'if: %d' % len(infile)
        #print current_year
        
#        for infile in infiles:
#            
#            if infile.endswith('.xml'):
#                fullpath = os.path.join(root, infile)
#                year = root.split('/')[-3]
#
#                classifier_tree = tree()
#
#                d3_tree = create_d3_tree(fullpath, classifier_tree)
#                
#                prettyprint.pp(d3_tree)
#                
#                #with open(os.path.join(workpath + 'nytdata' + year + '.json'), 'w') as outfile:
#                #    json.dump(d3_tree, outfile)
    
if __name__ == '__main__':
    main()
