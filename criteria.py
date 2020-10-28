import rdflib
from rdflib import Graph, URIRef, Namespace, util
from rdflib.namespace import NamespaceManager, RDFS, RDF, XSD
import re
import sys
import argparse
from src import source


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
	# CIDOC-CRM
	cidocClass = superClass(source.onto['crm'], 'crm', 'http://www.cidoc-crm.org/cidoc-crm/')
	for sc in cidocClass:
		for spc in cidocClass[sc]:
			# spc = spc.split(':')[1]
			if spc in classes:
				d[sc] = '_'.join(spc.split('_')[1:])
				break 
				# exit loop after the first superclass is found in the classes list.
				# e.g. for 'E21_Person' the first superclass found in the classes list
				# is E39_Actor
	# FRBRoo
	frbrClass = superClass(source.onto['frbroo'], 'frbroo', 'http://iflastandards.info/ns/fr/frbr/frbroo/')
	for fr in frbrClass:
		crmSpc = frbrClass[fr][-1] # retrieve the last/highest cidoc-crm superclass of a frbroo class.
		for spc in cidocClass[crmSpc]:
			# spc = spc.split(':')[1]
			if spc in classes:
				d[fr] = '_'.join(spc.split('_')[1:])
				break 
	# CRMDig
	digClass = superClass(source.onto['crmdig'], 'crmdig', 'http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/')
	for dig in digClass:
		crmSpc = digClass[dig][-1] # retrieve the last/highest cidoc-crm superclass of a crmdig class.
		for spc in cidocClass[crmSpc]:
			# spc = spc.split(':')[1]
			if spc in classes:
				d[dig] = '_'.join(spc.split('_')[1:])
				break 
	# CRMpc
	pcClass = superClass(source.onto['pc'], 'crm', 'http://www.cidoc-crm.org/cidoc-crm/')
	for pc in pcClass:
		d[pc] = 'PC_Classes'

	for c in classes:
		# d['crm:'+c] = '_'.join(c.split('_')[1:])
		d[c] = '_'.join(c.split('_')[1:])
	return d

# Function to convert RDF triples to Mermaid statements.
# Returns a list of statements
def convert(rdfInput):
	if '.json' in rdfInput or '.jsonld' in rdfInput:
		inFormat = util.guess_format(rdfInput, {'json': 'json-ld', 'jsonld': 'json-ld'})
	else:
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
			if isinstance(s, rdflib.URIRef):
				uriDict[s] = n1

		if o in uriDict:
			n2 = uriDict[o]
		else:
			n2 = i
			i += 1
			if (isinstance(o, rdflib.URIRef) and 
				p != 'rdf:type' ):
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

# Main function to convert a RDF turtle files to Mermaid with instances.
def instance(rdfInput, mmdOutput):
	template = open("./src/templates/instance.mmd", "r", encoding="utf-8")
	read = template.read()
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
	template = open("./src/templates/ontology.mmd", "r", encoding="utf-8")
	read = template.read()
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


def main(Type, rdf, mmd):
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

