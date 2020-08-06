# CRITERIA

**C**idoc c**R**m **I**n **T**urtle m**ER**maid d**I**agr**A**ms is a Python tool to convert RDF Turtle file (based on CIDOC-CRM model) into [Mermaid](https://mermaid-js.github.io/mermaid/#/) markdown to generate (flowchart) diagrams.

The tools allows you to generate two types of diagrams using the same Turtle file:
* One includes all the **instances**, i.e. URIs, dateTime, Literal values, etc.
* The other one includes only the classes, i.e. the **ontology** of the pattern.

Mainly the mardown is incorporated into HTML page, however, the PNG can be downloaded from [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editors) by simply pasting the entire markdown file into the code box. 

Here is an example of the Existence pattern of CHIN's Target Model.

##### RDF
```turtle
@prefix crm: <http://www.cidoc-crm.org/cidoc-crm/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

<https://www.rdm.net/person/0001> a crm:E21_Person ;
	crm:P98i_was_born <https://www.rdm.net/event/0001> ;
	crm:P100i_died_in <https://www.rdm.net/event/0002> .

<https://www.rdm.net/event/0001> a crm:E67_Birth ;
	crm:P4_has_time-span <http://www.rdm.net/time-span/0001> ;
	crm:P7_took_place_at <http://www.rdm.net/place/0001> .

<https://www.rdm.net/event/0002> a crm:E69_Death ;
	crm:P4_has_time-span <http://www.rdm.net/time-span/0002> ;
	crm:P7_took_place_at <http://www.rdm.net/place/0002> .

<http://www.rdm.net/time-span/0001> a crm:E52_Time-Span ;
	crm:P82a_begin_of_the_begin "1900-02-20T00:00:00-04:00"^^xsd:dateTime ;
	crm:P82b_end_of_the_end "1900-02-20T23:59:59-04:00"^^xsd:dateTime .

<http://www.rdm.net/time-span/0002> a crm:E52_Time-Span ;
	crm:P82a_begin_of_the_begin "1985-12-25T00:00:00-04:00"^^xsd:dateTime ;
	crm:P82b_end_of_the_end "1985-12-25T23:59:59-04:00"^^xsd:dateTime .

<http://www.rdm.net/place/0001> a crm:E53_Place .

<http://www.rdm.net/place/0002> a crm:E53_Place .
```
##### Diagram with instances
![Existence pattern with instances](/docs/images/existenceInst.png)

##### Ontology representation
![Ontology of Existence pattern ](/docs/images/existenceOnto.png)

## Installation
The tools can be simply installed by cloning the repository or downloading the zip file.
It will be run in console, see [Usage](#usage) for further instruction.

### Requirements
Make sure you have the following versions of dependencies before running the tool.
- Python 3.7.0
- [rdflib 5.0.0](https://rdflib.readthedocs.io/en/stable/gettingstarted.html)

## Usage

### criteria
The main python script is **`criteria.py`**, which requires **five** arguments.
|Argument|Description|
|--|--|
|Type | The type of the diagram, the values must be either **`instance`** or **`ontology`**|
|rdf|  RDF input filename (e.g. `Test.ttl`). Any RDF files **must be stored** in the folder `/rdf`|
|mmd|  Mermaid output filename (e.g. `instanceTest.mmd`)|
|uri|  URI of the first node of the graph (e.g. `https://www.rdm.net/person/0001`)|
|depth|  The depth/level of the diagram (e.g. `4` or `5`)|

For example, using the `Test.ttl` file in `./rdf` folder, to generate the diagram including instances, the command is like this:
```shell
$  python criteria.py instance Test.ttl instanceTest.mmd https://www.rdm.net/person/0001 5
```
### rdf
The folder **`/rdf`** is the location where you store the RDF files, of which you want to generate diagrams.

### mmd
The folder **`/mmd`** is the location where the output Mermaid files (`.mmd`) will be stored.

### src
The folder **`/src`** contains several resources for the main script.

#### /templates 
This folder contains the templates of `.mmd` output file, which has the pre-defined classes for styling: one is for diagram with instances (`instance.mmd`), the other is for ontology-only diagram (`ontology.mmd`).
For example,
```
graph TD
classDef Literal fill:#f2f2f2,stroke:#000000;
classDef CRM_Entity fill:#FFFFFF,stroke:#000000;
classDef CRM_Entity_URI fill:#FFFFFF,stroke:#000000;
classDef Temporal_Entity fill:#00C9E6, stroke:#000000;
classDef Temporal_Entity_URI fill:#99f1ff,stroke:#000000;
```
> :warning: At the moment, you can *ONLY edit the colors* in the files, but **DO NOT change the *name of the files* or the *name of the classes* !**

#### /ontologies
This folder contains the ontologies files to be used in the script. Currently it has the `.rdfs` files of main [CIDOC CRM (v6.2.1)](http://www.cidoc-crm.org/Version/version-6.2.1), [FRBRoo (v2.4)](http://www.cidoc-crm.org/frbroo/ModelVersion/frbroo-v.-2.4), and [CRMpc (v1.1)](http://www.cidoc-crm.org/Version/version-6.2).
> :warning: Make sure that the classes in the `.rdfs` **matches** the classes used in your `.ttl`
> For example, it's `E24_Physical_Human-Made_Thing` in your rdf, but it's `E24_Physical_Man-Made_Thing` in the ontology, so edit the ontology file accordingly.

#### source
**`source.py`** is the location to place several python objects to be imported in the main script. It has:
- `classes`: a list object storing the main Cidoc-CRM classes that you want to specify the color codes.
- `onto`: a dictionary object storing the filenames  of the corresponding ontologies (i.e. the `.rdfs` files in the folder `/ontologies`.
> :warning: If you replace the `.rdfs` in the folder `/ontologies` with an updated file, or rename it, make sure to the reflect the name-change by **changing the values** in the `onto` dictionary accordingly.
