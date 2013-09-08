import os, sys
import json
from collections import defaultdict, Counter
from lxml import etree

workpath = '/Users/rweiss/Downloads/nytimes/1992/'

#taxonomic_classifiers = Counter()

classifier_tree = {}

for root, dirs, infiles in os.walk(workpath):
    for infile in infiles:
        
        if infile.endswith('.xml'):
            fullpath = os.path.join(root, infile)
            print fullpath
        
            tree = etree.parse(open(fullpath, 'rb'))
            docroot = tree.getroot()

            classifiers = docroot.findall('head/docdata/identified-content/classifier')
#            classifier_attributes = [dict(el.attrib) for el in classifiers]
            
            for el in classifiers:
                
                if el.attrib['type'] == 'taxonomic_classifier':
                    children = classifier_tree
                    
                    #print 'root = ' + el.text
                    
                    for idx, val in enumerate(el.text.split('/')):
                        #print val
                        if val not in children.keys():
                            children[val] = {}
                            children[val]['name'] = val
                            children[val]['size'] = 1
                            children[val]['children'] = {}
                        else:
                            children[val]['size'] = children[val]['size'] + 1
                        children = children[val]['children']
                       
#                    taxonomic_classifiers[el.text] += 1
                    #break
        #break
        
import sys

f = open('data1992.json', 'w')

def pad(n):
    for i in range(0, n):
        f.write(' ') 


def traverse(node, indent):
    numKeys = len(node.keys())
    i = 0
    for el in node.keys():
        pad(indent)
        f.write('{ "name": "' + el + '", "size": %d' % node[el]['size'])
        if len(node[el]['children']) > 0:
            f.write(', "children": [ \n')
            traverse(node[el]['children'], indent + 4)
            pad(indent)
            f.write(']}')
        else:
            f.write(' }')

        i += 1
        if i < numKeys:
            f.write(',')
        f.write('\n')
            
traverse(classifier_tree, 0)

f.close()
