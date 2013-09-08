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
    
def main():

    workpath = '/Users/rweiss/Downloads/nytimes/1992/01/'
    
    classifier_tree = tree()

    for root, dirs, infiles in os.walk(workpath):
        for infile in infiles:
            
            if infile.endswith('.xml'):
                fullpath = os.path.join(root, infile)
            
                parsetree = etree.parse(open(fullpath, 'rb'))
                docroot = parsetree.getroot()
    
                classifiers = docroot.findall('head/docdata/identified-content/classifier')
                
                for el in classifiers:
                    
                    if el.attrib['type'] == 'taxonomic_classifier':
                        #with open('teststring.txt', 'a') as outfile:
                        #    writeline = el.text + '\n'
                        #    outfile.write(writeline)
                        keys = el.text.split('/')
                        add(classifier_tree, keys)
     
    d3ified_tree = d3ify('', classifier_tree)

    with open(os.path.join(workpath +  'testdata.json'), 'w') as outfile:
        json.dump(d3ified_tree, outfile)
    
if __name__ == '__main__':
    main()
