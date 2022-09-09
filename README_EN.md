# Ultima Patagonia Cave Project




## What this project is about


- [Ultima Patagonia Cave Project](#ultima-patagonia-cave-project)
  - [Contribute](#contribute)
  - [View](#view)
  - [Downloads](#downloads)
  - [Prerequisites](#prerequisites)

## How to contribute

## Prerequisites

To compile the data and draw surveys you will need some software installed.

For compiling and exporting:

- [Therion](https://therion.speleo.sk/download.php) - The main thing.
- [Survex](https://survex.com/download.html) - Used by Therion to generate `.3D` files.

For drawing we are using Inkscape and the Therion Inkscape extensions because we think its nicer than using the Therion editor:

- [Inkscape](https://inkscape.org) - Vector drawing program
- [Inkscape Therion Extensions](https://github.com/speleo3/inkscape-speleo/) - The extensions that allow you to draw Therion scraps in Inkscape.

(Optional) For editing the text files:

- [VSCode](https://code.visualstudio.com/Download)
- [VSCode Therion Extension](https://marketplace.visualstudio.com/items?itemName=rhystyers.therion)

## Therion Glossary

Therion has a complex vocabulary of its own so here is a basic translation.

### Internal Data

- **survey** : main data structure, which can be nested _ad nauseam_ to represent karst areas, caves or passages. Each survey has an object id, which must be unique within the scope of the higher level survey. Likewise, any object within a survey has unique id (from stations, to maps, scraps)
- **centreline**: survey data specification., with syntex mostly derived from Survex,
- **Scrap** - The most basic drawing element, a piece of 2D map. It will consist of the walls and stations of the passage as well as lots of extra information (should you choose to draw it!) like boulders, pits, passage gradients etc. A single set of survey data (a single passage) can have many scraps associated with it. It is often good to split the drawing over many scraps as this allows Therion to do clever things (like depth colouring). Scraps cannot overlap themselves.
- **Map** - The higher level drawing element. A map can be made of scraps, or it can be a map of maps. Maps are how you collect individual drawn passages into larger blocks. For example a passage like Aqueduct will have its scraps collected in a map called `m-all-p` (). A bigger map might be called `m-below_klic_globin-p` and contain maps from Aqueduct and many other passages (e.g. m-all-p@aqueduct, m-all-p@klic_globin, etc...). The `m-below_klic_globin` will be collected into an Primadona map `m-all-p@Primadona` with all the other maps in Primadona and finally that will collected with the maps from Vrntarija and the old system into a full System Migovec map. The advantage of this heirarchical structure is that you can export these maps at any level, whether you want an overview of the full system or a higher resolution look at the pushing front.
