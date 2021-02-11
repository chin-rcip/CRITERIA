# CRITERIA

**C**idoc c**R**m **I**n **T**riples m**ER**maid d**I**agr**A**ms (CRITERIA) is a Python tool that converts RDF files (based on the [CIDOC CRM model](http://www.cidoc-crm.org/)) into [Mermaid](https://mermaid-js.github.io/mermaid/#/) markdown to generate (flowchart) diagrams.

The tool can generate two types of diagrams using the same RDF file (which must always contain instances):
* One renders all **instances**, e.g. URIs, dateTime, Literal values
* The other renders only classes, i.e. the **ontology** of the pattern.

The markdown is intended to be incorporated into an HTML page; however, a PNG version can be downloaded from [Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor) by simply pasting the entire markdown file into the code box. 

If you do not want to use the script directly, a [Live Demonstrator](http://chinrcip.pythonanywhere.com/) of CRITERIA is available.

Recommended browsers for Mermaid Live Editor & Live Demontrator:
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
- [rdflib-jsonld 0.5.0](https://github.com/RDFLib/rdflib-jsonld)

## Usage

### criteria
The main python script is **`criteria.py`**, which requires **three** arguments.
|Argument|Description|
|--|--|
|Type | Type of the diagram; the values must be either **`instance`** or **`ontology`**|
|rdf|  RDF input including the full or relative path to the input file (e.g. `./rdf/BirthDeath_Fortin.ttl`).<br><br>- The tool can process **several input formats** such as **`Turtle`**, **`NTriples`**, **`RDF/XML`**, **`Trig`**, **`JSON-LD`**, etc.<br>- RDF files do not need to be  stored in the folder `/rdf`. User can provide their own **input path**, `/User/username/path_to_directory/input.ttl`.|
|mmd|  Mermaid output including the full or relative path to the output file (e.g. `./mmd/BirthDeath_Fortin.mmd`).<br>User can provide their own **output path**, `/User/username/path_to_directory/output.mmd`.|

For example, to generate a diagram rendering instances using the `BirthDeath_Fortin.ttl` file in `./rdf` folder and the mermaid output to be stored in folder `./mmd`, the command is as follows:
```shell
$  python criteria.py instance ./rdf/BirthDeath_Fortin.ttl ./mmd/BirthDeath_Fortin.mmd
```
### rdf
This folder contains RDF files used for testing.
> - The tool can process **prefixes defined by users**.
> - RDF files do not need be stored in the **`/rdf`** folder.

### mmd
This folder contains mermaid outputs generated during testing. 
> - Output files are no longer stored in the **`/mmd`** folder by default. User can now provide their own output path.
>
> **Note**: While processing the triples, the script would grab all of them randomly, meaning user would not have much control about the order of statements in the .mmd. It also means that running the script over the same RDF file would generate slightly different Mermaid files (i.e. different order of statements), meaning different graphs (i.e. different positions of the nodes). However, the top node's position will remain the same.

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

## CRITERIA Users

CHIN would like to highlight the projects and institutions that use CRITERIA, thanks to which CHIN can improve the tool. If you use CRITERIA and your project is not listed below, do not hesitate to [contact us](#contact-us).

Project: [Reference Data Models](http://docs.swissartresearch.net/)

Organization: [Swiss Art Research Infrastructure, University of Zurich](http://swissartresearch.net/)

Description ([Source](https://docs.swissartresearch.net/)):
>The Semantic Reference Data Models project aims to create a series of re-usable templates of semantic pattern for facilitating the integration and querying of cultural heritage data sources. Each template is a collection of semantic patterns and it is grounded on the analysis of selected sources determined to be of relevance an entity. The developed semantic patterns are mapped to the CIDOC-CRM ontology to ensure compatibility across the heritage domain. The patterns can be used to provide reference implementations for institutions and projects not familiar with CIDOC-CRM, to create usable guidelines to generate input interfaces for born-CRM semantic data and to guide mapping processes from extant sources into the CRM conformant reference model using tools such as 3M.

## Contact us

For questions or comments regarding CRITERIA, please consult the [Issues](https://github.com/chin-rcip/CRITERIA/issues) section (and open an Issue if it is relevant) or contact us by email at the following address: [pch.RCIP-CHIN.pch@canada.ca](mailto:pch.RCIP-CHIN.pch@canada.ca)


# CRITERIA

CRITERIA (acronyme anglais de **C**idoc c**R**m **I**n **T**riples m**ER**maid d**I**agr**A**ms) est un outil Python permettant de convertir des fichiers RDF (basés sur le [modèle CIDOC CRM](http://www.cidoc-crm.org/)) en format [Mermaid](https://mermaid-js.github.io/mermaid/#/) markdown pour générer des diagrammes.

Cet outil peut générer deux types de diagrammes en utilisant un seul fichier RDF (qui doit toujours contenir des instances) :
* Le premier type de diagramme représente toutes les **instances**, p. ex. des URI, des dates et des valeurs littérales. 
* Le second type de diagramme représente les classes, c.-à-d. l'**ontologie** du patron conceptuel.

Le markdown est prévu pour être intégré à une page HTML; une version PNG peut néanmoins être téléchargée depuis un [éditeur Mermaid](https://mermaid-js.github.io/mermaid-live-editor) en copiant l'intégralité du fichier markdown dans la boîte de code. 

Pour ceux qui ne souhaitent pas utiliser directement le script, un [démonstrateur en ligne](http://chinrcip.pythonanywhere.com/) de CRITERIA est disponible.

Navigateurs recommandés pour l'éditeur Mermaid et le Démonstrateur en ligne :
* **Mac**: Safari, Chrome, Firefox
* **Windows**: Firefox

L'exemple ci-dessous illustre le patron conceptuel du Réseau canadien d'information sur le patrimoine (RCIP) pour les naissances/décès (l'exemple n'est disponible qu'en anglais à l'heure actuelle): 

##### RDF
* [BirthDeath_Fortin.ttl](/rdf/BirthDeath_Fortin.ttl)

##### Diagramme des instances
![Birth/Death of People pattern with instances](/docs/images/BirthDeath_Fortin.png)

##### Représentation de l'ontologie
![Ontology of Birth/Death of People pattern ](/docs/images/BirthDeathOnto.png)

## Installation
L'outil peut être installé en clônant ce répertoire ou en le téléchargeant en format .zip. 
Le fichier s'exécutera dans la console; voir [Utilisation](#utilisation) pour plus de détails sur la procédure à suivre.

### Exigences techniques
Les versions des langages de programmation suivantes sont nécessaires à l'exécution de l'outil :
- Python 3.7.0
- [rdflib 5.0.0](https://rdflib.readthedocs.io/en/stable/gettingstarted.html)
- [rdflib-jsonld 0.5.0](https://github.com/RDFLib/rdflib-jsonld)

## Utilisation

### criteria
Le principal script python est **`criteria.py`**; il exige **trois** arguments:
|Argument|Description|
|--|--|
|Type | Type du diagramme; les valeurs doivent être **`instance`** ou **`ontology`**|
|rdf|  Entrée RDF, incluant le chemin complet ou relatif au fichier d'entrée (p. ex. `./rdf/BirthDeath_Fortin.ttl`).<br><br>- L'outil peut exécuter **plusieurs formats** tels que **`Turtle`**, **`NTriples`**, **`RDF/XML`**, **`Trig`**, **`JSON-LD`**, etc.<br>- Les fichiers RDF ne doivent pas nécessairement être enregistrés dans le dossier `/rdf`. L'utilisateur peut utiliser un **chemin d'entrée** qui lui est particulier : `/User/username/path_to_directory/input.ttl`.|
|mmd|  Les données converties en Mermaid, incluant le chemin complet ou relatif au fichier extrant (p. ex. `./mmd/BirthDeath_Fortin.mmd`).<br>L'utilisateur peut soumettre son propre **chemin extrant** : `/User/username/path_to_directory/output.mmd`.|

Par exemple, pour générer un diagramme représentant les instances du fichier `BirthDeath_Fortin.ttl` se trouvant dans le dossier `./rdf` avec pour extrant un fichier mermaid `./mmd`, il faut exécuter la commande suivante :
```shell
$  python criteria.py instance ./rdf/BirthDeath_Fortin.ttl ./mmd/BirthDeath_Fortin.mmd
```
### rdf
Ce dossier contient les fichiers RDF utilisés à des fins de tests.
> - L'outil peut utiliser des **préfixes définis par l'utilisateur**.
> - Il n'est pas nécessaire de stocker les fichiers RDF dans le dossier **`/rdf`**.

### mmd
Ce dossier contient les extrants mermaid générés par les tests. This folder contains mermaid outputs generated during testing. 
> - Les fichiers RDF extrants ne sont pas stockés dans le dossier **`/mmd`** par défaut. L'utilisateur peut soumettre son propre chemin.
>
> **Note**: Pendant le traitement des triplets, le script les analysera de manière aléatoire, ce qui veut dire que l'utilisateur a très peu de contrôle sur l'ordre des énoncés dans le .mmd. De plus, le fait de lancer le script sur un même fichier RDF pourrait générer un fichier Mermaid un peu différent (soit un ordre différent des énoncés), donc aussi des diagrammes différents (soit une disposition différente des noeuds sémantiques). Cependant, la position du noeud sémantique initial restera le même.

### src
Le dossier **`/src`** contient les ressources utilisées par le script principal.

#### /templates 
Le dossier **`templates`** contient les gabarits utilisés pour générer les fichiers extrants `.mmd`. Les gabarits ont des classes  de style pré-définies : l'une pour visualiser les instances (`instance.mmd`) et l'autre pour visualiser l'ontologie (`ontology.mmd`). Le style par défaut est basé sur le thème CIDOC CRM (tel que l'a proposé George Bruseker).

Par exemple :
```
graph TD
classDef Literal fill:#f2f2f2,stroke:#000000;
classDef CRM_Entity fill:#FFFFFF,stroke:#000000;
classDef CRM_Entity_URI fill:#FFFFFF,stroke:#000000;
classDef Temporal_Entity fill:#00C9E6, stroke:#000000;
classDef Temporal_Entity_URI fill:#99f1ff,stroke:#000000;
```
> :warning: À l'heure actuelle, il est possible d'éditer *UNIQUEMENT les couleurs* dans les fichiers, veuillez ne **PAS changer le *nom des fichiers* ou le *nom des classes* !**

#### /ontologies
Le dossier **`ontologies`** contient les fichiers d'ontologie utilisés par le script. À l'heure actuelle, ce dossier contient les fichiers `.rdfs` de [CIDOC CRM (v6.2.1)](http://www.cidoc-crm.org/Version/version-6.2.1), [FRBRoo (v2.4)](http://www.cidoc-crm.org/frbroo/ModelVersion/frbroo-v.-2.4), [CRMpc (v1.1)](http://www.cidoc-crm.org/Version/version-6.2), et CRMdig (v3.2.2) (depuis l'application [3M de FORTH](https://isl.ics.forth.gr/3M/)).
> :warning: il est crucial que les classes `.rdfs` **soient alignées** avec les classes utilisées dans le `.ttl`
> Par exemple, si le fichier `.ttl` utilise `E24_Physical_Human-Made_Thing` mais que l'ontologie utilise `E24_Physical_Man-Made_Thing`, le fichier d'ontologie devra être édité en conséquence.

#### source
**`source.py`** est l'endroit où conserver les objets python qui doivent être importés par le script. Il contient actuellement :
- `classes`: une liste d'objets stockant les principales classes CIDOC CRM auxquelles seront appliqués les codes de couleur.
- `onto`: un objet-dictionnaire stockant les noms d'ontologies utilisées par le script (c.-à-d. les fichiers `.rdfs` dans le dossier `/ontologies`).
> :warning: si vous remplacez le fichier `.rdfs` du dossier `/ontologies` par un fichier mis à jour ou si vous le renommez, les **valeurs** dans le dictionnaire `onto` doivent être mises à jour en conséquence.

## Licence

CRITERIA est disponible sous licence [MIT License](https://github.com/chin-rcip/CRITERIA/blob/master/LICENSE). Pour rencontrer les critères d'attribution de cette licence, vous devez désigner le détenteur des droits en utilisant la formule suivante :

> Copyright (c) 2020 Canadian Heritage Information Network, Canadian Heritage, Government of Canada - Réseau Canadien d'information sur le patrimoine, Patrimoine canadien, Gouvernement du Canada

## Utilisateurs de CRITERIA

Le RCIP aimerait souligner les projets et institutions utilisant CRITERIA et grâce à qui l'outil peut être amélioré. Si vous utilisez CRITERIA et que votre projet n'est pas mentionné ci-dessous, n'hésitez pas à [nous contacter](#contactez-nous).

Projet: [Reference Data Models](http://docs.swissartresearch.net/)

Organisation: [Swiss Art Research Infrastructure, University of Zurich](http://swissartresearch.net/)

Description ([Source](https://docs.swissartresearch.net/)):
>The Semantic Reference Data Models project aims to create a series of re-usable templates of semantic pattern for facilitating the integration and querying of cultural heritage data sources. Each template is a collection of semantic patterns and it is grounded on the analysis of selected sources determined to be of relevance an entity. The developed semantic patterns are mapped to the CIDOC-CRM ontology to ensure compatibility across the heritage domain. The patterns can be used to provide reference implementations for institutions and projects not familiar with CIDOC-CRM, to create usable guidelines to generate input interfaces for born-CRM semantic data and to guide mapping processes from extant sources into the CRM conformant reference model using tools such as 3M.

## Contactez-nous

Pour toute question ou commentaire au sujet de  CRITERIA, veuillez consulter la section [Issues](https://github.com/chin-rcip/CRITERIA/issues) (et ouvrir une Issue si c'est pertinent) ou contactez-nous par courriel à l'adresse suivante: [pch.RCIP-CHIN.pch@canada.ca](mailto:pch.RCIP-CHIN.pch@canada.ca)
