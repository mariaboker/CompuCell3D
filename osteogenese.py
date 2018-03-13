
import sys
from os import environ
from os import getcwd
import string

sys.path.append(environ["PYTHON_MODULE_PATH"])


import CompuCellSetup


sim,simthread = CompuCellSetup.getCoreSimulationObjects()
            
CompuCellSetup.initializeSimulationObjects(sim,simthread)

steppableRegistry=CompuCellSetup.getSteppableRegistry()
        

from osteogeneseSteppables import ConstraintInitializerSteppable
ConstraintInitializerSteppableInstance=ConstraintInitializerSteppable(sim,_frequency=10)
steppableRegistry.registerSteppable(ConstraintInitializerSteppableInstance)
        
from osteogeneseSteppables import Differentiation1Steppable
Differentiation1SteppableInstance=Differentiation1Steppable(sim,_frequency=5)
steppableRegistry.registerSteppable(Differentiation1SteppableInstance)

from osteogeneseSteppables import DeadSteppable
DeadSteppableInstance=DeadSteppable(sim,_frequency=30)
steppableRegistry.registerSteppable(DeadSteppableInstance)

        
CompuCellSetup.mainLoop(sim,simthread,steppableRegistry)
        
        