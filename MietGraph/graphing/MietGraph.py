import itertools
import pathlib
import tempfile
import copy
from tqdm import tqdm

import json
import pathlib
import networkx as nx
import re

crosslink_dict = {}

def parse_jurabasic(file = "output/jurabasic.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f:
        content = json.load(f)

    g = nx.DiGraph()

    node_label=0
    g.add_node(node_label, name="JuraBasic", label="Lexikon")
    bgh_dict = {}
    for entry in content:
        node_label+=1
        for value in entry:
            entry[value] = str(entry[value])
        if "sub_title" in entry:
            node = {"url": entry["page_url"],
                    "title": entry["title"],
                    "section": entry["sub_title"],
                    "name": entry["title"] + ": " + entry["sub_title"],
                    "text": entry["text"],
                    "label": "Erklärung"}
        else:
            node = {"url": entry["page_url"],
                    "title": entry["title"],
                    "name": entry["title"],
                    "text": entry["text"],
                    "label": "Erklärung"}

        g.add_node(node_label, **node)
        crosslink_dict[node_label] = entry["crosslinks"]
        g.add_edge(node_label, 0, edgelabel="partof")

        if entry["text"].find("BGH"):
            bgh_entries = re.findall("VIII ZR \d+\/\d+", node["text"])
            for entry in bgh_entries:
                if entry not in bgh_dict:
                    bgh_dict["AZ: " + entry] = [node_label]
                else:
                    bgh_dict["AZ: " + entry].append(node_label)

    for key, value in bgh_dict.items():
        bgh_node = {"name": key,
                    "label": "BGH-Urteil"}
        g.add_node(key, **bgh_node)
        for v in value:
            g.add_edge(key, v, edgelabel="bgh")

    node_label=0
    for entry in content:
        targets = [x for x in g.nodes if g.nodes[x].get("url","None") in entry["crosslinks"]]
        for t in targets:
            if node_label != t:
                g.add_edge(node_label, t, edgelabel="crosslink")
        node_label+=1
    return g

def parse_mietrechteinfach(file = "output/mietrechteinfach.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f:
        content = json.load(f)

    g=nx.DiGraph()

    node_label=10000
    g.add_node(node_label, name="MietrechtEinfach", label="Lexikon")
    for entry in content:
        node_label+=1
        for value in entry:
            entry[value] = str(entry[value])
        node = {"url": entry["page_url"],
                "name": entry["title"],
                "title": entry["title"],
                "text": entry["text"],
                "label": "Erklärung"}
        g.add_node(node_label, **node)
        crosslink_dict[node_label] = entry["crosslinks"]
        g.add_edge(node_label, 10000, edgelabel="partof")

    node_label=10000
    for entry in content:
        targets = [x for x in g.nodes if g.nodes[x].get("url","") in entry["crosslinks"]]
        for t in targets:
            if node_label != t:
                g.add_edge(node_label, t, edgelabel="crosslink")
        node_label+=1
    return g

def parse_mietrechtlexikon(file = "output/mietrechtlexikon.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f:
        content = json.load(f)

    g=nx.DiGraph()

    node_label=20000
    g.add_node(node_label, name="MietrechtLexikon", label="Lexikon")
    for entry in content:
        node_label+=1
        for value in entry:
            entry[value] = str(entry[value])
        node = {"url": entry["page_url"],
                "name": entry["title"] + ": " + entry["sub_title"],
                "title": entry["title"],
                "section": entry["sub_title"],
                "text": entry["text"],
                "label": "None"}
        g.add_node(node_label, **node)
        crosslink_dict[node_label] = entry["crosslinks"]
        g.add_edge(node_label, 20000, edgelabel="partof")

    node_label=20000
    for entry in content:
        targets = [x for x in g.nodes if g.nodes[x].get("url","") in entry["crosslinks"]]
        for t in targets:
            if node_label != t:
                g.add_edge(node_label, t, edgelabel="crosslink")
        node_label+=1
    return g

def parse_bgb(file = "output/bgb.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f:
        content = json.load(f)

    g=nx.DiGraph()

    node_label=30000
    g.add_node(node_label, name="BGB", label="Lexikon")
    for entry in content:
        node_label+=1
        for value in entry:
            entry[value] = str(entry[value])
        node = {"url": entry["page_url"],
                "name": entry["title"],
                "title": entry["title"],
                "text": entry["text"],
                "label": "Gesetzestext"}
        g.add_node(node_label, **node)
        g.add_edge(node_label, 30000, edgelabel="partof")
    return g

def parse_bmgev(file = "output/bmgev.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f:
        content = json.load(f)

    g=nx.DiGraph()

    node_label=40000
    g.add_node(node_label, name="BMGEV", label="Lexikon")
    bgh_dict = {}
    for entry in content:
        node_label+=1
        for value in entry:
            entry[value] = str(entry[value])
        node = {"url": entry["page_url"],
                "name": entry["title"] + ": " + entry["sub_title"],
                "title": entry["title"],
                "section": entry["sub_title"],
                "text": entry["text"],
                "label": "Ratgeber"}
        g.add_node(node_label, **node)
        crosslink_dict[node_label] = entry["crosslinks"]
        g.add_edge(node_label, 40000, edgelabel="partof")

        if entry["text"].find("BGH"):
            bgh_entries = re.findall("AZ: VIII ZR \d+\/\d+", node["text"])
            for entry in bgh_entries:
                if entry not in bgh_dict:
                    bgh_dict[entry] = [node_label]
                else:
                    bgh_dict[entry].append(node_label)

    for key, value in bgh_dict.items():
        bgh_node = {"name": key,
                    "label": "BGH-Urteil"}
        g.add_node(key, **bgh_node)
        for v in value:
            g.add_edge(key, v, edgelabel="bgh")

    node_label=40000
    for entry in content:
        targets = [x for x in g.nodes if g.nodes[x].get("url","None") in entry["crosslinks"]]
        for t in targets:
            if node_label != t:
                g.add_edge(node_label, t, edgelabel="crosslink")
        node_label+=1
    return g


def parse_rechtslexikon(file = "output/rechtslexikon.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f:
        content = json.load(f)

    g=nx.DiGraph()

    node_label=50000
    g.add_node(node_label, name="Rechtslexikon", label="Lexikon")
    for entry in content:
        node_label+=1
        for value in entry:
            entry[value] = str(entry[value])
        node = {"url": entry["page_url"],
                "name": entry["title"],
                "title": entry["title"],
                "text": entry["text"],
                "label": "None"}
        g.add_node(node_label, **node)
        g.add_edge(node_label, 50000, edgelabel="partof")

    node_label=50000
    for entry in content:
        targets = [x for x in g.nodes if g.nodes[x].get("url","") in entry["crosslinks"]]
        for t in targets:
            if node_label != t:
                g.add_edge(node_label, t, edgelabel="crosslink")
        node_label+=1
    return g

def recursive_compose(l):
    if len(l) == 0:
        return None
    if len(l) <2:
        return l[0]
    if len(l) == 2:
        return nx.compose(l[0],l[1])
    else:
        return nx.compose(l[0], recursive_compose(l[1:]))

def compare_two_graphs(g1, g2):
    print("\n--------------------------")
    print(f"{g1.graph['name']} vs. {g2.graph['name']}")
    common_nodes=set(g1).intersection(set(g2))
    print(f"Nodes in common ({len(common_nodes)}):")
    print(list(common_nodes)[:10])

    compose_greaph = nx.compose(g1,g2)
    print("Graph1 No. edges:", len(g1.edges))
    print("Graph1 No. edges:", len(g2.edges))
    print("Graph1 No. edges:", len(compose_greaph), "|Difference:", (len(g1.edges)+len(g2.edges))-len(compose_greaph.edges))
    print("-----------------------------\n\n")

class MietGraph:
    def __init__(self, dir="output/"):
        """
        Initilialize the Graph
        :param dir: The output directory of the crawling process
        """
        dir=pathlib.Path(dir)
        self.jb = parse_jurabasic(dir / "jurabasic.json")
        self.mre = parse_mietrechteinfach(dir / "mietrechteinfach.json")
        self.mrl = parse_mietrechtlexikon(dir / "mietrechtlexikon.json")
        self.bgb = parse_bgb(dir / "bgb.json")
        self.bmgev = parse_bmgev(dir / "bmgev.json")
        self.rl = parse_rechtslexikon(dir / "rechtslexikon.json")

        self.all = [self.jb,
                    self.mre,
                    self.mrl,
                    self.bgb,
                    self.bmgev,
                    self.rl]

        self.graph = recursive_compose(self.all)

    def compare_parts(self):
        """
        Compare the single graphs pair wise
        :return:
        """
        for comb in itertools.combinations(self.all, 2):
            compare_two_graphs(*comb)

    def to_gexf(self, file="mietgraph.gexf"):
        """
        Write to GEXF format
        :param file:
        :return:
        """
        nx.write_gexf(self.graph, file)

    def to_gml(self, file="mietgraph.gml"):
        """
        Write to GML format
        :param file:
        :return:
        """
        nx.write_gml(self.graph, file)

    def to_graphml(self, file="mietgraph.graphml"):
        """
        Write to GraphML format
        :param file:
        :return:
        """
        nx.write_graphml(self.graph, file)

    def to_pickle(self, file="mietgraph.p"):
        """
        Write to GraphML format
        :param file:
        :return:
        """
        nx.write_gpickle(self.graph, file)

    def igraph(self):
        """
        Return an igraph version of the graph
        :return:
        """
        try:
            import igraph as ig
        except:
            print("igraph not installed.")
            return None

        with tempfile.TemporaryDirectory() as f:
            self.to_gml(f+"/tmp.gml")
            g = ig.read(f+"/tmp.gml")
        return g

    def stats(self):
        """
        Print some figures
        :return:
        """
        print("Stats:")
        print(f"Nodes: {len(self.graph.nodes)}")
        print(f"Edges: {len(self.graph.edges)}")
        print(f"Density: {nx.density(self.graph)}")

    def attribute_set(self):
        """
        Give a list of all available node attributes
        :return:
        """
        attr_set = set([x for k,v in dict(self.graph.nodes(True)).items() for x in v.keys()])
        frequency = dict(zip(attr_set, [0 for _ in range(len(attr_set))]))
        for k, v in dict(self.graph.nodes(True)).items():
            for x in v.keys():
                frequency[x] = frequency[x]+1
        frequency = {k:v/len(self.graph) for k,v in frequency.items()}
        return attr_set, frequency

    def add_crosslinks(self):
        c  = copy.deepcopy(self.graph.nodes(True))
        for node, attr in c:
            for label in crosslink_dict:
                if "url" in attr and attr["url"] in crosslink_dict[label] and node != label:
                    self.graph.add_edge(node, label, edgelabel="crosslink")

    def add_keyword_in_text(self, check=["text", "title", "crosslinks"]):
        """
        Add a connection if the title of a keyword node occurrs in an attribute of some other node.
        :param check:  the attribute list to check if a keyword occurrs
        :return:
        """

        node_dict = {}
        stopwords = ["Kündigung", "Miete", "Mietvertrag", "Mieter", "Vermieter"]
        for node, attr in self.graph.nodes(True):
            if "title" in attr:
                node_dict.update({attr["title"]:node})
        #print(dict)

        keywords = [x[1].get("title") for x in self.graph.nodes(True) if "jura-basic" not in x[1].get("url","") and x[1].get("title") is not None]
        for val in check:
            for node, attr in tqdm(self.graph.nodes(True)):
                if not val in attr:
                    continue
                contains = [kw for kw in keywords if " " + kw + " "  in attr[val] and kw not in stopwords]
                contains = list(set(contains))
                #print(contains)
                self.graph.add_weighted_edges_from([(node, node_dict[kw], 0.5) for kw in contains if node != node_dict[kw]], edgelabel="keyword")

        node_dict = {}
        for node, attr in self.graph.nodes(True):
            if "section" in attr:
                node_dict.update({attr["section"]:node})

        keywords = [x[1].get("section") for x in self.graph.nodes(True) if "jura-basic" in x[1].get("url", "") and x[1].get("section") is not None]
        #print(keywords)
        for val in check:
            for node, attr in tqdm(self.graph.nodes(True)):
                if not val in attr:
                    continue
                contains = [kw for kw in keywords if " " + kw + " "  in attr[val] and kw not in stopwords]
                contains = list(set(contains))
                #print(contains)
                self.graph.add_weighted_edges_from([(node, node_dict[kw], 0.5) for kw in contains if node != node_dict[kw]], edgelabel="keyword")

    def highest_ranked_neighbours(self, q):
        """
        Rank the graph with a pagerank and return a sorted list of all neighbours of q
        :param q: a string query (must be a node in the graph)
        :return: list of (node, pagerank) tuples. sorted
        """
        r = nx.pagerank(self.graph)
        neighbours = list(set([x if x != q else y for x,y in list(self.graph.in_edges(q)) + list(self.graph.out_edges(q))]))
        neighbour_scores = [(n,r[n]) for n in neighbours]

        neighbour_scores.sort(key=lambda x: -x[1])
        return neighbour_scores

    def add_pagerank(self):
        """
        Add the page rank coeefficient
        :return:
        """
        r = nx.pagerank(self.graph)
        weights = {k: {"pagerank": v} for k, v in r.items()}
        nx.set_node_attributes(self.graph, weights)

    def add_clustering(self):
        """
        Add clustering coefficient
        :return:
        """
        r = nx.clustering(self.graph)
        weights = {k: {"clustercoefficient": v} for k, v in r.items()}
        nx.set_node_attributes(self.graph, weights)

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--format', dest='format', default="graphml",
                        help='Choose between .gexf, .gml, and .graphml. (default: graphml)')
    parser.add_argument('--output', dest='output', default="MietGraph.graphml",
                        help='Where to save the file.')
    parser.add_argument('--input', dest='input', default="input/",
                        help='The result file of the crawling process')

    args = parser.parse_args()

    mg = MietGraph(args.input)
    mg.add_keyword_in_text()
    mg.add_crosslinks()
    mg.stats()

    if args.output.endswith(args.format):
        if args.format.endswith("gexf"):
            mg.to_gexf(args.output)
        elif args.format.endswith("gml"):
            mg.to_gml(args.output)
        elif args.format.endswith("graphml"):
            mg.to_graphml(args.output)
    else:
        if args.format.endswith("gexf"):
            mg.to_gexf(args.output+"."+ args.format.replace(".",""))
        elif args.format.endswith("gml"):
            mg.to_gml(args.output + "." + args.format.replace(".", ""))
        elif args.format.endswith("graphml"):
            mg.to_graphml(args.output + "." + args.format.replace(".", ""))

if __name__ == "__main__":
    main()
# bg = MietGraph("output/")
# bg.add_keyword_in_text()
# bg.graph
