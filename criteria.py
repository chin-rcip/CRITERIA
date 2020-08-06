from rdflib import Graph, URIRef, Namespace
from rdflib.namespace import NamespaceManager, RDFS, RDF, XSD
import re
import sys
import argparse
from src import source
from pprint import pprint


# Function to build a dictionary of an ontology's classes and their superclasses.
# For instances, the returned object (clss) would look like this:
# 	clss = {
# 			'crm:E21_Person': ['crm:E39_Actor',
# 	                    'crm:E20_Biological_Object',
# 	                    'crm:E19_Physical_Object',
# 	                    'crm:E18_Physical_Thing',
# 	                    'crm:E72_Legal_Object',
# 	                    'crm:E92_Spacetime_Volume',
# 	                    'crm:E1_CRM_Entity'],
#  			'crm:E22_Human-Made_Object': ['crm:E19_Physical_Object',
# 	                           'crm:E24_Physical_Human-Made_Thing',
# 	                           'crm:E18_Physical_Thing',
# 	                           'crm:E71_Human-Made_Thing',
# 	                           'crm:E70_Thing',
# 	                           'crm:E77_Persistent_Item',
# 	                           'crm:E1_CRM_Entity']}

def superClass(ontology, prefix, baseURL):
	g = Graph()
	g.parse('./src/ontologies/{}'.format(ontology))

	ns = Namespace(baseURL)
	g.bind(prefix, ns)
	if baseURL != 'http://www.cidoc-crm.org/cidoc-crm/':
		crm = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
		g.bind('crm', crm)
	
	clss = {}
	for c in g.subjects(RDF.type, RDFS.Class):
		spcList = []
		l = 0	# l is the level/depth of the hierarchy
		while l <= 9: 
			if l == 0:
				sc = c
			for spc in g.objects(sc, RDFS.subClassOf):
				spcList.append(spc.n3(g.namespace_manager))
				sc = spc
			l += 1
		clss[c.n3(g.namespace_manager)] = spcList
	return clss


# Function to build a dictionary of an ontology's classes and their Mermaid classes, i.e. main CIDOC-CRM classes.
# For instances, the returned object (d) would look like this:
	# d = {'crm:E10_Transfer_of_Custody': 'Temporal_Entity',
	# 	 'crm:E11_Modification': 'Temporal_Entity',
	# 	 'crm:E12_Production': 'Temporal_Entity',
	# 	 'crm:E1_CRM_Entity': 'CRM_Entity',
	# 	 'crm:E20_Biological_Object': 'Physical_Thing',
	# 	 'crm:E21_Person': 'Actor',
	# 	 'crm:E22_Human-Made_Object': 'Physical_Thing'}

def classDict():
	d = {}
	classes = source.classes
	# CIDOC-CRM
	cidocClass = superClass(source.onto['crm'], 'crm', 'http://www.cidoc-crm.org/cidoc-crm/')
	for sc in cidocClass:
		for spc in cidocClass[sc]:
			spc = spc.split(':')[1]
			if spc in classes:
				d[sc] = '_'.join(spc.split('_')[1:])
				break 
				# exit loop after the first superclass is found in the classes list.
				# e.g. for 'crm:E21_Person' the first superclass found in the classes list
				# is E39_Actor
	# FRBRoo
	frbrClass = superClass(source.onto['frbroo'], 'frbroo', 'http://iflastandards.info/ns/fr/frbr/frbroo/')
	for fr in frbrClass:
		crmSpc = frbrClass[fr][-1] # retrieve the last/highest cidoc-crm superclass of a frbroo class.
		for spc in cidocClass[crmSpc]:
			spc = spc.split(':')[1]
			if spc in classes:
				d[fr] = '_'.join(spc.split('_')[1:])
				break 
	# CRMDig
	digClass = superClass(source.onto['crmdig'], 'crmdig', 'http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/')
	for dig in digClass:
		crmSpc = digClass[dig][-1] # retrieve the last/highest cidoc-crm superclass of a crmdig class.
		for spc in cidocClass[crmSpc]:
			spc = spc.split(':')[1]
			if spc in classes:
				d[dig] = '_'.join(spc.split('_')[1:])
				break 
	# CRMpc
	pcClass = superClass(source.onto['pc'], 'crm', 'http://www.cidoc-crm.org/cidoc-crm/')
	for pc in pcClass:
		d[pc] = 'PC_Classes'

	for c in classes:
		d['crm:'+c] = '_'.join(c.split('_')[1:])

	return d

