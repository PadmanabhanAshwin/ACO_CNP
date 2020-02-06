#%%
#This is not self sufficient code: This just imports the file instances. 
#I recommend running this file before and then natively use the graph instances. 

import networkx as nx
BA500 = nx.read_adjlist("instancs/BarabasiAlbert_n500m1.txt", nodetype = int)
BA1000 = nx.read_adjlist("instancs/BarabasiAlbert_n1000m1.txt", nodetype=int)
BA2500 = nx.read_adjlist("instancs/BarabasiAlbert_n2500m1.txt", nodetype = int)
BA5000 = nx.read_adjlist("instancs/BarabasiAlbert_n5000m1.txt", nodetype = int)

ER250 = nx.read_adjlist("instancs/ErdosRenyi_n250.txt", nodetype=int)
ER500 = nx.read_adjlist("instancs/ErdosRenyi_n500.txt", nodetype = int)
ER1000 = nx.read_adjlist("instancs/ErdosRenyi_n1000.txt", nodetype = int)
ER2500 = nx.read_adjlist("instancs/ErdosRenyi_n2500.txt", nodetype = int)

FF250 = nx.read_adjlist("instancs/ForestFire_n250.txt", nodetype=int)
FF500 = nx.read_adjlist("instancs/ForestFire_n500.txt", nodetype = int)
#FF1000 =  nx.read_adjlist("instancs/ForestFire_n1000.txt", nodetype = int)
FF2000 = nx.read_adjlist("instancs/ForestFire_n2000.txt", nodetype = int)

WS250 = nx.read_adjlist("instancs/WattsStrogatz_n250.txt", nodetype=int)
WS500 = nx.read_adjlist("instancs/WattsStrogatz_n500.txt", nodetype = int)
WS1000 = nx.read_adjlist("instancs/WattsStrogatz_n1000.txt", nodetype = int)
WS1500 = nx.read_adjlist("instancs/WattsStrogatz_n1500.txt", nodetype = int)
#%%
