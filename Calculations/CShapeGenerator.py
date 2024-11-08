import numpy as np

class CShapeGenerator():

    def __init__(self, fSpherePercent: float, fDiameter: float, iNumberOfSegments: int = 5, fHoleDiameter: float = 0.0):
        self.fSpherePercent = np.clip(fSpherePercent, 0.05, 0.95)
        self.fCanopyDiameter = np.clip(fDiameter, 0.0, None)
        self.iNumberOfSegments = np.clip(iNumberOfSegments, 5, None)
        self.fHoleDiameter = np.clip(fHoleDiameter, 0.0, self.fCanopyDiameter)
        
        self.fSphereRadius = self.fCanopyDiameter/(4.0*(self.fSpherePercent-self.fSpherePercent**2)**.5)

        # Spherical coordinates
        # Theta
        self.fThetaStart = np.arcsin(self.fHoleDiameter/(2.0*self.fSphereRadius)) if self.fHoleDiameter > 0.0 else 0.0
        self.fThetaEnd = np.arcsin(self.fCanopyDiameter/(2.0*self.fSphereRadius)) if self.fCanopyDiameter > 0.0 else 0.0
        if self.fSpherePercent > 0.50: self.fThetaEnd = np.pi-self.fThetaEnd 

        # Phi
        self.fPhiStart = 0.0
        self.fPhiEnd = 2.0*np.pi/self.iNumberOfSegments
    
    def getSegmentShape(self, iNPoints: int = 10):
        aTheta = np.concatenate((
            np.linspace(self.fThetaStart, self.fThetaEnd, iNPoints),
            [self.fThetaEnd],
            np.linspace(self.fThetaEnd, self.fThetaStart, iNPoints),
            [self.fThetaStart, self.fThetaStart]
        ))
        aPhi = np.concatenate((
            np.full(iNPoints, self.fPhiEnd/2),
            [0],
            np.full(iNPoints, -self.fPhiEnd/2),
            [0, self.fPhiEnd/2]
        ))

        aArcsHorizontal = (self.fSphereRadius*np.sin(aTheta))*aPhi
        aArcsVertical = (self.fSphereRadius*aTheta)

        aContour = np.stack((aArcsHorizontal, aArcsVertical), axis=-1)

        return aContour