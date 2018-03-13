from PySteppables import *
import CompuCell
import sys
            
            
# definicao no inicio da simulacao do volume das celulas
class ConstraintInitializerSteppable(SteppableBasePy):
    def __init__(self,_simulator,_frequency=10):
        SteppableBasePy.__init__(self,_simulator,_frequency)
    def start(self):
        for cell in self.cellList:
            cell.targetVolume=900                             
            cell.lambdaVolume=200.0
           

# Processos de diferenciacao desencadeados pela concentracao do Campo de RUNX 2
class Differentiation1Steppable(SteppableBasePy):
     def __init__(self,_simulator,_frequency=5):
         SteppableBasePy.__init__(self,_simulator,_frequency)
        
     def step(self,mcs):   
       
        ########### Calculos referentes ao campo RUNX2 ###########

        self.scalarField1=self.getConcentrationField('RUNX2')
        field1=CompuCell.getConcentrationField(self.simulator,"RUNX2")
        pt1=CompuCell.Point3D()
            
        for cell in self.cellList:
            pt1.x=int(cell.xCOM)
            pt1.y=int(cell.yCOM)
            pt1.z=int(cell.zCOM)
            concentrationAtCOM1=field1.get(pt1)
            
            if cell.type == 1:
                # primeira diferenciacao -> aumento gradual de volume de metade das celulas que tem contato com concentracao x de RUNX 2
                if (cell.id % 2 == 0) and (mcs > 50) and (mcs < 650):
                    cell.targetVolume = cell.targetVolume + 5
                   
                # segunda diferenciacao -> muda o tipo celular de algumas celulas com concentracao y de RUNX 2
                if ((concentrationAtCOM1 >= 7) and (cell.id % 5 == 0)):
                    cell.type = 2
                    
                if ((concentrationAtCOM1 >= 7.3) and (cell.id % 3 == 0)):
                    cell.type = 2
                    
                if ((concentrationAtCOM1 >= 7.8) and (cell.id % 2 == 0)):
                    cell.type = 2
                    
                if (concentrationAtCOM1 > 8):
                    cell.type = 2
                        

        ########### Calculos referentes ao campo Phosphatase Alkaline ########### 
            
        self.scalarField2=self.getConcentrationField('PhosphAlka')
        field2=CompuCell.getConcentrationField(self.simulator,"PhosphAlka")
        pt2=CompuCell.Point3D()    

        for cell in self.cellList:
            pt2.x=int(cell.xCOM)
            pt2.y=int(cell.yCOM)
            pt2.z=int(cell.zCOM)
            concentrationAtCOM2=field2.get(pt2)

            if cell.type == 2:
                # Concentracao de Fosfatase Alcalina induz diferenciacao para tipo 3
                if ((concentrationAtCOM2 >= 5) and (cell.id % 3 == 0)):
                  cell.type = 3
                  
                if ((concentrationAtCOM2 >= 6) and (cell.id % 2 == 0)):
                  cell.type = 3
                
                if (concentrationAtCOM2 >= 7):
                  cell.type = 3


        ########### Calculos referentes ao campo Osteocalcin ########### 
        
        self.scalarField3=self.getConcentrationField('Osteocalcin')
        field3=CompuCell.getConcentrationField(self.simulator,"Osteocalcin")
        pt3=CompuCell.Point3D()
          
        for cell in self.cellList:
            pt3.x=int(cell.xCOM)
            pt3.y=int(cell.yCOM)
            pt3.z=int(cell.zCOM)
            concentrationAtCOM3=field3.get(pt3)

            if cell.type == 3:
                if ((concentrationAtCOM3 >= 6) and (cell.id % 7 == 0)):
                    cell.type = 4
                    
                if ((concentrationAtCOM3 >= 6.5) and (cell.id % 5 == 0)):
                    cell.type = 4
                    
                if ((concentrationAtCOM3 >= 7) and (cell.id % 3 == 0)):
                    cell.type = 4
            
                if ((concentrationAtCOM3 >= 9) and (cell.id % 2 == 0)):
                    cell.type = 4



# Morte das celulas apos formacao e estabilizacao da matriz
class DeadSteppable(SteppableBasePy):
     def __init__(self,_simulator,_frequency=30):
         SteppableBasePy.__init__(self,_simulator,_frequency)
        
     def step(self,mcs):  
        matriz = 0
        for cell in self.cellList:
            if cell.type == 4:
                matriz = matriz + 1 
        
        if matriz >= (len(self.cellList)*0.4):
            for cell in self.cellList:
                if cell.id % 5 == 0 and cell.type != 4:
                    self.deleteCell(cell)
                    
        if matriz >= (len(self.cellList)*0.45):
            for cell in self.cellList:
                if cell.id % 3 == 0 and cell.type != 4:
                    self.deleteCell(cell)
            
        if matriz >= (len(self.cellList)*0.5):
            for cell in self.cellList:
                if cell.id % 2 == 0 and cell.type != 4:
                    self.deleteCell(cell)
                        
        if matriz >= (len(self.cellList)*0.60):   
            for cell in self.cellList:
                if cell.type != 4:
                    self.deleteCell(cell)






