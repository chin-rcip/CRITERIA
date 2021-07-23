[*Le français suit*](https://github.com/chin-rcip/criteria#criteria-1)

# CRITERIA

An overview of CRITERIA, its usage, and instructions.

**Version** 1.0

**Created date**: 2021-04-19

**Last update**: 2021-07-23

**Contact**: For questions or comments regarding CRITERIA, please consult the [Issues](https://github.com/chin-rcip/CRITERIA/issues) section (and open an Issue if it is relevant) or contact us by email at the following address: [pch.RCIP-CHIN.pch@canada.ca](mailto:pch.RCIP-CHIN.pch@canada.ca) with “CRITERIA” in the subject line.

- [Main Use](#main-use)
- [Context](#context)
- [Essential Vocabularies and Prior Knowledge](#essential-vocabularies-and-prior-knowledge)
- [Intended Audiences](#intended-audiences)
- [Instructions](#instructions)
	- [Live demonstrator](#live-demonstrator)
		- [Recommended browsers](#recommended-browsers)
		- [Usage](#usage)
	- [Command Line Interface (CLI)](#command-line-interface-cli)
		- [Installation](#installation)
		- [Requirements](#requirements)
		- [Usage](#usage-1)
			- [criteria.py](#criteriapy)
			- [Colour Scheme](#colour-scheme)
			- [Source ontologies](#source-ontologies)
- [Memory Aids](#memory-aids)
- [For More Information](#for-more-information)
- [Licence](#licence)
- [Notable Users](#notable-users)
- [Bibliography](#bibliography)


## Main Use

  - To convert RDF files (based on the [CIDOC CRM model](http://www.cidoc-crm.org/)) into [Mermaid](https://mermaid-js.github.io/mermaid/#/) markdown syntax.

## Context

**C**idoc c**R**m **I**n **T**riples m**ER**maid d**I**agr**A**ms (**CRITERIA**) is a Python tool that converts RDF files (based on the [CIDOC CRM model](http://www.cidoc-crm.org/)) in any format (json-ld, ttl, etc.) into [Mermaid](https://mermaid-js.github.io/mermaid/#/) markdown syntax (file with .mmd extension), which is then rendered as a (flowchart) diagram by Mermaid javascript.

## Essential Vocabularies and Prior Knowledge

Users should have a good understanding of the following terminologies and technologies before proceeding further:

  - [Instance](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#instance-noun)

  - [Ontology](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#ontology-noun)

  - [Pattern](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#pattern-noun)

  - [Data model](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#model-noun)

  - [Class](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#class-noun) and [Property](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#property-noun)

  - [RDF](https://www.w3.org/RDF/) and its formats, especially [Turtle](https://www.w3.org/TR/turtle/) and [JSON-LD](https://json-ld.org/)

  - [URI](https://en.wikipedia.org/wiki/Uniform_Resource_Identifier)

CRITERIA can generate two types of diagrams from the same RDF data, for example, the following RDF data pertaining to Marc-Aurèle Fortin’s birth and death events:

```turtle
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://www.chin-rcip.ca/e39/0001> a crm:E21_Person ;
	rdfs:label "Marc-Aurèle Fortin (1888-1970)"^^xsd:string ;
	crm:P98i_was_born <https://www.chin-rcip.ca/e2/0001> ;
	crm:P100i_died_in <https://www.chin-rcip.ca/e2/0002> .
<https://www.chin-rcip.ca/e2/0001> a crm:E67_Birth ;
	crm:P4_has_time-span <https://www.chin-rcip.ca/e52/0001> ;
	crm:P7_took_place_at <https://www.chin-rcip.ca/e53/0001> ;
	crm:P96_by_mother <https://www.chin-rcip.ca/e39/0002> ;
	crm:P97_from_father <https://www.chin-rcip.ca/e39/0003> .
<https://www.chin-rcip.ca/e2/0002> a crm:E69_Death ;
	crm:P4_has_time-span <https://www.chin-rcip.ca/e52/0002> ;
	crm:P7_took_place_at <https://www.chin-rcip.ca/e53/0002> .
<https://www.chin-rcip.ca/e52/0001> a crm:E52_Time-Span ;
	crm:P82a_begin_of_the_begin "1888-03-14T00:00:00"^^xsd:dateTime ;
	crm:P82b_end_of_the_end "1888-03-14T23:59:59"^^xsd:dateTime .
<https://www.chin-rcip.ca/e52/0002> a crm:E52_Time-Span ;
	crm:P82a_begin_of_the_begin "1970-03-02T00:00:00"^^xsd:dateTime ;
	crm:P82b_end_of_the_end "1970-03-02T23:59:59"^^xsd:dateTime .
<https://www.chin-rcip.ca/e53/0001> a crm:E53_Place ;
	rdfs:label "Laval, Québec"^^xsd:string .
<https://www.chin-rcip.ca/e53/0002> a crm:E53_Place ;
	rdfs:label "Macamic, Québec"^^xsd:string .
<https://www.chin-rcip.ca/e39/0002> a crm:E21_Person ;
	rdfs:label "Amanda Fortier (1861-1953)"^^xsd:string .
<https://www.chin-rcip.ca/e39/0003> a crm:E21_Person ;
	rdfs:label "Thomas Fortin (1853-1933)"^^xsd:string .
```

  - **Instance**: this type of diagram includes all the “instances” of the RDF, meaning both URIs and literal values.

![](/docs/images/criteria_1.png)

  - **Ontology**: this type of diagram includes ONLY the classes and the properties, i.e. the ontological part “ontology” of the pattern. Class means the (triple) object of the property `rdf:type`. Thus, this diagram cannot be generated if an instance does not have a class.

![](/docs/images/criteria_2.png)

## Intended Audiences

CRITERIA is a visualization tool for linked data. However, it is not suitable for visualizing an entire dataset, or even an entire data model pertaining to an entity, for the following reasons:

1. Mermaid handles nodes of the same level in its flowchart by spreading them either horizontally or vertically so that the result quickly becomes crowded;

2. The levels flow in either top-down or left-right directions, making the connections between nodes in non-consecutive levels difficult to read.

For example, all data pertaining to Canadian artist Emily Carr (appellation, birth, death, nationality, etc.) should not be visualized in a single diagram using CRITERIA. In other words, this tool is designed to illustrate individual patterns in a data model (e.g. appellations, birth, or death patterns) through diagrams. Thus, the tool is of most interest and use to the following user groups:

  - *Ontologist/Data modeller*: users who are responsible for the design/construction of a data model can use CRITERIA to visualize data in order to check and validate their modelling.

  - *CIDOC CRM user/learner*: users who would like to have a better understanding of CIDOC CRM ontologies through the visualization of an available RDF serialization; CRITERIA is currently built on top of the CIDOC CRM base and its selected extensions. The CIDOC CRM’s colour scheme is the default style.

  - *Developer (technical and/or content)*: users who are responsible for documenting a data model and/or maintaining its digital presence can use CRITERIA to programmatically integrate the visualization of patterns into their ecosystem. This user group would be more interested in the instruction for the [Command Line Interface](#command-line-interface-cli).

## Instructions

CRITERIA can be used in two ways, via either the live demonstrator or the command line interface (CLI).

### Live demonstrator

The live demonstrator is [available here](http://chinrcip.pythonanywhere.com).

This option is of most interest to users who want to generate diagrams on the go and quickly.

For JSON-LD data, the live demonstrator can process both [contexts](https://w3c.github.io/json-ld-syntax/#the-context) that are embedded in the document or are referenced remotely using URL (such as [Linked.art context](https://linked.art/ns/v1/linked-art.json)).

#### Recommended browsers

  - **MacOS**: Safari, Chrome, Firefox

  - **Windows**: Firefox

#### Usage

After launching the Live Demonstrator:

1. Paste the RDF data into the editor box, which can also highlight any syntax errors.

2. Select RDF format from the drop-down menu.

3. Select the type of diagram: instance or ontology.

4. Click the “Convert” button.

5. Click on the generated diagram to zoom in or out if needed.

6. Download the diagram as either a PNG or an SVG.

![](/docs/images/criteria_3.png)

### Command Line Interface (CLI)

This method is of interest to users who want to use CRITERIA programmatically, for example, for batch process and/or implementation purposes in a larger system.

#### Installation

The tool can be installed by cloning [the repository](https://github.com/chin-rcip/CRITERIA) or downloading it as a zip file.

#### Requirements

The following programming language versions and libraries are necessary to run this tool:

  - [Python 3.7.0](https://www.python.org/downloads/release/python-370/)

  - [rdflib 5.0.0](https://rdflib.readthedocs.io/en/stable/gettingstarted.html) ([BSD-3-Clause License](https://github.com/RDFLib/rdflib/blob/master/LICENSE))

  - [rdflib-jsonld 0.5.0](https://github.com/RDFLib/rdflib-jsonld) ([BSD-3-Clause License](https://github.com/RDFLib/rdflib-jsonld/blob/master/LICENSE.md))

#### Usage

#### criteria.py

1. Go to the `/CRITERIA`folder you just cloned or downloaded locally.
	`$ cd /path/to/CRITERIA`

2. Run: `$ python criteria.py [type] [rdf] [mmd]`

	- `[type]`: Type of the diagram; the values must be either **instance** or **ontology**.
	- `[rdf]`: `/path/to/RDF/input/file`. The downloaded CRITERIA comes with a folder named **rdf** where you can store your RDF files, and simply call `./rdf/your_rdf_input.ttl`. However, you can also call the input file outside of CRITERIA by providing its full path, e.g. `/full/path/to/directory/your_rdf_input.ttl`. The tool can process **several RDF formats** such as Turtle, NTriples, RDF/XML, Trig, JSON-LD, etc.
	- `[mmd]`: `/path/to/mmd/output/file`. The downloaded CRITERIA comes with a folder named **mmd** where you can store your mermaid (.mmd) files, and simply provide `./mmd/your_mmd_output.mmd`. However, you can also choose a file location outside of CRITERIA by providing its full path, e.g. `/full/path/to/directory.mmd`.
	
	**Note**: The script processes triples in random order, meaning the user would not have control on the order of statements in the mermaid output. It also means that running the script over the same RDF file would generate slightly different Mermaid files (i.e. different order of statements), meaning different graphs (i.e. nodes of the same level in different positions). However, the top node’s position and the hierarchy will remain the same.

3. After the mermaid output is created, the diagram can be generated by:

	- Pasting the entire mermaid markdown file into the code box on [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor), which offers the option to download it in PNG or SVG;
	- Embedding the mermaid markdown in the web site source code and [using Mermaid.js to render](https://mermaid-js.github.io/mermaid/#/n00b-gettingStarted?id=_3-deploying-mermaid-on-the-browser).
	
	**Example**:
	- To generate a diagram rendering instances using the RDF file `BirthDeath_Fortin.ttl` in the `./rdf` folder and the mermaid output to be stored in folder `./mmd`, the command is as follows:
    ```shell
    $ python criteria.py instance ./rdf/BirthDeath_Fortin.ttl ./mmd/BirthDeath_Fortin.mmd
    ```

	- To generate a diagram rendering only the ontology using the same RDF file and folder as above, the command is as follows:
    ```shell
    $ python criteria.py ontology ./rdf/BirthDeath_Fortin.ttl ./mmd/BirthDeath_onto.mmd
    ```

#### Colour Scheme

The default styling is based on the colour scheme of CIDOC CRM (as proposed by George Bruseker). The styling templates, found in the folder `/src/templates/`, contain pre-defined Mermaid classes with colour styling.

  - `instance.mmd`: template for styling of instances diagram.

  - `ontology.mmd`: template for styling of ontology diagram.

The colour scheme can be changed by editing the values for **fill** and **stroke**, as seen below:

This example is taken from the instance template.

From

<div class="language-plaintext highlighter-rouge">
	<div class="highlight"><pre class="highlight">
		<code>
graph TD

classDef Literal fill:#f2f2f2,stroke:#000000;

classDef CRM_Entity fill:<strong>#FFFFFF</strong>,stroke:#000000;

classDef CRM_Entity_URI fill:<strong>#FFFFFF</strong>,stroke:#000000;
</code></pre></div></div>

To

<div class="language-plaintext highlighter-rouge">
  <div class="highlight"><pre class="highlight">
    <code>
graph TD

classDef Literal fill:#f2f2f2,stroke:#000000;

classDef CRM_Entity fill:<strong>#ecb3ff</strong>,stroke:#000000;

classDef CRM_Entity_URI fill:<strong>#d24dff</strong>,stroke:#000000;
</code></pre></div></div>

<table>
<tbody>
<tr class="odd">
<td><p>🚩 <em>Warning</em></p>
<p><strong>DO NOT</strong> change the <strong>name and location of the templates files</strong> or the <strong>name of the Mermaid classes</strong>, unless you want to modify the source code <strong>critieria.py</strong>!</p></td>
</tr>
</tbody>
</table>

#### Source ontologies

CRITERIA comes with several default (CIDOC CRM) ontologies (in RDF), which are stored in the folder `/src/ontologies/`.

  - [CIDOC CRM (v6.2.1)](http://www.cidoc-crm.org/Version/version-6.2.1)

  - [FRBRoo (v2.4)](http://www.cidoc-crm.org/frbroo/ModelVersion/frbroo-v.-2.4)

  - [CRMpc (v1.1)](http://www.cidoc-crm.org/Version/version-6.2)

  - CRMdig (v3.2.2) (retrieved from [[FORTH's 3M](https://isl.ics.forth.gr/3M/)]).

<table>
<tbody>
<tr class="odd">
<td><p>🚩 <em>Warning</em></p>
<ul>
<li><p>At the moment, ontologies CANNOT be removed or added. Currently, by default CRITERIA can parse only the ontologies included.</p></li>
<li><p>Make sure that the classes in the ontology `.rdfs` <strong>match</strong> the classes used in the RDF input.</p></li>
</ul>
<p>For example, if the `.ttl` uses `E24_Physical_Human-Made_Thing` but the ontology has `E24_Physical_Man-Made_Thing`, either the ontology or the RDF must be edited for consistency.</p></td>
</tr>
</tbody>
</table>

## Memory Aids

  - [Link to Live Demonstrator](http://chinrcip.pythonanywhere.com)

  - Command for CLI: `$ python criteria.py [type] [rdf] [mmd]`

## For More Information

  - [Mermaid](https://mermaid-js.github.io/mermaid/#/)

  - [RDFLib](http://rdflib.readthedocs.org)

## Licence

CRITERIA is under the [MIT License](https://github.com/chin-rcip/CRITERIA/blob/master/LICENSE). To meet the attribution requirements of this licence, you must indicate the copyright holder using the following:

> Copyright (c) 2020 Canadian Heritage Information Network, Canadian Heritage, Government of Canada - Réseau Canadien d'information sur le patrimoine, Patrimoine canadien, Gouvernement du Canada

## Notable Users

CHIN would like to recognize the projects and institutions that use CRITERIA, which make it possible for CHIN to improve the tool. If you use CRITERIA and your project is not listed below, please feel free to [contact us](#30j0zll).

**Project**: [Reference Data Models](http://docs.swissartresearch.net/)

Organization: [Swiss Art Research Infrastructure, University of Zurich](http://swissartresearch.net/)

Description ([Source](https://docs.swissartresearch.net/)):

> The Semantic Reference Data Models project aims to create a series of re-usable templates of semantic patterns to facilitate the integration and querying of cultural heritage data sources. Each template is a collection of semantic patterns and is based on the analysis of selected sources determined to be of relevance to an entity. The developed semantic patterns are mapped to the CIDOC CRM ontology to ensure compatibility across the heritage domain. The patterns can be used to provide reference implementations for institutions and projects not familiar with CIDOC CRM, to create usable guidelines to generate input interfaces for born-CRM semantic data, and to guide mapping processes from extant sources into the CRM conformant reference model using tools such as 3M.

## Bibliography

Beckett, David, Tim Berners-Lee, Eric Prud’hommeaux, and Gavin Carothers. n.d. “RDF 1.1 Turtle.” Accessed May 28, 2021. [https://www.w3.org/TR/turtle/](https://www.w3.org/TR/turtle/).

Canadian Heritage Information Network (CHIN). 2021a. “class (noun).” In *Glossary*. Ottawa, ON: Government of Canada / Gouvernement du Canada. [https://chin-rcip.github.io/collections-model/en/resources/current/glossary#class-noun](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#class-noun)

———. 2021b. “instance (noun).” In *Glossary*. Ottawa, ON: Government of Canada / Gouvernement du Canada. [https://chin-rcip.github.io/collections-model/en/resources/current/glossary#instance-noun](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#instance-noun)

———. 2021c. “model (noun).” In *Glossary*. Ottawa, ON: Government of Canada / Gouvernement du Canada. [https://chin-rcip.github.io/collections-model/en/resources/current/glossary#model-noun](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#model-noun)

———. 2021d. “ontology (noun).” In *Glossary*. Ottawa, ON: Government of Canada / Gouvernement du Canada. [https://chin-rcip.github.io/collections-model/en/resources/current/glossary#ontology-noun](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#ontology-noun)

———. 2021e. “pattern (noun).” In *Glossary*. Ottawa, ON: Government of Canada / Gouvernement du Canada. [https://chin-rcip.github.io/collections-model/en/resources/current/glossary#pattern-noun](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#pattern-noun)

———. 2021f. “property (noun).” In *Glossary*. Ottawa, ON: Government of Canada / Gouvernement du Canada. [https://chin-rcip.github.io/collections-model/en/resources/current/glossary#property-noun](https://chin-rcip.github.io/collections-model/en/resources/current/glossary#property-noun)

JSON-LD Working Group. 2014. “JSON-LD - JSON for Linking Data.” JSON-LD. January 16, 2014. https://json-ld.org/.

linked.art. 2020. “Linked Art.” Linked Art. January 30, 2020. https://linked.art/.

RDF Working Group. 2014. “RDF - Semantic Web Standards.” W3C. February 25, 2014. https://www.w3.org/RDF/.

RDFLib Team. n.d. “Rdflib 5.0.0 — Rdflib 5.0.0 Documentation.” Accessed May 28, 2021. https://rdflib.readthedocs.io/en/stable/.

Sveidqvist, Knut. n.d. “Mermaid - Markdownish Syntax for Generating Flowcharts, Sequence Diagrams, Class Diagrams, Gantt Charts and Git Graphs.” Accessed May 28, 2021. https://mermaid-js.github.io/mermaid/#/.

Swiss Art Research Infrastructure. n.d. “SARI Documentation.” Accessed May 28, 2021. https://docs.swissartresearch.net/.

Wikipedia. 2020. “Uniform Resource Identifier.” In Wikipedia. San Francisco, CA: Wikipedia. [https://en.wikipedia.org/w/index.php?title=Uniform_Resource_Identifier&oldid=960824188](https://en.wikipedia.org/w/index.php?title=Uniform_Resource_Identifier&oldid=960824188).

---

# CRITERIA

Un aperçu de ce que CRITERIA offre comme fonctionnalités ainsi que les instructions à suivre pour utiliser l’outil.

**Version** : 1.0

**Créé le** : 2021-04-19

**Mis à jour** : 2021-07-23

**Pour information** : Si vous avez des questions ou des commentaires sur CRITERIA, veuillez consulter la section [Issues](https://github.com/chin-rcip/CRITERIA/issues) (et créez une nouvelle problématique « Issue » si pertinent) ou communiquez avec nous par courriel, à l’adresse [pch.RCIP-CHIN.pch@canada.ca](mailto:pch.RCIP-CHIN.pch@canada.ca). Indiquez « CRITERIA » en objet.

- [Utilisation principale](#utilisation-principale)
- [Contexte](#contexte)
- [Vocabulaire de base et connaissances préalables](#vocabulaire-de-base-et-connaissances-préalables)
- [Auditoires visés](#auditoires-visés)
- [Instructions](#instructions-1)
	- [Démonstrateur en ligne](#démonstrateur-en-ligne) 
		- [Navigateurs recommandés](#navigateurs-recommandés)
		- [Utilisation](#utilisation) 
	- [Interface en ligne de commande](#interface-en-ligne-de-commande) 
		- [Installation](#installation-1) 
		- [Dépendances](#dépendances) 
		- [Utilisation](#utilisation-1) 
			- [criteria.py](#criteriapy-1) 
			- [Schème de couleurs](#schème-de-couleurs) 
			- [Ontologies source (en anglais)](#ontologies-source-en-anglais)
- [Aide-mémoire](#aide-mémoire)
- [Pour en savoir plus](#pour-en-savoir-plus)
- [Licence](#licence-1)
- [Utilisateurs dignes de mention](#utilisateurs-dignes-de-mention)
- [Bibliographie](#bibliographie)

## Utilisation principale

  - Convertir des documents RDF fondés sur [CIDOC CRM](http://www.cidoc-crm.org/) en documents Markdown (syntaxe [Mermaid](https://mermaid-js.github.io/mermaid/#/)).

## Contexte

**CRITERIA** (acronyme anglais de **C**idoc c**R**m **I**n **T**riples m**ER**maid d**I**agr**A**ms) est un outil créé en Python qui convertit des documents de tout format (json-ld, ttl, etc.) fondés sur le [CIDOC CRM](http://www.cidoc-crm.org/)) en documents Markdown (syntaxe [Mermaid](https://mermaid-js.github.io/mermaid/#/), extension .mmd), qu’un script Javascript Mermaid peut ensuite convertir en organigramme.

## Vocabulaire de base et connaissances préalables 

Avant de poursuivre, tout utilisateur doit bien comprendre les termes et technologies suivants :

  - [Instance](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#instance-nom-feminin)

  - [Ontologie](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#ontologie-nom-feminin)

  - [Patron conceptuel](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#patron-conceptuel-nom-masculin)

  - [Modèle de données](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#modele-nom-masculin)

  - [Classe](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#classe-nom-feminin) et [Propriété](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#propriete-nom-feminin)

  - [RDF](https://www.w3.org/RDF/) et ses divers formats, notamment [Turtle](https://www.w3.org/TR/turtle/) et [JSON-LD](https://json-ld.org/)

  - [URI](https://fr.wikipedia.org/wiki/Uniform_Resource_Identifier)

CRITERIA peut créer deux types de diagrammes à partir des mêmes données RDF. Prenons par exemple les données RDF suivantes, sur la naissance et le décès de Marc-Aurèle Fortin :

```turtle
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://www.chin-rcip.ca/e39/0001> a crm:E21_Person ;
  rdfs:label "Marc-Aurèle Fortin (1888-1970)"^^xsd:string ;
  crm:P98i_was_born <https://www.chin-rcip.ca/e2/0001> ;
  crm:P100i_died_in <https://www.chin-rcip.ca/e2/0002> .
<https://www.chin-rcip.ca/e2/0001> a crm:E67_Birth ;
  crm:P4_has_time-span <https://www.chin-rcip.ca/e52/0001> ;
  crm:P7_took_place_at <https://www.chin-rcip.ca/e53/0001> ;
  crm:P96_by_mother <https://www.chin-rcip.ca/e39/0002> ;
  crm:P97_from_father <https://www.chin-rcip.ca/e39/0003> .
<https://www.chin-rcip.ca/e2/0002> a crm:E69_Death ;
  crm:P4_has_time-span <https://www.chin-rcip.ca/e52/0002> ;
  crm:P7_took_place_at <https://www.chin-rcip.ca/e53/0002> .
<https://www.chin-rcip.ca/e52/0001> a crm:E52_Time-Span ;
  crm:P82a_begin_of_the_begin "1888-03-14T00:00:00"^^xsd:dateTime ;
  crm:P82b_end_of_the_end "1888-03-14T23:59:59"^^xsd:dateTime .
<https://www.chin-rcip.ca/e52/0002> a crm:E52_Time-Span ;
  crm:P82a_begin_of_the_begin "1970-03-02T00:00:00"^^xsd:dateTime ;
  crm:P82b_end_of_the_end "1970-03-02T23:59:59"^^xsd:dateTime .
<https://www.chin-rcip.ca/e53/0001> a crm:E53_Place ;
  rdfs:label "Laval, Québec"^^xsd:string .
<https://www.chin-rcip.ca/e53/0002> a crm:E53_Place ;
  rdfs:label "Macamic, Québec"^^xsd:string .
<https://www.chin-rcip.ca/e39/0002> a crm:E21_Person ;
  rdfs:label "Amanda Fortier (1861-1953)"^^xsd:string .
<https://www.chin-rcip.ca/e39/0003> a crm:E21_Person ;
  rdfs:label "Thomas Fortin (1853-1933)"^^xsd:string .
```

  - **Instance :** type de diagramme qui comprend toutes les instances que renferme le document RDF, c’est-à-dire les URIs et les valeurs littérales.

![](/docs/images/criteria_1.png)

  - **Ontologie :** type de diagramme qui ne comprend que les classes et leurs propriétés, c’est-à-dire le volet « ontologie » d’un patron conceptuel. Par « classe », on entend l’objet (du triplet) de la propriété `rdf:type`. Par conséquent, il est impossible de créer ce type de diagramme si une instance n’appartient à aucune classe.

![](/docs/images/criteria_2.png)

## Auditoires visés 

CRITERIA est un outil de visualisation de données liées. Il se prête toutefois mal à la visualisation de tout un ensemble de données ou d’un modèle de données complet se rapportant à une seule entité. Voici pourquoi :

1. le format Mermaid dispose les nœuds de même niveau à l’horizontale ou à la verticale dans l’organigramme, ce qui rend rapidement ce dernier illisible;

2. les niveaux sont présentés de haut en bas ou de gauche à droite; il est donc difficile de distinguer les liens entre des nœuds qui ne se suivent pas.

Par exemple, il ne faudrait pas utiliser CRITERIA pour visualiser toutes les données (nom, naissance, décès, nationalité, etc.) sur l’artiste canadienne Emily Carr. En d’autres termes, cet outil sert à illustrer à l’aide de diagrammes des patrons conceptuels précis d’un modèle de données (patrons d’appellations, de naissances ou de décès, par exemple). Il intéresse donc divers groupes d’utilisateurs.

  - *Ontologistes et modélisateurs de données *: les personnes qui conçoivent ou créent des modèles de données peuvent se servir de CRITERIA pour visualiser leurs modèles afin de les valider.

  - *Utilisateurs (incluant les néophytes) du CIDOC CRM *: les personnes qui veulent mieux comprendre les ontologies du CIDOC CRM peuvent visualiser une sérialisation RDF existante, puisque CRITERIA a été créé à partir du CIDOC CRM de base et de certaines de ses extensions. Le schème de couleurs du CIDOC CRM est le style appliqué par défaut.

  - *Développeurs de logiciels ou de contenu *: les personnes chargées de produire la documentation sur un modèle de données ou de le tenir à jour sous forme numérique peuvent utiliser CRITERIA pour intégrer automatiquement dans leur environnement une visualisation des patrons conceptuels. Ces utilisateurs seront particulièrement intéressés par l’utilisation en [ligne de commande](https://docs.google.com/document/d/1BCWZAtljnQag212G7hsHwfjvvsDwplLfjOh7gfODPLQ/edit#heading=h.17dp8vu) de cet outil.

## Instructions

On peut utiliser CRITERIA de deux façons : par une démonstrateur en ligne ou par ligne de commande.

### Démonstrateur en ligne 

Le [démonstrateur en ligne](http://chinrcip.pythonanywhere.com), en anglais seulement, intéressera surtout ceux et celles qui désirent créer rapidement des diagrammes.

Dans le cas des données JSON-LD, le démonstrateur en temps réel peut traiter les [contextes](https://w3c.github.io/json-ld-syntax/#the-context) tant intégrés au document que ceux auxquels le document fait référence par URL (comme le [contexte Linked.art](https://linked.art/ns/v1/linked-art.json)).

#### Navigateurs recommandés 

  - **MacOS :** Safari, Chrome ou Firefox

  - **Windows :** Firefox

#### Utilisation

Après avoir lancé le démonstrateur en ligne :

1. Coller les données RDF dans le champ d’édition qui peut mettre en évidence toute erreur de syntaxe.

2. Choisir le format RDF dans la liste déroulante.

3. Choisir le type de diagramme : Instance ou Ontologie.

4. Cliquer sur « Convert » (convertir).

5. Pour agrandir ou réduire le diagramme, cliquer sur celui-ci.

6. Pour télécharger le diagramme en format PNG ou SVG, cliquer sur le bouton correspondant.

![](/docs/images/criteria_3.png)

### Interface en ligne de commande

Cette méthode intéressera surtout les utilisateurs voulant utiliser CRITERIA de façon automatisée, comme dans le traitement par lots ou la mise en œuvre dans un système plus élaboré.

#### Installation

Pour installer l’outil, cloner [son répertoire](https://github.com/chin-rcip/CRITERIA) ou télécharger celui-ci en fichier Zip.

#### Dépendances 

Pour exécuter l’outil, les versions du langage de programmation et les bibliothèques suivantes sont nécessaires :

  - [Python 3.7.0](https://www.python.org/downloads/release/python-370/)

  - [rdflib 5.0.0](https://rdflib.readthedocs.io/en/stable/gettingstarted.html) ([license BSD 3](https://github.com/RDFLib/rdflib/blob/master/LICENSE))

  - [rdflib - 0.5.0](https://github.com/RDFLib/rdflib-jsonld) ([license BSD 3](https://github.com/RDFLib/rdflib-jsonld/blob/master/LICENSE.md))

#### Utilisation 

***criteria.py***

1. Ouvrir le répertoire `/CRITERIA` cloné ou téléchargé sur votre poste de travail.

    `$ cd /path/to/CRITERIA`

2. Exécuter : `$ python criteria.py [type] [rdf] [mmd]`

    - `[type]`: Le type de diagramme ne peut être que **instance** ou **ontology**.
    - `[rdf]`: `/chemin/vers/le/fichier/RDF/intrant`. Tel qu’installé ou téléchargé, CRITERIA comprend le sous-répertoire **rdf** où copier les fichiers RDF. Ensuite, préciser `./rdf/fichier_RDF_intrant.ttl`. On peut aussi indiquer le chemin d’accès complet d’un fichier s’il ne se trouve pas dans ce sous-répertoire : `/chemin/complet/du/répertoire/fichier_RDF_intrant.ttl`. L’outil peut traiter **plusieurs formats RDF**, comme Turtle, NTriples, RDF/XML, Trig ou JSON-LD.
    - `[mmd]`: `/chemin/du/répertoire/extrant`. Tel qu’installé ou téléchargé, CRITERIA comprend le sous-répertoire **mmd** où sauvegarder les fichiers mermaid (.mmd) extrants : `./mmd/fichier_MMD_extrant.ttl`. On peut aussi préciser le chemin d’accès complet d’un répertoire où sauvegarder le fichier extrant : `/chemin/complet/du/répertoire/fichier_MMD_extrant.ttl`.

    **Remarque :** Le script traite les triplets en ordre aléatoire; par conséquent, l’utilisateur n’a aucun contrôle sur l’ordre de présentation du fichier mermaid extrant. Cela signifie aussi qu’exécuter le script plusieurs fois à partir d’un même document RDF crée des documents Mermaid légèrement différents (l’ordre des énoncés y diffère), ce qui crée des diagrammes différents, car l’ordre des nœuds de même niveau sera différent. L’emplacement du nœud principal et la hiérarchie restent toutefois identiques.

3. Une fois le fichier mermaid extrant créé, générer le diagramme en procédant comme suit :

    - coller intégralement le contenu du fichier mermaid Markdown dans le champ de code de [l’éditeur Mermaid en ligne](https://mermaid-js.github.io/mermaid-live-editor); cet utilitaire permet de télécharger le diagramme correspondant en formats PNG ou SVG; ou
    - intégrer le code Markdown dans le code source du site Web et créer le diagramme à l’aide de [Mermaid.js](https://mermaid-js.github.io/mermaid/#/n00b-gettingStarted?id=_3-deploying-mermaid-on-the-browser).

    **Exemple :**
    - Voici la commande servant à générer un diagramme d’instances à partir du fichier RDF `BirthDeath_Fortin.ttl` dans le répertoire `./rdf` et l’enregistrer dans le répertoire `./mmd` :
    ```shell
    $ python criteria.py instance ./rdf/BirthDeath_Fortin.ttl ./mmd/BirthDeath_Fortin.mmd
    ```

    - Voici la commande servant à ne générer que l’ontologie à partir du même fichier et à l’enregistrer dans le même répertoire :
    ```shell
    $ python criteria.py ontology ./rdf/BirthDeath_Fortin.ttl ./mmd/BirthDeath_onto.mmd
    ```

***Schème de couleurs***

Comme l’a proposé George Bruseker, le style par défaut est fondé sur le schème de couleurs du CIDOC CRM. Les gabarits de styles, dans le répertoire `/src/templates/`, contiennent les classes Mermaid prédéfinies et les couleurs correspondantes.

  - `instance.mmd`: gabarit de styles pour les diagrammes d’instances.

  - `ontology.mmd`: gabarit de styles pour les diagrammes d’ontologies.

Pour modifier ce schème de couleurs, modifier les valeurs des paramètres **fill** et **stroke**.

Voici un exemple tiré du modèle des instances :

Fichier d’origine :

<div class="language-plaintext highlighter-rouge">
  <div class="highlight"><pre class="highlight">
    <code>
graph TD

classDef Literal fill:#f2f2f2,stroke:#000000;

classDef CRM_Entity fill:<strong>#FFFFFF</strong>,stroke:#000000;

classDef CRM_Entity_URI fill:<strong>#FFFFFF</strong>,stroke:#000000;
</code></pre></div></div>

Fichier modifié :

<div class="language-plaintext highlighter-rouge">
  <div class="highlight"><pre class="highlight">
    <code>
graph TD

classDef Literal fill:#f2f2f2,stroke:#000000;

classDef CRM_Entity fill:<strong>#ecb3ff</strong>,stroke:#000000;

classDef CRM_Entity_URI fill:<strong>#d24dff</strong>,stroke:#000000;
</code></pre></div></div>

<table>
<tbody>
<tr class="odd">
<td><p>🚩 <em>Avertissement</em></p>
<p><strong>NE JAMAIS</strong> <strong>modifier le nom, l’emplacement des fichiers gabarits</strong> ni le <strong>nom des classes Mermaid</strong>, à moins de vouloir modifier aussi le code source de criteria.py!</p></td>
</tr>
</tbody>
</table>

***Ontologies source (en anglais)***

CRITERIA est installé avec plusieurs ontologies CIDOC CRM par défaut en format RDF; elles se trouvent dans le répertoire `/src/ontologies/`.

  - [CIDOC CRM (v6.2.1)](http://www.cidoc-crm.org/Version/version-6.2.1)

  - [FRBRoo (v2.4)](http://www.cidoc-crm.org/frbroo/ModelVersion/frbroo-v.-2.4)

  - [CRMpc (v1.1)](http://www.cidoc-crm.org/Version/version-6.2)

  - CRMdig (v3.2.2) (téléchargée du site [3m du FORTH](https://isl.ics.forth.gr/3M/)).

<table>
<tbody>
<tr class="odd">
<td><p>🚩 <em>Avertissement</em></p>
<ul>
<li>
<p>La suppression ou l’ajout d’ontologies est actuellement IMPOSSIBLE. Par défaut, CRITERIA ne peut traiter que les ontologies incluses.</p>
</li>
<li>
<p>S’assurer donc que les classes des documents RDF intrants <strong>correspondent</strong> aux classes des ontologies (fichiers .rdfs).</p>
</li>
</ul>
<p>Si par exemple le fichier .ttl intrant désigne la classe « E24_Physical_Human-Made_Thing » mais que l’ontologie la nomme « E24_Physical_Man-Made_Thing », il faut modifier le fichier intrant ou l’ontologie, par souci d’uniformité.</p></td>
</tr>
</tbody>
</table>

## Aide-mémoire 

  - [Lien vers le démonstrateur en ligne](http://chinrcip.pythonanywhere.com)

  - Syntaxe en ligne de commande : `$ python criteria.py [type] [rdf] [mmd]`

## Pour en savoir plus

  - [Mermaid](https://mermaid-js.github.io/mermaid/#/)

  - [RDFLib](http://rdflib.readthedocs.org)

## Licence

CRITERIA est distribué en vertu de la [licence MIT](https://github.com/chin-rcip/CRITERIA/blob/master/LICENSE). Pour satisfaire aux exigences relatives à son attribution, vous devez préciser comme suit le détenteur du droit d’auteur :

> Copyright (c) 2020 Canadian Heritage Information Network, Canadian Heritage, Government of Canada – Réseau canadien d'information sur le patrimoine, Patrimoine canadien, Gouvernement du Canada

## Utilisateurs dignes de mention

Le RCIP veut remercier les responsables de projets et les institutions qui utilisent CRITERIA; nous ne pourrions pas améliorer cet outil sans leur contribution. Si vous utilisez CRITERIA mais que votre projet est absent de la liste ci-dessous, n’hésitez pas à [communiquer avec nous](#kix.xmzgkpdo17zb).

**Projet :** [Reference Data Models](http://docs.swissartresearch.net/) (en anglais seulement)

Organisme : [Swiss Art Research Infrastructure, University of Zurich](http://swissartresearch.net/)

Description ([Source](https://docs.swissartresearch.net/)) :

> Le projet des modèles de données sémantiques de référence a pour but de créer un ensemble de modèles de patrons conceptuels sémantiques réutilisables afin de simplifier l’intégration et la recherche des sources de données sur le patrimoine culturel. Chaque modèle consiste en une série de patrons conceptuels sémantiques fondés sur l’analyse de sources choisies jugées pertinentes à une entité. Aux fins de compatibilité avec l’ensemble du domaine patrimonial, ces patrons conceptuels sémantiques correspondent à l’ontologie CIDOC CRM et peuvent servir d’applications de référence aux institutions et responsables de projets peu familiers avec le CIDOC CRM. En effet, il est possible de les utiliser comme modèles pour développer des interfaces de saisie de données sémantiques créées nativement à partir du CRM. De plus, ces patrons conceptuels peuvent servir à transformer des sources existantes vers un modèle de référence conforme au CIDOC CRM, à l’aide d’un outil tel que 3M.

## Bibliographie

Beckett, David, Tim Berners-Lee, Eric Prud’hommeaux, et Gavin Carothers. sans date. “RDF 1.1 Turtle.” Consulté le 28 mai 2021. [https://www.w3.org/TR/turtle/](https://www.w3.org/TR/turtle/).

Réseau canadien d’information sur le patrimoine (RCIP). 2021a. « classe (nom féminin) ». Dans le *Glossaire*. Ottawa, Ont. : Gouvernement du Canada / Government of Canada. [https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#classe-nom-feminin](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#classe-nom-feminin)

———. 2021b. « instance (nom féminin) ». Dans le *Glossaire*. Ottawa, Ont. : Gouvernement du Canada / Government of Canada. [https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#instance-nom-feminin](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#instance-nom-feminin)

———. 2021c. « modèle (nom masculin) ». Dans le *Glossaire*. Ottawa, Ont. : Gouvernement du Canada / Government of Canada. [https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#modele-nom-masculin](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#modele-nom-masculin)

———. 2021d. « ontologie (nom féminin) ». Dans le *Glossaire*. Ottawa, Ont. : Gouvernement du Canada / Government of Canada. [https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#ontologie-nom-feminin](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#ontologie-nom-feminin)

———. 2021e. « patron conceptuel (nom masculin) ». Dans le *Glossaire*. Ottawa, Ont. : Gouvernement du Canada / Government of Canada. [https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#patron-conceptuel-nom-masculin](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#patron-conceptuel-nom-masculin)

———. 2021f. « propriété (nom féminin) ». Dans le *Glossaire*. Ottawa, Ont. : Gouvernement du Canada / Government of Canada. [https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#propriete-nom-feminin](https://chin-rcip.github.io/collections-model/fr/ressources/actuel/glossaire#propriete-nom-feminin)

JSON-LD Working Group. 2014. “JSON-LD - JSON for Linking Data.” LFQ 16 janvier 2014. https://json-ld.org/.

linked.art. 2020. “Linked Art.” Linked Art. 30 janvier 2020. https://linked.art/.

RDF Working Group. 2014. “RDF - Semantic Web Standards.” W3C. 25 février 2014. https://www.w3.org/RDF/.

RDFLib Team. sans date. “Rdflib 5.0.0 — Rdflib 5.0.0 Documentation.” Consulté le 28 mai 2021. https://rdflib.readthedocs.io/en/stable/.

Sveidqvist, Knut. sans date. “Mermaid - Markdownish Syntax for Generating Flowcharts, Sequence Diagrams, Class Diagrams, Gantt Charts and Git Graphs.” Consulté le 28 mai 2021. https://mermaid-js.github.io/mermaid/#/.

Swiss Art Research Infrastructure. sans date. “SARI Documentation.” Consulté le 28 mai 2021. https://docs.swissartresearch.net/.

Wikipédia 2020. “Uniform Resource Identifier.” Wikipédia. San Francisco (Californie) Wikipédia. https://fr.wikipedia.org/wiki/Uniform_Resource_Identifier.

