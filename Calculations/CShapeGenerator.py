import numpy as np

class CShapeGenerator():

    def __init__(self, fSpherePercent: float, fDiameter: float, iNumberOfSegments: int = 5, fHoleDiameter: float = 0.0, iNPoints: int = 100):
        self.fSpherePercent = np.clip(fSpherePercent, 0.05, 0.95)
        self.fCanopyDiameter = np.clip(fDiameter, 0.0, None)
        self.iNumberOfSegments = np.clip(iNumberOfSegments, 5, None)
        self.fHoleDiameter = np.clip(fHoleDiameter, 0.0, self.fCanopyDiameter)
        self.iNPoints = np.clip(iNPoints, 1, 250)
        
        self.fSphereRadius = self.fCanopyDiameter/(4.0*(self.fSpherePercent-self.fSpherePercent**2)**.5)

        # Spherical coordinates
        # Theta
        self.fThetaStart = np.arcsin(self.fHoleDiameter/(2.0*self.fSphereRadius)) if self.fHoleDiameter > 0.0 else 0.0
        self.fThetaEnd = np.arcsin(self.fCanopyDiameter/(2.0*self.fSphereRadius)) if self.fCanopyDiameter > 0.0 else 0.0
        if self.fSpherePercent > 0.50: self.fThetaEnd = np.pi-self.fThetaEnd 

        # Phi
        self.fPhiStart = 0.0
        self.fPhiEnd = 2.0*np.pi/self.iNumberOfSegments

    def get3DRepresentation(self):

        aTheta = np.linspace(self.fThetaStart,self.fThetaEnd,self.iNPoints)
        aPhi = np.linspace(0,2.0*np.pi,self.iNumberOfSegments+1)

        u, v = np.meshgrid(aPhi, aTheta)

        aX = self.fSphereRadius * np.cos(u) * np.sin(v)
        aY = self.fSphereRadius * np.sin(u) * np.sin(v)
        aZ = self.fSphereRadius * np.cos(v)

        return aX, aY, aZ
    
    def get2DRepresentation(self):

        # Theta
        aTheta0 = np.linspace(0,self.fThetaStart,int(np.ceil(self.fThetaStart/(self.fThetaEnd-self.fThetaStart)*self.iNPoints))) if self.fThetaStart > 0.0 else np.array([])
        aTheta = np.linspace(self.fThetaStart,self.fThetaEnd,self.iNPoints)
        aTheta = np.concatenate((aTheta0, aTheta))
        iIndiceStart = len(aTheta0)
        del aTheta0

        # Arcs and chords
        aChordsHorizontal = (self.fSphereRadius*np.sin(aTheta))*((1-np.cos(self.fPhiEnd))*2)**.5
        aArcsVertical = (self.fSphereRadius*aTheta)

        # Calculate X and Y
        dX, dV = np.diff(aChordsHorizontal/2),np.diff(aArcsVertical)
        dY = (dV**2-dX**2)**.5

        aX, aY = np.concatenate(([0],dX)), np.concatenate(([0],dY))
        aX, aY = np.cumsum(aX), np.cumsum(aY)

        aX, aY = np.array(aX[iIndiceStart:]), np.array(aY[iIndiceStart:])

        # Create 2D contour
        aContour = np.concatenate((
            np.stack((aX, aY), axis=-1),
            np.stack((-np.flip(aX), np.flip(aY)), axis=-1),
            [[aX[0], aY[0]]]
        ))

        return aContour
    
    def getSegmentShape(self):
        aTheta = np.concatenate((
            np.linspace(self.fThetaStart, self.fThetaEnd, self.iNPoints),
            [self.fThetaEnd],
            np.linspace(self.fThetaEnd, self.fThetaStart, self.iNPoints),
            [self.fThetaStart, self.fThetaStart]
        ))
        aPhi = np.concatenate((
            np.full(self.iNPoints, self.fPhiEnd/2),
            [0],
            np.full(self.iNPoints, -self.fPhiEnd/2),
            [0, self.fPhiEnd/2]
        ))

        aArcsHorizontal = (self.fSphereRadius*np.sin(aTheta))*aPhi
        aArcsVertical = (self.fSphereRadius*aTheta)

        aContour = np.stack((aArcsHorizontal, aArcsVertical), axis=-1)

        return aContour