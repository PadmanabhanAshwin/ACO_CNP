
#=============DO NOT RUN ===========================================
# ======================================================================================
#======================================================================================
#%% Read pickle data
with open('BAinstances.pkl', 'rb') as f:
        a = pickle.load(f)
#%%
print("FF250 instance METHOD 1")
instances = [instance.FF250, instance.FF500, instance.FF2000]
instanceres = []
for q in instances:
        datares = func.getstatistics(q, 1, repnum = 10)
        instanceres.append(datares)
import pickle
with open('FFinstances.pkl', 'wb') as f:
        pickle.dump(instanceres, f)

print("WS instance METHOD 1")
instances = [instance.WS250, instance.WS500, instance.WS1000, instance.WS1500 ]
instanceres = []
for q in instances:
        datares = func.getstatistics(q, 1, repnum = 10)
        instanceres.append(datares)

import pickle
with open('WSinstances.pkl', 'wb') as f:
        pickle.dump(instanceres, f)
#================ METHOD 2 =========================
#=========================BA METHOD 2=========================
print("BA instance Method 2")
instances = [instance.BA500, instance.BA1000, instance.BA2500, instance.BA5000]
#instances = [instance.BA500, instance.BA1000]
#instances = [instance.BA500]
instanceres = []
for q in instances:
        datares = func.getstatistics(q, 1, repnum = 10)
        instanceres.append(datares)

import pickle
with open('BAinstancesMethod2.pkl', 'wb') as f:
        pickle.dump(instanceres, f)
#=================== FF Method 2=========================

print("FF instance method 2")
instances = [instance.FF250, instance.FF500, instance.FF2000]
instanceres = []
for q in instances:
        datares = func.getstatistics(q, 2, repnum = 10)
        instanceres.append(datares)
import pickle
with open('FFinstancesMethod2.pkl', 'wb') as f:
        pickle.dump(instanceres, f)

#=================== WS Method 2=========================

print("WS instance method 2")
instances = [instance.WS250, instance.WS500, instance.WS1000, instance.WS1500 ]
instanceres = []
for q in instances:
        datares = func.getstatistics(q, 2, repnum = 10)
        instanceres.append(datares)
import pickle
with open('WSinstancesMethod2.pkl', 'wb') as f:
        pickle.dump(instanceres, f)