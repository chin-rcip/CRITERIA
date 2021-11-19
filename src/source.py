# Main CIDOC-CRM classes, serving as Mermaid classes for styling
classes = {
"Literal": {"classColor": "#ffffff", "classStroke": "#000000", "instanceColor": "", "instanceStroke": ""},
"E1_CRM_Entity": {"classColor": "#ffffff", "classStroke": "#000000", "instanceColor": "#ffffff", "instanceStroke": "#000000"},
"E2_Temporal_Entity": {"classColor": "#82c3ec", "classStroke": "#000000", "instanceColor": "#d2e9f9", "instanceStroke": "#000000"},
"E55_Type": {"classColor": "#fab565", "classStroke": "#000000", "instanceColor": "#fde7ce", "instanceStroke": "#000000"},
"E52_Time-Span": {"classColor": "#86bcc8", "classStroke": "#000000", "instanceColor": "#dcebef", "instanceStroke": "#000000"},
"E41_Appellation": {"classColor": "#fef3ba", "classStroke": "#000000", "instanceColor": "#fffae6", "instanceStroke": "#000000"},
"E53_Place": {"classColor": "#94cc7d", "classStroke": "#000000", "instanceColor": "#e1f1da", "instanceStroke": "#000000"},
"E77_Persistent_Item": {"classColor": "#ffffff", "classStroke": "#000000", "instanceColor": "#ffffff", "instanceStroke": "#000000"},
"E28_Conceptual_Object": {"classColor": "#fddc34", "classStroke": "#000000", "instanceColor": "#fef6cd", "instanceStroke": "#000000"},
"E18_Physical_Thing": {"classColor": "#e1ba9c", "classStroke": "#000000", "instanceColor": "#f3e5d8", "instanceStroke": "#000000"},
"E39_Actor": {"classColor": "#ffbdca", "classStroke": "#000000", "instanceColor": "#ffe6eb", "instanceStroke": "#000000"},
"PC0_Typed_CRM_Property": {"classColor": "#cc80ff", "classStroke": "#000000", "instanceColor": "#ebccff", "instanceStroke": "#000000"},
"Mutlti": {"classColor": "", "classStroke": "", "instanceColor": "#cccccc", "instanceStroke": "#000000"},
}


# Ontologies files
onto = {
	'cidoc': {
		'core': 'cidoc_crm_v6.2.1-2018April.rdfs',
		'extensions': {
			'crmpc': 'CRMpc_v1.1.1.rdfs',
			'frbr': 'FRBR2.4-draft.rdfs',
			'crmdig': 'CRMdig_v3.2.2.rdfs',
			'crmsci': 'CRMsci_v1.2.6.rdfs',
			'crmarcheo': 'CRMarchaeo_v1.4.1.rdfs'
		}
	}
	
}

# Prefixes
prefix = {
	'crm': 'http://www.cidoc-crm.org/cidoc-crm/',
	'crmpc': 'http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/',
	'frbroo':'http://iflastandards.info/ns/fr/frbr/frbroo/',
	'crmdig':'http://www.ics.forth.gr/isl/CRMext/CRMdig.rdfs/',
	'crmsci':'http://www.cidoc-crm.org/cidoc-crm/CRMsci/',
	'crmarcheo':'http://www.cidoc-crm.org/cidoc-crm/CRMarchaeo/',
	'schema': 'https://schema.org/'
}



