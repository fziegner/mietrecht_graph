import itertools
import pathlib
import tempfile
from tqdm import tqdm

import json
import pathlib
import networkx as nx

# hoai_file = ""
def parse_hoai(file = "output/hoai.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f: content = json.load(f)
    # node_list = list(set("".join(entry["title"]) for entry in content))

    g=nx.DiGraph()
    g.add_node("HOAI")
    g.graph["name"] = "hoai"
    # g.add_nodes_from(["HOAI"] + node_list)

    attributes = {}
    for entry in content :
        node = {"t": entry["type"],
                "url": entry["page_url"],
                # "text": entry["text"]
                }

        if node["t"] == "LP":
            node["paragraph"] = entry["paragraph"]
        else:
            node["doctitle"] = entry["doc_title"]
            node["honorar"] = json.dumps(entry["honorar"])

        g.add_node(entry["title"], **node)
        g.add_edge(entry["title"], "HOAI", t="partof")

    for entry in content:
        try:
            connect_targets = [x for x in g.nodes if g.nodes[x].get("url","") == entry["previous"]]
            g.add_edge(entry["title"], connect_targets[0], t="previous")
        except:pass
        try:
            connect_targets = [x for x in g.nodes if g.nodes[x].get("url","") == entry["next"]]
            g.add_edge(entry["title"], connect_targets[0], t="next")
        except:pass
    return g


def parse_bDIN(file="output/baunormenlexikondin.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f:
        content = json.load(f)
    g = nx.DiGraph()
    g.add_node("DIN", url="")
    g.graph["name"] = "din"

    for entry in content:
        node = {"t":entry["norm"],
                "url": entry["page_url"],
                # "text": "".join(entry["text"])
        }
        g.add_edge(entry["title"], "DIN", t="partof")
        g.add_node(entry["title"], **node)
    for entry in content:
        if len(entry["key_phrases"]) > 0:
            for url, phrase in entry["key_phrases"]:
                g.add_node(phrase, url=url)
                g.add_edge(entry["title"], phrase)

    for entry in content:
        connect_targets = [x for x in g.nodes if g.nodes[x]["url"] in entry["related"]]
        for n in connect_targets:
            g.add_edge(entry["title"], n, t="related")
    return g



def parse_bVOB(file="output/baunormenlexikonvob.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f:
        content = json.load(f)
    g = nx.DiGraph()
    g.add_node("VOB", url="")
    g.graph["name"] = "vob"
    for entry in content:
        node = {"t":entry["norm"],
                "url": entry["page_url"],
                # "text": "".join(entry["text"])
        }
        g.add_edge(entry["title"], "VOB", t="partof")
        g.add_node(entry["title"], **node)
    for entry in content:
        if len(entry["key_phrases"]) > 0:
            for url, phrase in entry["key_phrases"]:
                g.add_node(phrase, url=url)
                g.add_edge(entry["title"], phrase)
    for entry in content:
        connect_targets = [x for x in g.nodes if g.nodes[x]["url"] in entry["related"]]
        for n in connect_targets:
            g.add_edge(entry["title"], n, t="related")
    return g


def parse_bauprofessor(file = "output/bauprofessor.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f: content = json.load(f)
    # node_list = list(set("".join(entry["title"]) for entry in content))

    g=nx.DiGraph()
    g.graph["name"] = "bauprofessor"

    for entry in content:
        node = {"url": entry["page_url"],
                "text": entry["text"],
                "category": entry["category"],
                }
        g.add_node(entry["title"], **node)

    for entry in content:
        for kw in  entry["keywords"]:
            if not kw in g: g.add_node(kw, t="keyword")
            g.add_edge(entry["title"], kw, t="keyword")
        targets = [x for x in g.nodes if g.nodes[x].get("url","") in entry["crosslinks"]]
        for t in targets:
            g.add_edge(entry["title"], t, t="crosslink")
        targets = [x for x in g.nodes if g.nodes[x].get("url","") in entry["related_term"]]
        for t in targets:
            g.add_edge(entry["title"], t, t="related")
    return g



def parse_beuthlex(file = "output/beuthlex.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f: content = json.load(f)
    g=nx.DiGraph()
    g.add_node("Lexikon", url = "", t="LexikonRoot")
    g.graph["name"] = "beuthlex"
    from bs4 import BeautifulSoup
    targets = {}
    for entry in content:
        html = BeautifulSoup("".join(entry["text"]),'html.parser')
        targets[entry["title"]] = ['http://baulexikon.beuth.de/'+x["href"] for x in html.find_all('a') if ".HTM" in x["href"] ]
        node = {"url": entry["page_url"],
                "text": html.text,
                "t": "keyword"
                }
        g.add_node(entry["title"], **node)
        g.add_edge(entry["title"], "Lexikon", t="partof")
    for k,v in targets.items():
        for t in [(x[0],x[1]["url"]) for x in g.nodes(True)  if x[1]["url"] in v]:
            if t[1] not in g:g.add_node(t[0],url=t[1])
            g.add_edge(k,t,t="related")
    return g



def parse_hb(file = "output/hb.json"):
    file = pathlib.Path(file)
    if not file.exists():
        print(f"No such file: {file.name}.")
        return False

    with open(file, "r") as f: content = json.load(f)
    g=nx.DiGraph()
    g.add_node("Lexikon", url="", t="LexikonRoot")
    g.graph["name"] = "Hausbauberater"
    from bs4 import BeautifulSoup
    targets = {}
    for entry in content:
        html = BeautifulSoup("".join(entry["text"]), 'html.parser')
        targets[entry["title"]] = ['https://www.hausbauberater.de' + x["href"] for x in html.find_all('a') ]

        node = {"url": entry["page_url"],
                "text": html.text,
                "t": "keyword"
                }
        g.add_node(entry["title"], **node)
        g.add_edge(entry["title"], "Lexikon", t="partof")

    for k, v in targets.items():
        for t in [x[0] for x in g.nodes(True)  if x[1]["url"] in v]:
            g.add_edge(k, t, t="related")

    for entry in content:
        if len(entry["synonym"]) == 0:
            continue
        synonyms = [x.strip() for x in entry["synonym"][0].split("\n")[1].split(", ")]

        for s in synonyms:
            g.add_node(s, t="keyword")
            g.add_edge(entry["title"], s, t="synonym")

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



class BauGraph:
    def __init__(self, dir="output/"):
        """
        Initilialize the Graph
        :param dir: The output directory of the crawling process
        """
        dir=pathlib.Path(dir)
        self.hoai = parse_hoai(dir / "hoai.json")
        self.din = parse_bDIN(dir / "baunormenlexikondin.json")
        self.vob = parse_bVOB(dir / "baunormenlexikonvob.json")
        self.bp = parse_bauprofessor(dir / "bauprofessor.json")

        self.bl = parse_beuthlex(dir / "beuthlex.json")
        self.hb = parse_hb(dir / "hb.json")

        self.lexicon = recursive_compose([self.bl, self.hb])
        # self.lexicon.remove_node("Lexikon")
        self.lexicon.graph["name"] = "lexikon"

        self.all = [self.lexicon,
                    self.bp,
                    self.hoai,
                    self.din,
                    self.vob,  ]

        self.graph = recursive_compose(self.all)

    def compare_parts(self):
        """
        Compare the single graphs pair wise
        :return:
        """
        for comb in itertools.combinations(self.all, 2):
            compare_two_graphs(*comb)

    def to_gexf(self, file="bauprofesser.gexf"):
        """
        Write to GEXF format
        :param file:
        :return:
        """
        nx.write_gexf(self.graph, file)

    def to_gml(self, file="bauprofesser.gml"):
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

    def add_keyword_in_text(self, check=["text", "title", "paragraph", "honorar"]):
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
    parser.add_argument('--output', dest='output', default="Baugraph.gml",
                        help='Where to save the file.')
    parser.add_argument('--input', dest='input', default="output/",
                        help='The result file of the crawling process')

    args = parser.parse_args()

    b = BauGraph(args.input)
    b.add_keyword_in_text(check=["text", "paragraph", "honorar", "title"])
    b.stats()
    b.add_clustering()
    b.add_pagerank()

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
# bg = BauGraph("output/")
# bg.add_keyword_in_text()
# bg.graph