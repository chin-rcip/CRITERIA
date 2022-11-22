import rdflib
from rdflib import Graph, URIRef, Namespace, util
from rdflib.util import SUFFIX_FORMAT_MAP
from rdflib.namespace import NamespaceManager, RDFS, RDF, XSD, SKOS, SH
import re
import sys
import argparse
import json


nodeLabels = {} # URI: {Property, Node Label} for node 
nodeLink = {} # Node Label and URL link to node documentation
defaultConfig = json.load(open('config.json','r',encoding='utf-8'))

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

def superClass(ontology,conf):
	inFormat = util.guess_format(ontology)
	g = Graph()

	g.parse(ontology, format=inFormat)
	if 'prefix' in conf:
		prefix = conf['prefix']
	else:
		prefix = defaultConfig['prefix']
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
				spcList.append(spc.n3(g.namespace_manager))
				sc = spc
			l += 1
		clss[c.n3(g.namespace_manager)] = spcList
	return clss


# Function to build a dictionary of an ontology's classes and their Mermaid classes, i.e. main CIDOC-CRM classes.
# For instances, the returned object (d) would look like this:
	# d = {'E10_Transfer_of_Custody': 'crm_E2_Temporal_Entity',
	# 	 'E11_Modification': 'crm_E2_Temporal_Entity',
	# 	 'E12_Production': 'crm_E2_Temporal_Entity',
	# 	 'E1_CRM_Entity': 'crm_E1_CRM_Entity',
	# 	 'E20_Biological_Object': 'crm_E18_Physical_Thing',
	# 	 'E21_Person': 'crm_E39_Actor',
	# 	 'E22_Human-Made_Object': 'crm_E18_Physical_Thing'}

def classDict(conf):
	d = {}
	if 'style' in conf:
		classes = conf['style']
	else:
		classes = defaultConfig['style']
	if 'onto' in conf:
		onto = conf['onto']
	else:
		onto = defaultConfig['onto']
	
	for ontology in onto:
		core = onto[ontology]['core']
		coreClass = superClass(core,conf)
		for sc in coreClass:
			for spc in coreClass[sc]:
				spc = spc.replace(':','_')
				if spc in classes:
					d[sc] = spc
					break 
					# exit loop after the first superclass is found in the classes list.
					# e.g. for 'E21_Person' the first superclass found in the classes list
					# is E39_Actor

		if 'extensions' in onto[ontology]:
			for key in onto[ontology]['extensions']:
				ext = onto[ontology]['extensions'][key]
				extClass = superClass(ext,conf)
				for ent in extClass:
					if ent in coreClass:
						for spc in coreClass[ent]:
							spc = spc.replace(':','_')
							if spc in classes:
								d[ent] = spc
								break
					elif len(extClass[ent]) > 0:
						crmSpc = extClass[ent][-1] # retrieve the last/highest superclass of an extension class.
						if crmSpc.replace(':','_') in classes:
							crmSpc = crmSpc.replace(':','_')
							d[ent] = crmSpc
						elif crmSpc in coreClass:
							for spc in coreClass[crmSpc]:
								spc = spc.replace(':','_')
								if spc in classes:
									d[ent] = spc
									break

	for c in classes:
		d[c.replace('_',':',1)] = c
	return d

# Function to convert RDF triples to Mermaid statements.
# Returns a list of statements
def convert(dataGraph,conf):
	g = dataGraph

	classes = classDict(conf)

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
			c = o.n3(g.namespace_manager)
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

# processing node labels and urls described by shacl
def shapeProc(dataGraph,shapeInput):
	shapeFormat = util.guess_format(shapeInput)
	shape = Graph()
	shape.parse(shapeInput, format=shapeFormat)

	for s,p,o in shape.triples((None, SKOS.example, None)):
		if (s,RDF.type,SH.NodeShape) in shape:
			inst = "(["+o.n3(shape.namespace_manager)+"])"
			inst = inst.replace('<','').replace('>','')
			nodeLb =''
			for propShape in shape.objects(s,SH.property):
				for path in shape.objects(propShape,SH.path):
					path = path.n3(shape.namespace_manager)
				for nodeLb in shape.objects(propShape,SH.name):
					nodeLb = nodeLb.n3(shape.namespace_manager).replace('"','')
				for nodeURL in shape.objects(propShape,SH.description):
					nodeURL = nodeURL.n3(shape.namespace_manager).replace('"','')
				if nodeURL:
					nodeLink[nodeLb] = nodeURL
				for nodeVal in shape.objects(propShape,SH.defaultValue):
					nodeLb = nodeLb+'|||'+nodeVal.n3(shape.namespace_manager)
					nodeValURL = nodeVal
					nodeVal = nodeVal.n3(shape.namespace_manager)
					for nodeValLb in dataGraph.objects(nodeValURL,RDFS.label):
						nodeValLb = nodeValLb.n3(shape.namespace_manager).replace('"',"''").replace('^^xsd:string','')
						nodeLb = nodeLb+'<br><em>'+str(nodeValLb)+'</em>'
						nodeVal = nodeVal+'<br><em>'+str(nodeValLb)+'</em>'
					if nodeValURL:
						nodeLink[nodeVal] = nodeValURL

				if not inst in nodeLabels:
					nodeLabels[inst] = {path: nodeLb}
				else:
					nodeLabels[inst][path] = nodeLb		


