from Bio import Phylo
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

def makeXML(node, filename):
    '''
    Take a root node and make an XML file for biopython to make a tree out of
    Mattias Park
    '''

    def recurseSubElements(parent, node, branch_length=0):
        '''
        Recursive method to make ElementTree subelements
        '''

        # Make the subelement and set the branch length
        subclade = ET.SubElement(parent, 'clade')
        if branch_length != 0:
            # Branch length must be passed down from above
            subclade.set("branch_length", str( round(float(branch_length), 2) ) )
            # Rounding is to get rid of ugly floating point errors but probably not really necessary

        # add a <name> tag
        subclade_name = ET.SubElement(subclade, 'name')
        subclade_name.text = node.name

        # Recurse on each child
        if node.left is not None:
            recurseSubElements(subclade, node.left, node.left_height()) 
        if node.right is not None:
            recurseSubElements(subclade, node.right, node.right_height())

    # XML header
    header = b'<?xml version="1.0" encoding="UTF-8"?>'

    phyloxml = ET.Element('phyloxml')
    phyloxml.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    phyloxml.set('xsi:schemaLocation', 'http://www.phyloxml.org http://www.phyloxml.org/1.10/phyloxml.xsd')
    phyloxml.set('xmlns', 'http://www.phyloxml.org')

    phylogeny = ET.SubElement(phyloxml, 'phylogeny')
    phylogeny.set('rooted', 'true')

    recurseSubElements(phylogeny, node)

    # Write to file
    myfile = open(filename, "wb")

    myfile.write(header)
    myfile.write(b'\n')

    xml_string = ET.tostring(phyloxml)
    myfile.write(xml_string)
    myfile.write(b'\n')

def makeXML_blank(filename):

    # XML header
    header = b'<?xml version="1.0" encoding="UTF-8"?>'

    phyloxml = ET.Element('phyloxml')
    phyloxml.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    phyloxml.set('xsi:schemaLocation', 'http://www.phyloxml.org http://www.phyloxml.org/1.10/phyloxml.xsd')
    phyloxml.set('xmlns', 'http://www.phyloxml.org')

    phylogeny = ET.SubElement(phyloxml, 'phylogeny')
    phylogeny.set('rooted', 'true')

    clade = ET.SubElement(phylogeny, 'clade')

    # Write to file
    myfile = open(filename, "wb")

    myfile.write(header)
    myfile.write(b'\n')

    xml_string = ET.tostring(phyloxml)
    myfile.write(xml_string)
    myfile.write(b'\n')


def makePNG(XML, filename):
	tree = Phylo.read(XML, "phyloxml")
	Phylo.draw(tree, do_show=False)
	plt.savefig(filename)

# A3 final tree for testing
"""
boboer = Node('S13245', 5.9,
              Node('S1325', 5.3, 
                Node('S132', 2.7,
                    Node('S13', 2.0,
                        Node('S1', 0),
                        Node('S3', 0)),
                    Node('S2', 0)),
                Node('S5', 0) ),
              Node('S4', 0))
#makeXML(boboer, 'test.xml')
"""