import networkx as nx
import spacy
import pickle
import pathlib
import pdftotext
import re
# import mlmc

from tqdm import tqdm
import requests
import string


class KnowledgeBase:
    def __init__(self, path):
        self.path = path

        suffix = path.split(".")[-1]
        if suffix == "gexf":
            self.kb = nx.read_gexf(path)
        elif suffix == "gml":
            self.kb = nx.read_gml(path)
        elif suffix == "gp":
            self.kb = nx.read_gexf(path)
        elif suffix == "p":
            with open(path,"r") as f:
                self.kb = pickle.load(f)
        else:
            print("Unknown file suffix, nothing loaded.")

    def save(self, path):
        suffix = path.split(".")[-1]
        if suffix == "gexf":
            nx.write_gexf(self.kb, path)
        elif suffix == "gml":
            nx.read_gml(self.kb, path)
        elif suffix == "gp":
            nx.read_gexf(self.kb, path)
        elif suffix == "p":
            with open(path,"w") as f:
                pickle.dump(self.kb, f)
        else:
            print("Unknown file suffix, nothing loaded.")



    def wiki(self):
        abstracts = {}
        batch_size = 20
        for ind in tqdm(list(range(0, len(self.kb), batch_size))):
            batch = list(self.kb)[ind:(ind + batch_size)]
            batch_mapping = {
                n: "".join([i for i in n.replace("&amp;", " and ") if i in string.ascii_letters + " &"]).split("  ")[-1]
                for n in batch}
            url = "https://de.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro&explaintext&redirects=1&titles=" + "|".join(
                batch_mapping.values())
            r = requests.get(url)
            data = r.json()
            mappings = {}
            if "redirects" in data["query"]:
                mappings = {x["from"]: x["to"] for x in data["query"]["redirects"]}

            extract_dict = {v["title"]: {"extract": v["extract"], "pageid": v["pageid"]} for k, v in
                            data["query"]["pages"].items() if int(k) > 0}
            for b in batch:
                if mappings.get(batch_mapping[b], batch_mapping[b]) in extract_dict.keys():
                    abstracts[b] = extract_dict.get(mappings.get(batch_mapping[b], batch_mapping[b]))
        nx.set_node_attributes(self.kb, abstracts)

    @staticmethod
    def read_pdf(path):
        with open(path, "rb") as f:
            pdf = pdftotext.PDF(f)
            content = "\n\n".join(pdf)
        return content

    def exact_token_matches(self, content):
        matches = [(x,{}) for x in content if x in self.kb]
        return matches

    def exact_lemma_matches(self, content):
        matches = [(x,{}) for x in content if x in self.kb]
        return matches

    def entities(self, content):
        if not hasattr(self, "stanza"):
            from stanza import Pipeline
            self.stanza = Pipeline(lang="de", processors='tokenize,ner', use_gpu=False)
        doc = self.stanza(content)
        return [(ent.text,{"type": ent.type}) for ent in doc.ents]

    def mwu(self, content):
        doc = self.spacy(content)
        return [(ent.text,ent.type) for ent in doc.ents]

    # def embed(self, content):
    #     if not hasattr(self, "embedder"):
    #         self.embedder = mlmc.representation.Embedder("glove300")
    #     if not hasattr(self, "node_embeddings"):
    #         self.node_embeddings = self.embedder.embed(list(self.kb.nodes), pad=10).mean(1)
    #
    #     content = self.embedder.embed(content)[0].mean(0)[None]
    #     sim = (self.node_embeddings*content).sum(-1)


    @staticmethod
    def clean(x):
        x = re.sub("[ \n]+", " ", x)
        x = re.sub("\n+", " ", x)
        x = re.sub("_", " ", x)
        return "".join([c for c in x if c in string.ascii_letters+string.digits+string.whitespace+"äöüÄÖÜß-!.,?()/&§_"])


    def matching_nodes(self, content, similarity="exact", clean = True):
        similarity = similarity if isinstance(similarity, list) else [similarity]
        if clean:
            content = self.clean(content)
        if not hasattr(self, "spacy"):
            import spacy
            self.spacy = spacy.load("de_core_news_sm")

        # Caching
        self._content = content
        self._tokenized_content = re.split("[ \n]", content)
        doc = self.spacy(content)
        self._lemmas_content = [x.lemma_ for x in doc if x.lemma_!=x.text and x.pos_ == "NOUN"]


        nodes = self.exact_token_matches(self._tokenized_content)
        nodes += self.exact_lemma_matches(self._tokenized_content)
        nodes += self.entities(self._content)
        # nodes += self.embed(self._content)
        return nodes

    def add(self, file):
        """
        Add a file to the graph.
        :param file: link to a pdf file
        """
        edges = self.matching_nodes(kb.read_pdf(file), clean=True)
        self.kb.add_node(file.name, content=self._content, type="document")
        for edge in edges:
            if len(edge[1])>0:
                self.kb.add_node(edge[0], **edge[1])
        nodes = list(set([x[0] for x in edges]))

        for node in nodes:
            self.kb.add_edge(node, file.name)
        print(f"Added {file.name} to KB with {len(nodes)} edges.")

    def list_documents(self):
        """
        List all documents in the graph
        """
        return [x[0] for x in self.kb.nodes(True) if x[1].get("type", "no") == "document"]

    def get_neighbors(self, doc, attr=False):
        """
        Get all neighbours of a node
        :param doc: name of the document
        :param attr: If True will return all attributes of neighbouring nodes (default:false).
        :return: List of neighbouring nodes, or list of tuples.
        """
        if attr:
            tmp_d = self.kb.nodes(True)
            return list((x[0],tmp_d[x[0]]) for x in self.kb.in_edges(doc))
        else:
            return list(x[0] for x in self.kb.in_edges(doc))

    def get_attr(self, doc, attr):
        """
        retrieve an attribute of a node
        :param doc:  name of the node
        :param attr:  name of the attribute
        :return: content of the attribute
        """
        tmp_d = self.kb.nodes(True)
        return tmp_d[doc][attr]

    def most_similar(self, doc, return_nodes=False):
        """
        Return a list of documents in the graph sorted by similarity to a given document.
        Similarity is the number of common keywords.

        :param doc: name of a documents.
        :param return_nodes: if True returns a list of the keywords both docuemtns have in common (default: False)
        :return:
        """
        documents = {x: self.get_neighbors(x) for x in self.list_documents()}
        x = documents[doc]

        def wic(x, y):
            return set(x).intersection(set(y))

        if return_nodes:
            similarity = [(k,wic(x,v)) for k,v in documents.items()]
            similarity.sort(key=lambda x: len(x[1]))
        else:
            similarity = [(k,len(wic(x,v))/len(x) ) for k,v in documents.items()]
            similarity.sort(key=lambda x: x[1])
        return similarity

    def document_subgraph(self, doc, depth=1):
        """
        Returns a subgraph of the knowledge base starting from a document node.
        It adds all neighbours of the document to the graph.
        :param doc: Name of the document
        :param depth: number of steps allowed. ( If depht is two all nodes that are reachable in pathlength 2 are considered)
        :return:
        """
        nodes = [doc]
        for i in range(depth):
            nodes += sum([self.get_neighbors(x) for x in nodes],[])
        self.kb.subgraph(nodes)


# dir = pathlib.Path("/home/jb/DataMiningProject/Aedificon/HFW Leipzig/Ausschreibungsunterlagen")
# ex1 = "VU2107_EignungserklärungNUN_2016_FBL108.pdf"
# ex2 = "VU2105a_EU_Verpflichtungserklaerung_Unternehmen_2016_FBL105b.pdf"


# kb = KnowledgeBase("/home/jb/bauprofessor.gexf")
# kb.wiki()
# kb.save("/home/jb/bauprofessor_wiki2.gexf")

# for f in dir.glob("**/*.pdf"):
#     kb.add(f)

# kb.save("/home/jb/bauprofessor_wiki2_aedificon.gexf")

# prior = [0 for _ in range(len(kb.kb))]
# prior = {k:0 for k in kb.kb}
# prior["VU2107_EignungserklärungNUN_2016_FBL108.pdf"]=1
# for neighbour, node in list(kb.kb.in_edges("VU2107_EignungserklärungNUN_2016_FBL108.pdf")):
#     prior[neighbour]=1
# result = nx.pagerank(kb.kb, nstart=prior)
