import numpy as np

class CShapeGenerator():

    def __init__(self, fSpherePercent: float, fDiameter: float, iNumberOfSegments: int = 5, fHoleDiameter: float = 0.0):
        self.fSpherePercent = np.clip(fSpherePercent, 0.05, 0.95)
        self.fCanopyDiameter = np.clip(fDiameter, 0.0, None)

        self.iNumberOfSegments = np.clip(iNumberOfSegments, 5, None)
        
        self.fSphereRadius = self.fCanopyDiameter/(2.0 * np.sin(self.fSpherePercent*np.pi))

        self.fHoleDiameter = np.clip(fHoleDiameter, 0.0, self.fCanopyDiameter)
        self.fHolePercent = np.arcsin(self.fHoleDiameter/(2.0*self.fSphereRadius))/np.pi if self.fHoleDiameter > 0.0 else 0.0
    
    def getSegmentShape(self, iNPoints: int = 10):

        aY = np.linspace(self.fHolePercent, self.fSpherePercent, iNPoints)

        aDiameters = 2.0*np.sin(aY*np.pi)*self.fSphereRadius
        aArcLenghtsX = aDiameters*np.pi/self.iNumberOfSegments
        aArcLenghtsY = np.pi*self.fSphereRadius*aY

        aContour = np.zeros((len(aArcLenghtsX),2))
        aContour[:,0], aContour[:,1] = aArcLenghtsX/2, aArcLenghtsY
        aContourMir = aContour.copy()
        aContourMir[:,0] = -aContour[:,0]

        return np.concatenate((aContour, np.flip(aContourMir,axis=0), [aContour[0]]))