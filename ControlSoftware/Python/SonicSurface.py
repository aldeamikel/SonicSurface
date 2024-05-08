import serial
import serial.tools.list_ports
import numpy as np
from Waves import Waves
import time
import csv

class SonicSurface:
    PHASE_DIVS = 32
    N_EMMITERS = 256
    WAVELENGTH = 0.00865 #Air at 25C
    EMITTERS_POS = [-0.07874993,0,0.08074993,-0.057749946,0,0.08074993,-0.047249947,0,0.08074993,-0.06824995,0,0.070249945,-0.07874993,0,0.070249915,-0.047249954,0,0.07024993,-0.057749953,0,0.07024993,-0.06824992,0,0.08074993,-0.07874993,0,0.05974994,-0.057749946,0,0.059749942,-0.047249947,0,0.059749942,-0.06824993,0,0.04924994,-0.07874993,0,0.04924994,-0.047249947,0,0.049249943,-0.057749946,0,0.049249943,-0.06824993,0,0.05974994,-0.07874993,0,0.03874995,-0.057749946,0,0.038749944,-0.047249947,0,0.038749944,-0.06824993,0,0.028249947,-0.07874993,0,0.028249947,-0.047249954,0,0.028249951,-0.057749953,0,0.028249951,-0.06824993,0,0.03874994,-0.07874993,0,0.017749948,-0.057749953,0,0.017749952,-0.047249954,0,0.017749952,-0.068249926,0,0.0072499607,-0.07874993,0,0.007249957,-0.04724995,0,0.007249959,-0.05774995,0,0.007249959,-0.06824993,0,0.017749948,-0.07874993,0,-0.0032500343,-0.05774995,0,-0.0032500399,-0.04724995,0,-0.0032500362,-0.06824993,0,-0.013750033,-0.07874993,0,-0.013750033,-0.04724995,0,-0.013750035,-0.05774995,0,-0.013750035,-0.06824993,0,-0.0032500343,-0.07874993,0,-0.024250032,-0.05774995,0,-0.024250034,-0.04724995,0,-0.024250034,-0.06824993,0,-0.03475002,-0.07874994,0,-0.034750026,-0.047249954,0,-0.03475003,-0.057749953,0,-0.03475003,-0.06824993,0,-0.024250032,-0.07874993,0,-0.045250025,-0.057749953,0,-0.04525003,-0.047249947,0,-0.04525002,-0.06824993,0,-0.055750016,-0.07874993,0,-0.055750024,-0.047249947,0,-0.05575002,-0.057749953,0,-0.055750027,-0.06824993,0,-0.045250017,-0.078749925,0,-0.06624998,-0.05774995,0,-0.06624999,-0.04724995,0,-0.06624999,-0.06824994,0,-0.076749995,-0.07874994,0,-0.07674998,-0.04724995,0,-0.07674999,-0.05774995,0,-0.07674999,-0.068249926,0,-0.06625,-0.03674995,0,0.08074994,-0.015749965,0,0.08074993,-0.005249969,0,0.08074993,-0.026249964,0,0.07024993,-0.03674996,0,0.07024994,-0.005249969,0,0.07024993,-0.015749965,0,0.07024993,-0.026249964,0,0.08074993,-0.03674995,0,0.05974994,-0.015749961,0,0.059749935,-0.0052499655,0,0.05974994,-0.02624996,0,0.04924994,-0.036749955,0,0.04924994,-0.0052499655,0,0.04924994,-0.015749961,0,0.04924994,-0.02624996,0,0.059749935,-0.036749955,0,0.038749944,-0.01574996,0,0.03874995,-0.0052499655,0,0.038749944,-0.026249964,0,0.028249947,-0.036749955,0,0.028249947,-0.0052499664,0,0.02824995,-0.015749965,0,0.028249947,-0.026249958,0,0.03874995,-0.036749955,0,0.017749948,-0.015749965,0,0.017749948,-0.0052499664,0,0.01774995,-0.026249962,0,0.007249958,-0.036749955,0,0.007249959,-0.0052499673,0,0.007249957,-0.015749963,0,0.007249958,-0.026249964,0,0.017749948,-0.036749955,0,-0.003250037,-0.015749961,0,-0.003250038,-0.005249968,0,-0.003250038,-0.026249958,0,-0.013750037,-0.036749955,0,-0.013750033,-0.005249967,0,-0.013750033,-0.01574996,0,-0.013750037,-0.02624996,0,-0.003250038,-0.036749955,0,-0.024250032,-0.01574996,0,-0.024250036,-0.0052499673,0,-0.024250032,-0.02624996,0,-0.034750026,-0.036749955,0,-0.034750026,-0.0052499673,0,-0.034750026,-0.015749961,0,-0.034750026,-0.026249958,0,-0.024250036,-0.036749955,0,-0.04525003,-0.015749963,0,-0.04525002,-0.0052499655,0,-0.04525002,-0.026249964,0,-0.05575002,-0.036749955,0,-0.055750027,-0.0052499655,0,-0.05575002,-0.015749965,0,-0.05575002,-0.026249962,0,-0.04525002,-0.03674995,0,-0.06624999,-0.015749963,0,-0.06624999,-0.005249969,0,-0.06624999,-0.026249962,0,-0.07674999,-0.03674996,0,-0.07674999,-0.005249969,0,-0.07674999,-0.015749963,0,-0.07674999,-0.026249962,0,-0.06624999,0.0052500297,0,0.08074993,0.026250018,0,0.08074993,0.036750015,0,0.08074993,0.015750019,0,0.07024993,0.0052500297,0,0.07024993,0.036750015,0,0.07024993,0.026250018,0,0.07024993,0.015750019,0,0.08074993,0.0052500297,0,0.05974994,0.026250016,0,0.059749935,0.036750015,0,0.05974994,0.015750017,0,0.049249936,0.0052500297,0,0.04924994,0.036750015,0,0.04924994,0.026250016,0,0.049249936,0.015750017,0,0.059749935,0.005250028,0,0.038749944,0.02625002,0,0.038749944,0.036750015,0,0.038749944,0.01575002,0,0.028249951,0.005250028,0,0.028249947,0.036750015,0,0.028249951,0.02625002,0,0.028249951,0.01575002,0,0.038749944,0.0052500293,0,0.017749952,0.02625002,0,0.017749952,0.036750015,0,0.017749952,0.01575002,0,0.007249958,0.0052500293,0,0.007249957,0.036750015,0,0.007249959,0.02625002,0,0.007249958,0.01575002,0,0.017749952,0.005250029,0,-0.003250037,0.02625002,0,-0.003250038,0.036750015,0,-0.003250038,0.01575002,0,-0.013750033,0.005250028,0,-0.013750033,0.036750015,0,-0.013750037,0.02625002,0,-0.013750033,0.01575002,0,-0.003250038,0.005250028,0,-0.024250032,0.02625002,0,-0.024250034,0.036750015,0,-0.024250036,0.015750019,0,-0.034750022,0.0052500297,0,-0.034750026,0.036750015,0,-0.034750026,0.026250018,0,-0.034750022,0.01575002,0,-0.024250034,0.0052500297,0,-0.04525002,0.026250018,0,-0.04525002,0.036750015,0,-0.045250017,0.015750019,0,-0.05575002,0.0052500297,0,-0.05575002,0.03675001,0,-0.05575002,0.026250018,0,-0.05575002,0.015750019,0,-0.04525002,0.0052500297,0,-0.06624999,0.02625002,0,-0.06624999,0.03675002,0,-0.06624998,0.01575002,0,-0.07674999,0.0052500297,0,-0.07674999,0.03675001,0,-0.07674998,0.02625002,0,-0.07674999,0.01575002,0,-0.06624999,0.047250018,0,0.08074993,0.068249986,0,0.08074993,0.078749985,0,0.08074993,0.05775,0,0.07024994,0.04725001,0,0.07024992,0.078749985,0,0.07024993,0.068249986,0,0.07024993,0.05775001,0,0.08074993,0.047250006,0,0.059749946,0.068249986,0,0.05974994,0.078749985,0,0.059749946,0.057750013,0,0.049249936,0.04725001,0,0.04924994,0.078749985,0,0.049249947,0.068249986,0,0.04924994,0.05775001,0,0.05974994,0.047250006,0,0.03874995,0.068249986,0,0.03874994,0.078749985,0,0.03874995,0.057750005,0,0.028249947,0.047250006,0,0.028249947,0.078749985,0,0.028249947,0.068249986,0,0.028249947,0.057750005,0,0.038749937,0.047250006,0,0.017749948,0.068249986,0,0.017749948,0.078749985,0,0.017749948,0.05775001,0,0.007249957,0.04725001,0,0.007249959,0.078749985,0,0.0072499607,0.068249986,0,0.007249955,0.057750005,0,0.017749948,0.04725001,0,-0.0032500362,0.068249986,0,-0.003250038,0.078749985,0,-0.003250038,0.057750005,0,-0.013750033,0.047250006,0,-0.013750033,0.078749985,0,-0.013750037,0.068249986,0,-0.013750037,0.05775001,0,-0.0032500362,0.047250006,0,-0.024250032,0.068249986,0,-0.024250036,0.078749985,0,-0.024250036,0.057750005,0,-0.034750022,0.047250006,0,-0.03475003,0.078749985,0,-0.034750026,0.068249986,0,-0.034750026,0.057750005,0,-0.024250032,0.047250014,0,-0.045250017,0.068249986,0,-0.045250017,0.078749985,0,-0.045250025,0.057750013,0,-0.055750016,0.047250014,0,-0.055750016,0.078749985,0,-0.055750024,0.068249986,0,-0.055750016,0.057750013,0,-0.045250017,0.047250018,0,-0.06625,0.06824999,0,-0.06625,0.07874999,0,-0.06624998,0.05775001,0,-0.07674999,0.04725001,0,-0.07674999,0.07874998,0,-0.07674998,0.06824998,0,-0.076749995,0.057750016,0,-0.06624998]
    
    def __init__(self):
        self.serialConn = None
        emittersPos = np.array( self.EMITTERS_POS ).reshape(self.N_EMMITERS, 3)
        rounding=np.around(emittersPos,decimals=5) # some positions were off by distances smaller than nanometers. This caused a big problem when sorting them.
        self.orderArray=[0, 7, 1, 2, 64, 71, 65, 66, 128, 135, 129, 130, 192, 199, 193, 194, 4, 3, 6, 5, 68, 67, 70, 69, 132, 131, 134, 133, 196, 195, 198, 197, 8, 15, 9, 10, 72, 79, 73, 74, 136, 143, 137, 138, 200, 207, 201, 202, 12, 11, 14, 13, 76, 75, 78, 77, 140, 139, 142, 141, 204, 203, 206, 205, 16, 23, 17, 18, 80, 87, 81, 82, 144, 151, 145, 146, 208, 215, 209, 210, 20, 19, 22, 21, 84, 83, 86, 85, 148, 147, 150, 149, 212, 211, 214, 213, 24, 31, 25, 26, 88, 95, 89, 90, 152, 159, 153, 154, 216, 223, 217, 218, 28, 27, 30, 29, 92, 91, 94, 93, 156, 155, 158, 157, 220, 219, 222, 221, 32, 39, 33, 34, 96, 103, 97, 98, 160, 167, 161, 162, 224, 231, 225, 226, 36, 35, 38, 37, 100, 99, 102, 101, 164, 163, 166, 165, 228, 227, 230, 229, 40, 47, 41, 42, 104, 111, 105, 106, 168, 175, 169, 170, 232, 239, 233, 234, 44, 43, 46, 45, 108, 107, 110, 109, 172, 171, 174, 173, 236, 235, 238, 237, 48, 55, 49, 50, 112, 119, 113, 114, 176, 183, 177, 178, 240, 247, 241, 242, 52, 51, 54, 53, 116, 115, 118, 117, 180, 179, 182, 181, 244, 243, 246, 245, 56, 63, 57, 58, 120, 127, 121, 122, 184, 191, 185, 186, 248, 255, 249, 250, 60, 59, 62, 61, 124, 123, 126, 125, 188, 187, 190, 189, 252, 251, 254, 253]
        self.emittersPos=rounding
        self.phaseOffsets = np.zeros( [self.N_EMMITERS] )
        self.phases = np.zeros( [1,self.N_EMMITERS], dtype=np.complex128 )
   
    @staticmethod
    def listSerial():
        ports = serial.tools.list_ports.comports()
        print("Serial Ports:")
        for i, port in enumerate(ports, start=1):
            print(f"{i}: {port.device}")
            
    def disconnect(self):
        if self.serialConn != None:
            self.serialConn.close()
            self.serialConn = None
    
    def connect(self, indexPort):
        if indexPort == -1:
            self.listSerial()
            indexPort = int(input("Enter index of serial port: "))
        selectedPort = serial.tools.list_ports.comports()[indexPort - 1]
        self.disconnect()
        self.serialConn = serial.Serial(selectedPort.name, baudrate=230400)
    
    #phases range from 0 to 2pi
    #we can use this function to directly send the phases from ArrayAmp
    def sendPhases(self, phases):
        assert( phases.shape == (self.N_EMMITERS,) )
        phasesDisc = (phases % (2*np.pi)) * self.PHASE_DIVS / 2 / np.pi
        
        #phasesDisc += self.phaseOffsets
        #phasesDisc %= self.PHASE_DIVS
        dataToSend = bytes( phasesDisc.astype(np.uint8))
        
        self.serialConn.write( bytes([254]) ) #start phases
        self.serialConn.write(dataToSend)
        self.serialConn.write( bytes([253]) ) #commit
        
    def switchOnOrOff(self, on):
        if on:
            dataToSend = bytes([0 for i in range(self.N_EMMITERS)])
        else:
            dataToSend = bytes([self.PHASE_DIVS for i in range(self.N_EMMITERS)])    
        self.serialConn.write( bytes([254]) ) #start phases
        self.serialConn.write(dataToSend)
        self.serialConn.write( bytes([253]) ) #commit
        
    def focusAtPos(self, x,y,z):
        self.focusAt(np.array([x,y,z]))
        
    def focusAt(self, pos):
        distances = np.linalg.norm(self.emittersPos - pos, axis=1)
        lambdas = distances / self.WAVELENGTH
        frags = np.ceil(lambdas) - lambdas
        
        self.sendPhases( 2.0 * np.pi * frags )
        
    def multiFocusIBP(self, points, iters=20, resetPhases=False):
        propagators = Waves.calcPropagatorsPistonsToPoints(self.emittersPos, np.array([0,1,0]), points, self.WAVELENGTH*np.pi*2, 0.009)
        backprops = np.conjugate( propagators )
        if resetPhases:
            self.phases *= 0
        for _ in range(iters):
            fieldAtPoints = self.phases * propagators #propagate emitters -> points
            fieldAtPoints /= np.abs( fieldAtPoints ) #normalize points
            self.phases = backprops * fieldAtPoints #backprop points <- emitters
            self.phases /= np.abs( self.phases ) #normalize emitters
        self.sendPhases( np.angle(self.phases) + np.pi )
        
    def multiFocusChecker(self, positions):
        nPoints = positions.shape[0]
        nEmitters = self.emittersPos.shape[0]
        phases = np.zeros( [nEmitters] )
        for i in range(nEmitters):
            dist = np.linalg.norm(self.emittersPos[i,:] - positions[i % nPoints ,:])
            lambdas = dist / self.WAVELENGTH
            frags = np.ceil(lambdas) - lambdas
            phases[i] = frags * 2.0 * np.pi
        self.sendPhases( phases )
        
  
