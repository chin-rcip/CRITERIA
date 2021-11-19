import rdflib
from rdflib import Graph, URIRef, Namespace, util
from rdflib.util import SUFFIX_FORMAT_MAP
from rdflib.namespace import NamespaceManager, RDFS, RDF, XSD
import re
import sys
import argparse

try:
	from src import source
except ImportError:
	from CRITERIA.src import source


# Function to build a dictionary of an ontology's classes and their superclasses.
# For instances, the returned object (clss) would look like this:
# 	clss = {
# 			'E21_Person': ['E39_Actor',
# 	                    'E20_Biological_Object',
# 	                    'E19_Physical_Object',
# 	                    'E18_Physical_Thing',
# 	                    'E72_Legal_Object',
# 	                    'E92_Spacetime_Volume',
# 	                    'E1_CRM_Entity'],
#  			'E22_Human-Made_Object': ['E19_Physical_Object',
# 	                           'E24_Physical_Human-Made_Thing',
# 	                           'E18_Physical_Thing',
# 	                           'E71_Human-Made_Thing',
# 	                           'E70_Thing',
# 	                           'E77_Persistent_Item',
# 	                           'E1_CRM_Entity']}

def superClass(ontology):
	inFormat = util.guess_format(ontology)
	g = Graph()

	if not "http" in ontology:
		g.parse('./src/ontologies/{}'.format(ontology), format=inFormat)
	else:
		g.parse(ontology, format=inFormat)

	prefix = source.prefix
	for pf in prefix:
		ns = Namespace(prefix[pf])
		g.bind(pf, ns)

	
	clss = {}
	for c in g.subjects(RDF.type, RDFS.Class):
		spcList = []
		l = 0	# l is the level/depth of the hierarchy
		while l <= 9: 
			if l == 0:
				sc = c
			for spc in g.objects(sc, RDFS.subClassOf):
				spcList.append(spc.n3(g.namespace_manager).split(':')[1])
				sc = spc
			l += 1
		clss[c.n3(g.namespace_manager).split(':')[1]] = spcList
	return clss


# Function to build a dictionary of an ontology's classes and their Mermaid classes, i.e. main CIDOC-CRM classes.
# For instances, the returned object (d) would look like this:
	# d = {'E10_Transfer_of_Custody': 'Temporal_Entity',
	# 	 'E11_Modification': 'Temporal_Entity',
	# 	 'E12_Production': 'Temporal_Entity',
	# 	 'E1_CRM_Entity': 'CRM_Entity',
	# 	 'E20_Biological_Object': 'Physical_Thing',
	# 	 'E21_Person': 'Actor',
	# 	 'E22_Human-Made_Object': 'Physical_Thing'}

def classDict():
	d = {}
	classes = source.classes
	onto = source.onto
	
	for ontology in onto:
		core = onto[ontology]['core']
		coreClass = superClass(core)
		for sc in coreClass:
			for spc in coreClass[sc]:
				if spc in classes:
					d[sc] = spc
					break 
					# exit loop after the first superclass is found in the classes list.
					# e.g. for 'E21_Person' the first superclass found in the classes list
					# is E39_Actor

		if 'extensions' in onto[ontology]:
			for key in onto[ontology]['extensions']:
				ext = onto[ontology]['extensions'][key]
				extClass = superClass(ext)
				for ent in extClass:
					if ent in coreClass:
						for spc in coreClass[ent]:
							if spc in classes:
								d[ent] = spc
								break
					elif len(extClass[ent]) > 0:
						crmSpc = extClass[ent][-1] # retrieve the last/highest superclass of an extension class.
						if crmSpc in classes:
							d[ent] = crmSpc
						elif crmSpc in coreClass:
							for spc in coreClass[crmSpc]:
								if spc in classes:
									d[ent] = spc
									break

	for c in classes:
		d[c] = c
	return d

# Function to convert RDF triples to Mermaid statements.
# Returns a list of statements
def convert(rdfInput):
	inFormat = util.guess_format(rdfInput)
	g = Graph()
	g.parse(rdfInput, format=inFormat)

	classes = classDict()

	objList = []
	stmtList = []

	uriDict = {}
	stmtList = []
	doubleInst = [] # to check for URI with double instantiations
	i = 0
	for s,p,o in g.triples((None, None, None)):
		p = p.n3(g.namespace_manager)
		if s in uriDict:
			n1 = uriDict[s]
		else:
			n1 = i
			i += 1
			if isinstance(s, rdflib.URIRef) or isinstance(s, rdflib.BNode):
				uriDict[s] = n1

		if o in uriDict:
			n2 = uriDict[o]
		else:
			n2 = i
			i += 1
			if (isinstance(o, rdflib.URIRef) or isinstance(o, rdflib.BNode)) and p != 'rdf:type':
				uriDict[o] = n2

		# check whether the object of the triple is a key in the returned dict of classDict
		# to retrieve the Mermaid class, i.e check for the object of the property rdf:type
		if p == 'rdf:type':
			c = o.n3(g.namespace_manager).split(':')[1]
			if c in classes:
				cl = classes[c]
			else:
				cl = 'Default'
			if not s in doubleInst:
				doubleInst.append(s)
				uriCl = cl+'_URI'
			else:
				uriCl = 'Multi_URI'
			stmt = '{}([{}]):::{} -->|{}| {}[{}]:::{}'.format(n1,
										s.n3(g.namespace_manager),
										uriCl,p,
										n2,
										o.n3(g.namespace_manager),
										cl)

		elif '"' in o.n3(g.namespace_manager):
			cl = 'Literal'
			stmt = '{}([{}]) -->|{}| {}([{}]):::{}'.format(n1,
										s.n3(g.namespace_manager),
										p,
										n2,
										o.n3(g.namespace_manager),
										cl)

		else:
			stmt = '{}([{}]) -->|{}| {}([{}])'.format(n1,
										s.n3(g.namespace_manager),
										p,
										n2,
										o.n3(g.namespace_manager))

		stmtList.append(stmt)
	return stmtList