# Function to generate mermaid.jd style class definition based the classes dict from source.py
def template(conf):
	template = "flowchart TD\n"
	if 'style' in conf:
		classes = conf['style']
	else:
		classes = defaultConfig['style']
	for c in classes:
		if 'classColor' in classes[c]:
			classFill = classes[c]["classColor"]
		else:
			classFill = ''
		if 'classStroke' in classes[c]:
			classStroke = classes[c]["classStroke"]
		else:
			classStroke = ''
		if 'classFontColor' in classes[c]:
			classFontColor = classes[c]["classFontColor"]
		else:
			classFontColor = ''
		if 'instanceColor' in classes[c]:
			instanceFill = classes[c]["instanceColor"]
		else:
			instanceFill = ''
		if 'instanceStroke' in classes[c]:
			instanceStroke = classes[c]["instanceStroke"]
		else:
			instanceStroke = ''
		if 'instanceFontColor' in classes[c]:
			instanceFontColor = classes[c]["instanceFontColor"]
		else:
			instanceFontColor = ''
		template += "classDef {} fill:{},stroke:{},color:{};\n".format(c,classFill,classStroke,classFontColor)
		template += "classDef {}_URI fill:{},stroke:{},color:{};\n".format(c,instanceFill,instanceStroke,instanceFontColor)
	return template

# Main function to convert a RDF turtle files to Mermaid with instances.
def instance(dataGraph, mmdOutput, conf):
	read = template(conf)
	out = open(mmdOutput, "w", encoding="utf-8")
	out.write(read)

	stmtList = convert(dataGraph,conf)
		
	for stmt in stmtList:
		stmt = stmt.replace('"',"''").replace('[','["').replace(']','"]')
		stmt = stmt.replace('(["<','(["').replace('>"])','"])')
		stmt = stmt.replace('|<','|"').replace('>|','"|').replace('--"','-->')
		out.write(stmt+'\n')

# Main function to convert a RDF turtle files to Mermaid, but only the classes represented, without the instances,
# by replacing the uri with the classes in Mermaid statements.
def ontology(dataGraph, mmdOutput, conf):
	read = template(conf)
	out = open(mmdOutput, "w", encoding="utf-8")
	out.write(read)

	uriType = {} # URI and class dict

	statements = []

	stmtList = convert(dataGraph,conf)

	for stmt in stmtList:
		stmt = stmt.replace('"',"''").replace('[','["').replace(']','"]')
		stmt = stmt.replace('(["<','([').replace('>"])','])')

		date = re.findall('\(\[".*\^xsd:dateTime"]\)', stmt)
		lit = re.findall('\(\["\'\'.*\'\'.*"]\)', stmt)
		if date:
			stmt = stmt.replace(date[0], '["xsd:dateTime"]')
		elif lit:
			stmt = stmt.replace(lit[0], '["xsd:string"]')
		
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
		m = re.match('\d+(\(\[.*:.*\)) -->\|(.*)\| (\d+)(\(*\[(.*)\]\)*)', stmt)
		label = ''
		if m.group(1) in uriType:
			stmt = stmt.replace(m.group(1), uriType[m.group(1)])
		if m.group(4) in uriType:
			stmt = stmt.replace(m.group(4), uriType[m.group(4)])

		m2 = re.match('\d+(\(*\[.*:.*\)*) -->\|(.*)\| (\d+)(\(*\[(.*)\]\)*)(.*)', stmt)
		mGroup1 = m.group(1).replace('"','')
		if mGroup1 in nodeLabels and m.group(2) in nodeLabels[mGroup1]:
			label = nodeLabels[mGroup1][m.group(2)]
			out.write(f'subgraph {m2.group(3)} [{m2.group(5)}]\n')
			lbSplit = label.split('|||')
			if lbSplit[0] != '':
				sgStmt1 = f'{m2.group(3)}a[<strong>{lbSplit[0]}</strong>]{m2.group(6)}\n'
				out.write(sgStmt1)
				if lbSplit[0] in nodeLink:
					out.write(f'click {m.group(3)}a "{nodeLink[lbSplit[0]]}" _blank\n')
			if len(lbSplit) > 1:
				sgStmt2 = f'{m2.group(3)}b["{lbSplit[1]}"]{m2.group(6)}\n'
				out.write(sgStmt2)
				if lbSplit[1] in nodeLink:
					out.write(f'click {m.group(3)}b "{nodeLink[lbSplit[1]]}" _blank\n')
			if len(lbSplit) > 1 and lbSplit[0] != '':
				out.write(f'{m2.group(3)}a---{m2.group(3)}b\n')
			out.write('end\n')
			stmt = stmt.replace(m2.group(4), '')
		
		out.write(stmt+'\n')


def main(Type, rdf, mmd, shacl, configFile):
	SUFFIX_FORMAT_MAP["rdfs"] = "xml"
	SUFFIX_FORMAT_MAP["json"] = "json-ld"
	
	inFormat = util.guess_format(rdf)
	dataGraph = Graph()
	dataGraph.parse(rdf, format=inFormat)
	if shacl is not None:
		shapeProc(dataGraph,shacl)
	conf = json.load(open(configFile,'r',encoding='utf-8'))
	if Type == 'instance':
		instance(dataGraph, mmd, conf)
	elif Type == 'ontology':
		ontology(dataGraph, mmd, conf)		
	print('Success!')

# argparse arguments
def parse_args():
	parser = argparse.ArgumentParser(description='Convert CidocCRM-based RDF to Mermaid')

	parser.add_argument("Type", help='The type of the diagram', choices=['instance', 'ontology'])
	parser.add_argument("rdf", help='RDF input filename including path_to_file')
	parser.add_argument("mmd", help='Mermaid output filename including path_to_file')
	parser.add_argument("-sh","--shacl", help='SHACL filename including path_to_file', default=None)
	parser.add_argument("-conf","--configFile", help='Configuration filename including path_to_file', default='config.json')

	args = parser.parse_args()
	return args

if __name__ == '__main__':
	args = parse_args()
	main(args.Type, args.rdf, args.mmd, args.shacl, args.configFile)