# CRITERIA

**C**idoc c**R**m **I**n **T**riples m**ER**maid d**I**agr**A**ms (CRITERIA) is a Python tool that converts RDF files (based on [CIDOC CRM model](http://www.cidoc-crm.org/)) into [Mermaid](https://mermaid-js.github.io/mermaid/#/) markdown to generate (flowchart) diagrams.

The tool can generate two types of diagrams using the same RDF file (which must always contain instances):
* One renders all **instances**, e.g. URIs, dateTime, Literal values
* The other renders only classes, i.e. the **ontology** of the pattern.

The markdown is intended to be incorporated into an HTML page; however, a PNG version can be downloaded from [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor) by simply pasting the entire markdown file into the code box. 

Recommended browsers for Mermaid Live Editor:
* **Mac**: Safari, Chrome, Firefox
* **Windows**: Firefox

Below is an example using CHIN's Birth/Death of People pattern:

##### RDF
* [BirthDeath_Fortin.ttl](/rdf/BirthDeath_Fortin.ttl)

##### Diagram with instances
![Birth/Death of People pattern with instances](/docs/images/BirthDeath_Fortin.png)

##### Ontology representation
![Ontology of Birth/Death of People pattern ](/docs/images/BirthDeathOnto.png)

## Installation
The tool can be installed by cloning this repository or downloading it as a zip file.
It will run in console; see [Usage](#usage) for further instructions.

### Requirements
The following programming language versions of are necessary to run this tool.
- Python 3.7.0
- [rdflib 5.0.0](https://rdflib.readthedocs.io/en/stable/gettingstarted.html)
- **UPDATE**: [rdflib-jsonld 0.5.0](https://github.com/RDFLib/rdflib-jsonld)

## Usage

### criteria
The main python script is **`criteria.py`**, which requires **three** arguments.
|Argument|Description|
|--|--|
|Type | Type of the diagram; the values must be either **`instance`** or **`ontology`**|
|rdf|  RDF input including the full or relative path to the input file (e.g. `./rdf/BirthDeath_Fortin.ttl`).<br>>>**UPDATE**:<br>- The tool can now process **other input formats** besides **`Turtle`**, such as **`NTriples`**, **`RDF/XML`**, **`Trig`**, **`JSON-LD`**, etc.<br>- RDF files is NO LONGER needed to be  stored in the folder `/rdf`. User can now provide their own **input path**, `/User/username/path_to_directory/input.ttl`.|
|mmd|  Mermaid output including the full or relative path to the output file (e.g. `./mmd/BirthDeath_Fortin.mmd`).<br>>>**UPDATE**: User can now provide their own **output path**, `/User/username/path_to_directory/output.mmd`.|

For example, to generate a diagram rendering instances using the `BirthDeath_Fortin.ttl` file in `./rdf` folder and the mermaid output to be stored in folder `./mmd`, the command is as follows:
```shell
$  python criteria.py instance ./rdf/BirthDeath_Fortin.ttl ./mmd/BirthDeath_Fortin.mmd
```
### rdf
This folder contains RDF files used for testing.
> **UPDATE**:
> - The tool can now process **prefixes defined by users**.
> - RDF files are no longer needed be stored in the **`/rdf`** folder.

### mmd
This folder contains mermaid outputs generated during testing. 
> **UPDATE**:
> - Output files are no longer stored in the **`/mmd`** folder by default. User can now provide their own output path.
>
> **Note**: While processing the triples, the script would grab all of them randomly, meaning user would not have much control about the order of statements in the .mmd. However, it also means that running the script over the same RDF file would generate slightly different Mermaid files (i.e. different order of statements), meaning different graphs (i.e. different positions of the nodes). However, the top node's position will remain the same.

### src
The **`/src`** folder contains resources used by the main script.

#### /templates 
The **`templates`** folder contains the templates used to generate the `.mmd` output files. The templates have pre-defined classes for styling: one for visualising instances (`instance.mmd`), the other for visualising only the ontology (`ontology.mmd`). The default styling is based on the color scheme of CIDOC CRM (as proposed by George Bruseker).

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
This **`ontologies`** folder contains the ontology files used in the script. Currently it contains the `.rdfs` files of main [CIDOC CRM (v6.2.1)](http://www.cidoc-crm.org/Version/version-6.2.1), [FRBRoo (v2.4)](http://www.cidoc-crm.org/frbroo/ModelVersion/frbroo-v.-2.4), [CRMpc (v1.1)](http://www.cidoc-crm.org/Version/version-6.2), and CRMdig (v3.2.2) (retrieved from [FORTH's 3M](https://isl.ics.forth.gr/3M/)).
> :warning: Make sure that the classes in the `.rdfs` **match** the classes used in the `.ttl`
> For example, if your `.ttl` uses `E24_Physical_Human-Made_Thing` but the ontology uses `E24_Physical_Man-Made_Thing` the ontology file must be edited accordingly.

#### source
**`source.py`** is the location where to place several python objects to be imported in the main script. It currently contains:
- `classes`: a list object storing the main CIDOC CRM classes that are to be assigned color codes.
- `onto`: a dictionary object storing the filenames of the ontologies used by the script (i.e. the `.rdfs` files in the folder `/ontologies`).
> :warning: If you replace the `.rdfs` in the folder `/ontologies` with an updated file, or rename it, **the values** in the `onto` dictionary must be updated accordingly.

## License

CRITERIA is under the [MIT License](https://github.com/chin-rcip/CRITERIA/blob/master/LICENSE). To meet the attribution requirement of this license, you must must indicate the copyright holder using the following:

> Copyright (c) 2020 Canadian Heritage Information Network, Canadian Heritage, Government of Canada - Réseau Canadien d'information sur le patrimoine, Patrimoine canadien, Gouvernement du Canada