try:  
    if __name__ == "__main__":
    
        array = SonicSurface()
        # array.connect( -1 )
       
        # for _ in range(3):
        #     array.switchOnOrOff( True )
        #     time.sleep(1)
        #     array.switchOnOrOff( False )
        #     time.sleep(1)
        
        
        
        
        # listSwitchOn = [array.PHASE_DIVS for i in range(array.N_EMMITERS)]
        # # Lets switch on 16 in the middle
        # for i in range(6,10):
        #     for j in range(6,10):
        #         listSwitchOn[array.orderArray[16 * i + j]] = 0
        
        # listSwitchOn = [array.PHASE_DIVS for i in range(array.N_EMMITERS)]
        # # 4 focal points
        # for i in range(2,5):
        #     for j in range(2, 5):
        #         listSwitchOn[array.orderArray[16 * i + j]] = 0
        #     for j in range(11, 14):
        #         listSwitchOn[array.orderArray[16 * i + j]] = 0
        # for i in range(11,14):
        #     for j in range(2, 5):
        #         listSwitchOn[array.orderArray[16 * i + j]] = 0
        #     for j in range(11, 14):
        #         listSwitchOn[array.orderArray[16 * i + j]] = 0
                
        # # Switch one by one to check which ones are broken
        # inp = " "
        # num = -1
        # while inp != "end":
        #     inp = input("")
        #     if inp == "":
        #         num += 1
        #     elif inp == "a":
        #         num -= 1
                
        #     listSwitchOn = [array.PHASE_DIVS for i in range(array.N_EMMITERS)]
        #     listSwitchOn[array.orderArray[num]] = 0
            
        #     dataToSend = bytes(listSwitchOn)    
        #     array.serialConn.write( bytes([254]) ) #start phases
        #     array.serialConn.write(dataToSend)
        #     array.serialConn.write( bytes([253]) ) #commit
        #     time.sleep(1)
                
            
        # Switch one just the first one    
        # listSwitchOn = [0 for i in range(array.N_EMMITERS)]
        # listSwitchOn[array.orderArray[0]] = 0
            
        # 4x4 
        # listSwitchOn = [array.PHASE_DIVS for i in range(array.N_EMMITERS)]
        # for i in range(0,16,5):
        #     for j in range(0,16,5):
        #         listSwitchOn[array.orderArray[16 * i + j]] = 0
                
        # dataToSend = bytes(listSwitchOn)    
        # array.serialConn.write( bytes([254]) ) #start phases
        # array.serialConn.write(dataToSend)
        # array.serialConn.write( bytes([253]) ) #commit
        
        with open("phasesEmitters  20240227-1459PM53413863.csv", newline='') as csvfile:
            data = list(csv.reader(csvfile))
            patternPhases= np.array(data[0]).astype(float)  
        
        # 16x16 pattern
        reorderedPatternPhases = np.zeros(array.N_EMMITERS)
        for i in range(len(patternPhases)):
            reorderedPatternPhases[array.orderArray[i]] = patternPhases[i]
        reorderedPatternPhases = np.array(reorderedPatternPhases)
        
        save = True
        
        if save:
            np.savetxt("reorderedPatternPhases.csv", reorderedPatternPhases, delimiter = ',')
            
        # # 4x4 pattern
        # reorderedPatternPhases = np.zeros(array.N_EMMITERS)
        # pos = 0
        # for i in range(0,16,5):
        #     for j in range(0,16,5):
        #         reorderedPatternPhases[array.orderArray[16 * i + j]] = patternPhases[pos]
        #         pos += 1
        # reorderedPatternPhases = np.array(reorderedPatternPhases)
        
        # array.sendPhases(reorderedPatternPhases)
        time.sleep(1)
        
        array.disconnect()
        
except KeyboardInterrupt:
    array.disconnect()
    pass
