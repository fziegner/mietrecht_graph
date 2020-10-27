# MietGraph

Creating a knowledge graph about the rent stuff.
This is a fork of [BauGraph](https://git.informatik.uni-leipzig.de/dmw/civil_engineering/bauprofessor_crawler)


## Create the graph
To create the graph there are two steps. First we have to crawl a few websites then we create the graph.


1. Clone the repository ```git clone https://git.informatik.uni-leipzig.de/information_extraction_group/bauprofessor_crawler.git```
2. Change into the repository folder and install the necessary requirements with ```pip install -r requirements.txt```
3. Change into the directory ```cd MietGraph/crawling``` and run the crawling with ```./run.sh [output_folder]```
4. Change to MietGraph/graphing, move the output from step 3 to a folder for input and run ```python MietGraph.py --input=[input_folder] --output=MietGraph.graphml``` to generate the graph. (```python MietGraph.py -h``` for more options)
5. ???
6. Profit

The output formats ".gml", ".gexf" and ".graphml" can all be used with gephi.

## Installation
You should also be able to install the package with ```pip install .``` from the repository's base directory.
After that you can invoke the MietGraph class and generate the Graph in python environment.

```python
>> from MietGraph import MietGraph
>> g = MietGraph("input/")
>> g.add_keyword_in_text()
>> g.add_crosslinks()
>> g.graph
<networkx.classes.digraph.DiGraph at 0x7f38243927c0>
```
You can also get a igraph representation with
```
g.igraph()
```
You can use this to manipulate the graph further. More Information coming up..

-------

KnowledgeBase

```python
import MietGraph
kb = MietGraph.KnowledgeBase("name of your knowledge base file")

# See a list of contained documents
docs = kb.list_documents()

# Get all neighbours of a document with all attributes
kb.get_neighbors(docs[0], True)

#See the content of the document
kb.get_attr(docs[0], "content")

# Show document names of similar documents
kb.most_similar(docs[0])

# you can also add new pdfs to the knowledgebase
kb.add("path_to_new_pdf.pdf")

# And save the modified graph
kb.save("save.graphml")
```
