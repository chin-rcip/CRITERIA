# CRITERIA

**C**idoc c**R**m **I**n **T**urtle m**ER**maid d**I**agr**A**ms (CRITERIA) is a Python tool that converts RDF Turtle files (based on CIDOC CRM model) into [Mermaid](https://mermaid-js.github.io/mermaid/#/) markdown to generate (flowchart) diagrams.

The tool can generate two types of diagrams using the same Turtle file:
* One renders all **instances**, e.g. URIs, dateTime, Literal values
* The other renders only classes, i.e. the **ontology** of the pattern.

The markdown is intended to be incorporated into an HTML page; however, a PNG version can be downloaded from [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor) by simply pasting the entire markdown file into the code box. 

Recommended browsers for Mermaid Live Editor:
* Mac: Safari, Chrome, Firefox
* Windows: Firefox

Below is an example using CHIN's Birth/Death of People pattern:

##### RDF
* [Test.ttl](/rdf/Test.ttl)

##### Diagram with instances
![Birth/Death of People pattern with instances](/docs/images/BirthDeathInst.png)

##### Ontology representation
![Ontology of Birth/Death of People pattern ](/docs/images/BirthDeathOnto.png)

## Installation
The tool can be installed by cloning this repository or downloading it as a zip file.
It will run in console; see [Usage](#usage) for further instructions.

### Requirements
The following programming language versions of are necessary to run this tool.
- Python 3.7.0
- [rdflib 5.0.0](https://rdflib.readthedocs.io/en/stable/gettingstarted.html)

## Usage

### criteria
The main python script is **`criteria.py`**, which requires **five** arguments.
|Argument|Description|
|--|--|
|Type | Type of the diagram; the values must be either **`instance`** or **`ontology`**|
|rdf|  RDF Turtle input filename (e.g. `Test.ttl`); TTL files **must be stored** in the folder `/rdf`|
|mmd|  Mermaid output filename (e.g. `instanceTest.mmd`)|
|uri|  URI of the first node of the graph, which is expected to be at the top of the diagram (e.g. in the above example, the first node is the URI of E21_Person `https://www.chin-rcip/e39/0001`)|
|depth|  The depth/level of the diagram (e.g. `4` or `5`)|

For example, to generate a diagram rendering instances using the `Test.ttl` file in `./rdf` folder, the command is as follows:
```shell
$  python criteria.py instance Test.ttl instanceTest.mmd https://www.rdm.net/person/0001 5
```
### rdf
RDF files used to generate diagrams must be stored in the **`/rdf`** folder.

### mmd
Mermaid files (`.mmd`) are outputed and stored in the **`/mmd`** folder.

### src
The **`/src`** folder contains resources used by the main script.

#### /templates 
The **`templates`** folder contains the templates used to generate the `.mmd` output files. The templates have pre-defined classes for styling: one for visualising instances (`instance.mmd`), the other for visualising only the ontology (`ontology.mmd`).
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
This **`ontologies`** folder contains the ontology files used in the script. Currently it contains the `.rdfs` files of main [CIDOC CRM (v6.2.1)](http://www.cidoc-crm.org/Version/version-6.2.1), [FRBRoo (v2.4)](http://www.cidoc-crm.org/frbroo/ModelVersion/frbroo-v.-2.4), and [CRMpc (v1.1)](http://www.cidoc-crm.org/Version/version-6.2).
> :warning: Make sure that the classes in the `.rdfs` **match** the classes used in the `.ttl`
> For example, if your `.ttl` uses `E24_Physical_Human-Made_Thing` but the ontology uses `E24_Physical_Man-Made_Thing` the ontology file must be edited accordingly.

#### source
**`source.py`** is the location where to place several python objects to be imported in the main script. It currently contains:
- `classes`: a list object storing the main CIDOC CRM classes that are to be assigned color codes.
- `onto`: a dictionary object storing the filenames of the ontologies used by the script (i.e. the `.rdfs` files in the folder `/ontologies`).
> :warning: If you replace the `.rdfs` in the folder `/ontologies` with an updated file, or rename it, **the values** in the `onto` dictionary must be updated accordingly.
