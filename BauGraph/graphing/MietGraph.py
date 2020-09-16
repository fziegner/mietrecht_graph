import itertools
import pathlib
import tempfile
from tqdm import tqdm

import json
import pathlib
import networkx as nx

def parse_jurabasic(file = "output/jurabasic.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f:
        content = json.load(f)
    g=nx.DiGraph()
    g.graph["name"] = "jurabasic"

    node_label=0
    for entry in content:
        if "sub_title" in entry:
            node = {"url": entry["page_url"],
                    "text": entry["text"],
                    "name": entry["title"],
                    "name2": entry["sub_title"]}
        else:
            node = {"url": entry["page_url"],
                    "text": entry["text"],
                    "name": entry["title"]}
        g.add_node(node_label, **node)
        g.add_edge(node_label, "JuraBasic", t="partof")
        node_label+=1

    node_label=0
    for entry in content:
        targets = [x for x in g.nodes if g.nodes[x].get("url","") in entry["crosslinks"]]
        for t in targets:
            g.add_edge(node_label, t, t="crosslink")
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
    g.graph["name"] = "mietrechteinfach"

    for entry in content:
        node = {"url": entry["page_url"],
                "text": entry["text"],
                "name": entry["title"]}
        g.add_node(entry["title"], **node)
        g.add_edge(entry["title"], "MietrechtEinfach", t="partof")

    for entry in content:
        targets = [x for x in g.nodes if g.nodes[x].get("url","") in entry["crosslinks"]]
        for t in targets:
            g.add_edge(entry["title"], t, t="crosslink")
    return g

def parse_mietrechtlexikon(file = "output/mietrechtlexikon.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f:
        content = json.load(f)

    g=nx.DiGraph()
    g.graph["name"] = "mietrechtlexikon"

    for entry in content:
        node = {"url": entry["page_url"],
                "text": entry["text"],
                "name": entry["title"]}
        g.add_node(entry["title"], **node)
        g.add_edge(entry["title"], "MietrechtLexikon", t="partof")

    for entry in content:
        targets = [x for x in g.nodes if g.nodes[x].get("url","") in entry["crosslinks"]]
        for t in targets:
            g.add_edge(entry["title"], t, t="crosslink")
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

        self.all = [self.jb,
                    self.mre,
                    self.mrl]
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

    def add_keyword_in_text(self, check=["text", "title", "crosslinks"]):
        """
        Add a connection if the title of a keyword node occurrs in an attribute of some other node.
        :param check:  the attribute list to check if a keyword occurrs
        :return:
        """
        keywords = [x[0] for x in self.graph.nodes(True) if x[1].get("t", "") == "keyword"]

        for val in check:
            for node, attr in tqdm(self.graph.nodes(True)):
                if not val in attr:
                    continue
                contains = [kw for kw in keywords if " " + kw + " "  in attr[val]]
                self.graph.add_weighted_edges_from([(node, kw, 0.5) for kw in contains if node != kw])

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
    parser.add_argument('--format', dest='format', default="gml",
                        help='Choose between .gexf and .gml. (default: gml)')
    parser.add_argument('--output', dest='output', default="MietGraph.gml",
                        help='Where to save the file.')
    parser.add_argument('--input', dest='input', default="output/",
                        help='The result file of the crawling process')

    args = parser.parse_args()

    b = MietGraph(args.input)
    b.add_keyword_in_text(check=["url", "text", "name", "name2", "crosslinks"])
    b.stats()

    if args.output.endswith(args.format):
        if args.format.endswith("gexf"):
            b.to_gexf(args.output)
        elif args.format.endswith("gml"):
            b.to_gml(args.output)
    else:
        if args.format.endswith("gexf"):
            b.to_gexf(args.output+"."+ args.format.replace(".",""))
        elif args.format.endswith("gml"):
            b.to_gml(args.output + "." + args.format.replace(".", ""))

# #
# # if __name__ == "__main__":
# #     main()
#
# bg = MietGraph("output/")
# bg.add_keyword_in_text()
# bg.graph