# Function to generate mermaid.jd style class definition based the classes dict from source.py
def template():
	template = "graph TD\n"
	classes = source.classes
	for c in classes:
		template += "classDef {} fill:{},stroke:{};\n".format(c,classes[c]["classColor"],classes[c]["classStroke"])
		template += "classDef {}_URI fill:{},stroke:{};\n".format(c,classes[c]["instanceColor"],classes[c]["instanceStroke"])
	return template

# Main function to convert a RDF turtle files to Mermaid with instances.
def instance(rdfInput, mmdOutput):
	read = template()
	out = open(mmdOutput, "w", encoding="utf-8")
	out.write(read)

	stmtList = convert(rdfInput)
		
	for stmt in stmtList:
		stmt = stmt.replace('"',"''").replace('[','["').replace(']','"]')
		stmt = stmt.replace('(["<','(["').replace('>"])','"])')
		stmt = stmt.replace('|<','|"').replace('>|','"|').replace('--"','-->')
		out.write(stmt+'\n')

# Main function to convert a RDF turtle files to Mermaid, but only the classes represented, without the instances,
# by replacing the uri with the classes in Mermaid statements.
def ontology(rdfInput, mmdOutput):
	read = template()
	out = open(mmdOutput, "w", encoding="utf-8")
	out.write(read)

	uriType = {}
	statements = []
	
	stmtList = convert(rdfInput)
	for stmt in stmtList:
		stmt = stmt.replace('"',"''").replace('[','["').replace(']','"]')
		stmt = stmt.replace('(["<','([').replace('>"])','])')
					
		date = re.findall('\(\[".*\^xsd:dateTime"]\)', stmt)
		lit = re.findall('\(\["\'\'.*\'\'.*"]\)', stmt)
		if date:
			stmt = stmt.replace(date[0], '[xsd:dateTime]')
		elif lit:
			stmt = stmt.replace(lit[0], '[rdfs:Literal]')
		if 'rdf:type' in stmt:
			inst = re.findall('\(\[.*:.*\)', stmt)[0] # get the uri part
			clType = '[' + re.findall('\|.*\[".*"\].*', stmt)[0].split('[')[1] # get the class part
			# add to the uriType dict the uri part as the key, and the class part as the value
			# so the class part will replace the uri part in the for loop below
			if not inst in uriType:
				uriType[inst] = clType
			# else if uri is already in uriType, indicating multi instantiations,
			# update the value of the 'inst' key by append the second class with <br> betwwen them
			# so that all classes are in the same box/node
			else:
				clType = clType.split('["')[1].split(']')[0]
				multi = uriType[inst].split('"]')[0] + '<br>' + clType + ']:::Multi'
				uriType[inst] = multi
				
		elif not 'rdfs:label' in stmt:
			statements.append(stmt)

	for stmt in statements:
		key1 = re.findall('\(\[.*:.*\) ', stmt)[0].split(' ')[0]
		stmt = stmt.replace(key1, uriType[key1])
		key2 = re.findall('\(\[.*:.*\)', stmt)
		if key2:
			key2 = key2[0]
			stmt = stmt.replace(key2, uriType[key2])
		out.write(stmt+'\n')


def main(Type, rdf, mmd,):
	SUFFIX_FORMAT_MAP["rdfs"] = "xml"
	SUFFIX_FORMAT_MAP["json"] = "json-ld"
	if Type == 'instance':
		instance(rdf, mmd)
	elif Type == 'ontology':
		ontology(rdf, mmd)
	print('Success!')

# argparse arguments
def parse_args():
	parser = argparse.ArgumentParser(description='Convert CidocCRM-based RDF to Mermaid')

	parser.add_argument("Type", help='The type of the diagram', choices=['instance', 'ontology'])
	parser.add_argument("rdf", help='RDF input filename including path_to_file')
	parser.add_argument("mmd", help='Mermaid output filename including path_to_file')

	args = parser.parse_args()
	return args

if __name__ == '__main__':
	args = parse_args()
	main(args.Type, args.rdf, args.mmd)
