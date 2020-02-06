#%%Flow rate experiment: 
""" def getnumberoffuturenodes(flowG, node, traversecheck):
        neigh = flowG.neighbors(node)
        numnodes = 0 
        for i in neigh: 
                if traversecheck[i] == True:
                        numnodes+=1
        return numnodes

flowG = copy.deepcopy(Gorg)
nx.draw(flowG, with_labels = True)
resdict = {i: 0 for i in flowG.nodes()}
for o in range(100):
        for root in flowG.nodes():
                #updates to flowmat is reflected in the graph node attributes. 
                #flowmat = [#nodes, 1] of flowrates in each node. 
                nodeflowmat = {i : 0 for i in flowG.nodes()}
                nx.set_edge_attributes(flowG, None, 'edgeflow')
                traverse = []

                #dict{node#; Needs to enter? }
                traversecheck = {i : True for i in flowG.nodes()}

                #root = 0
                inflow = 100
                traversecheck[root] = False
                nodeflowmat[root] = inflow
                traverse.append(root)
                nx.set_node_attributes(flowG, nodeflowmat, 'flowrate')
                #print("Inflow at node", root, "is= ", flowG.nodes[root]["flowrate"])

                #Get neighbours of roots: (rootneight is an iterator obj)
                rootneigh = flowG.neighbors(root)
                for i in rootneigh:
                        traverse.append(i)
                        numnodes = getnumberoffuturenodes(flowG, root, traversecheck)
                        nodeflowmat[i] = inflow/numnodes
                nx.set_node_attributes(flowG, nodeflowmat, 'flowrate')

                while len(traverse) < len(flowG.nodes()):
                        #print(traverse)
                        unexplorednodes = 0 
                        for i in traverse:
                                #print("Checking existence of unexplored")
                                unexplorednodes+= int(traversecheck[i])
                        if unexplorednodes == 0:
                                break
                        else: 
                                for i in traverse:
                                        if traversecheck[i]:
                                                #print("Root node is ", i)
                                                traversecheck[i] = False
                                                neigh = flowG.neighbors(i)
                                                neighlist = [] 
                                                for h in neigh:
                                                        neighlist.append(h)
                                                chooselist = []
                                                for u in range(100):
                                                        shuffle(neighlist)
                                                        chooselist.append(list(neighlist))
                                                myneighlist = chooselist[randrange(10)]
                                                numnodes = getnumberoffuturenodes(flowG, i, traversecheck)
                                                for j in list(myneighlist):
                                                        if traversecheck[j]:
                                                                if j not in traverse:
                                                                        traverse.append(j)
                                                                #print(traverse)
                                                                nodeflowmat[j] = nodeflowmat[j] + (flowG.nodes[i]["flowrate"]/numnodes)
                                                nx.set_node_attributes(flowG, nodeflowmat, 'flowrate')
                                        #print(i)
                                        #print("For root", root,"nodeflow is= ", nodeflowmat)
                                for p in nodeflowmat:
                                        resdict[p] = resdict[p] + nodeflowmat[p]
                                print("resdict is" , resdict)
                                print("nodeflow is", nodeflowmat)
 """