# Function to convert RDF triples to Mermaid statements.
# the returned objList will be the input subList when the function 
# is called again in the next loop.
def convert(subList,g,classes,i, uriDict):
	objList = []
	stmtList = []
	crm = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
	frbroo = Namespace('http://iflastandards.info/ns/fr/frbr/frbroo/')
	crmdig = Namespace('http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/')
	aat = Namespace('http://vocab.getty.edu/aat/')

	for idx, s in subList:
		count = 0 
		# to count number of classes assigned to an instance, i.e. double instanciations
		
		for p, o in g.predicate_objects(s):
			p = p.n3(g.namespace_manager)
			if o in uriDict:
				n = uriDict[o]
			else:
				n = i				
				if (not 'crm' in o.n3(g.namespace_manager) and 
					not 'frbroo' in o.n3(g.namespace_manager)):
				# if 'chin-rcip.ca' in o.n3(g.namespace_manager):
					uriDict[o] = i
					group = (i,o)
					objList.append(group)

			# check whether the object of the triple is a key in the returned dict of classDict
			# to retrieve the Mermaid class, i.e check for the object of the property rdf:type
			if o.n3(g.namespace_manager) in classes:
				cl = classes[o.n3(g.namespace_manager)]
				count += 1
				if count < 2:
					uriCl = cl+'_URI' # if not multi instanciations, Mermaid class is the node class + _URI
				else:
					uriCl = 'Multi_URI' # if multi instanciations
				stmt = '{}([{}]):::{} -->|{}| {}[{}]:::{}'.format(idx,
											s.n3(g.namespace_manager),
											uriCl,p,
											n,
											o.n3(g.namespace_manager),
											cl)
			# check for quotation marks in the object, indicating Literal values.
			elif '"' in o.n3(g.namespace_manager):
				cl = 'Literal'
				stmt = '{}([{}]) -->|{}| {}([{}]):::{}'.format(idx,
											s.n3(g.namespace_manager),
											p,
											n,
											o.n3(g.namespace_manager),
											cl)
				
			else:
				stmt = '{}([{}]) -->|{}| {}([{}])'.format(idx,
											s.n3(g.namespace_manager),
											p,
											n,
											o.n3(g.namespace_manager))
			stmtList.append(stmt)
			i += 1			
	return stmtList, objList, i, uriDict

# Main function to convert a RDF turtle files to Mermaid.
def instance(rdfInput, mmdOutput, uri, depth):
	template = open("./src/templates/instance.mmd", "r", encoding="utf-8")
	read = template.read()
	out = open('./mmd/{}'.format(mmdOutput), "w", encoding="utf-8")
	out.write(read)

	g = Graph()
	g.parse('./rdf/{}'.format(rdfInput) , format="turtle")

	# crm = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
	# frbroo = Namespace('http://iflastandards.info/ns/fr/frbr/frbroo/')
	# aat = Namespace('http://vocab.getty.edu/aat/')

	classes = classDict()

	u = URIRef(uri)

	i = 1
	lvl = 1 

	subList = [(0,u)]
	uriDict = {u: 0}
	while lvl <= int(depth):
		stmtList, subList, i, uriDict = convert(subList,g,classes,i,uriDict)
		
		for stmt in stmtList:
			stmt = stmt.replace('"',"''").replace('[','["').replace(']','"]')
			stmt = stmt.replace('(["<','([').replace('>"])','])')
			out.write(stmt+'\n')
		lvl += 1

# Main function to convert a RDF turtle files to Mermaid, but only the classes represented, without the instances,
# by replacing the uri with the classes in Mermaid statements.
def ontology(rdfInput, mmdOutput, uri, depth):
	template = open("./src/templates/ontology.mmd", "r", encoding="utf-8")
	read = template.read()
	out = open('./mmd/{}'.format(mmdOutput), "w", encoding="utf-8")
	out.write(read)

	g = Graph()
	g.parse('./rdf/{}'.format(rdfInput) , format="turtle")

	classes = classDict()

	u = URIRef(uri)

	i = 1
	lvl = 1

	subList = [(0,u)]
	uriDict = {u: 0}
	uriType = {}
	statements = []
	while lvl <= int(depth):
		stmtList, subList, i, uriDict = convert(subList,g,classes,i, uriDict)
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
				clType = re.findall('\["crm:.*"]:::.*', stmt)[0] # get the class part
				# add to the uriType dict the uri part as the key, and the class part as the value
				# so the class part will replace the uri part in the for loop below
				uriType[inst] = clType
			elif not 'rdfs:label' in stmt:
				statements.append(stmt)
		lvl += 1

	for stmt in statements:
		key1 = re.findall('\(\[.*:.*\) ', stmt)[0].split(' ')[0]
		stmt = stmt.replace(key1, uriType[key1])
		key2 = re.findall('\(\[.*:.*\)', stmt)
		if key2:
			key2 = key2[0]
			stmt = stmt.replace(key2, uriType[key2])
		out.write(stmt+'\n')


def main(Type, rdf, mmd, uri, depth):
	try:
		if Type == 'instance':
			instance(rdf, mmd, uri, depth)
		elif Type == 'ontology':
			ontology(rdf, mmd, uri, depth)
		print('Success! Your output file {} is located in folder /mmd'.format(mmd))
	except:
		pass

# argparse arguments
def parse_args():
	parser = argparse.ArgumentParser(description='Convert CidocCRM-based RDF to Mermaid')

	parser.add_argument("Type", help='The type of the diagram', choices=['instance', 'ontology'])
	parser.add_argument("rdf", help='RDF input filename')
	parser.add_argument("mmd", help='Mermaid output filename')
	parser.add_argument("uri", help='URI of the first node of the graph, e.g. URI of a E39_Actor')
	parser.add_argument("depth", help='The depth/level of the diagram, e.g. 4, 5')

	args = parser.parse_args()
	return args

if __name__ == '__main__':
	args = parse_args()
	main(args.Type, args.rdf, args.mmd, args.uri, args.depth)




