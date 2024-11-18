import numpy as np

def create_closed_symmetrical_contour(aX: np.ndarray, aY: np.ndarray) -> np.ndarray:
    # Create 2D contour
    return np.concatenate((
        np.stack((aX, aY), axis=-1),
        np.stack((-np.flip(aX), np.flip(aY)), axis=-1),
        [[aX[0], aY[0]]]
    ))

class CSphericalGenerator():

    def __init__(self, fSpherePercent: float, fDiameter: float, iNumberOfSegments: int = 5, fHoleDiameter: float = 0.0, iNPoints: int = 100):
        
        self.fSpherePercent = np.clip(fSpherePercent, 0.05, 0.95)
        self.fCanopyDiameter = np.clip(fDiameter, 0.0, None)
        self.iNumberOfSegments = np.clip(iNumberOfSegments, 5, None)
        self.fHoleDiameter = np.clip(fHoleDiameter, 0.0, self.fCanopyDiameter)
        self.iNPoints = np.clip(iNPoints, 2, 250)
        
        if self.fSpherePercent < 0.50:
            self.fSphereRadius = self.fCanopyDiameter/(4.0*(self.fSpherePercent-self.fSpherePercent**2)**.5)
        else:
            # If sphere percent >= 0.50 then effective diameter is the same as in half-sphere
            self.fSphereRadius = self.fCanopyDiameter/2


        # Spherical coordinates
        # Theta
        self.fThetaStart = np.arcsin(self.fHoleDiameter/(2.0*self.fSphereRadius)) if self.fHoleDiameter > 0.0 else 0.0
        self.fThetaEnd = np.arccos(1-2.0*self.fSpherePercent)

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

        return create_closed_symmetrical_contour(aX, aY)
    
class CConicalGenerator():
    
    def __init__(self, fConeAngle: float, fDiameter: float, iNumberOfSegments: int = 5, fHoleDiameter: float = 0.0):
        
        self.fConeAngle = np.deg2rad(np.clip(fConeAngle, 0.0, 180.0))
        self.fCanopyDiameter = np.clip(fDiameter, 0.0, None)
        self.iNumberOfSegments = np.clip(iNumberOfSegments, 5, None)
        self.fHoleDiameter = np.clip(fHoleDiameter, 0.0, self.fCanopyDiameter)
        self.iNPoints = 2

        # Cylindrical coordinates
        # Height
        self.fHeightStart = self.fHoleDiameter/(2.0*np.tan(self.fConeAngle/2)) if self.fHoleDiameter > 0.0 else 0.0
        self.fHeightEnd = self.fCanopyDiameter/(2.0*np.tan(self.fConeAngle/2))

        # Phi
        self.fPhiStart = 0.0
        self.fPhiEnd = 2.0*np.pi/self.iNumberOfSegments

    def get3DRepresentation(self):

        aHeight = np.linspace(self.fHeightStart,self.fHeightEnd,self.iNPoints)
        aPhi = np.linspace(0,2.0*np.pi,self.iNumberOfSegments+1)

        u, v = np.meshgrid(aPhi, aHeight)

        aX = np.cos(u) * v * np.tan(self.fConeAngle/2)
        aY = np.sin(u) * v * np.tan(self.fConeAngle/2)
        aZ = self.fHeightEnd - v

        return aX, aY, aZ
    
    def get2DRepresentation(self):

        aHeight = np.linspace(self.fHeightStart,self.fHeightEnd,self.iNPoints)

        # Chords and segment height
        aChordsHorizontal = (np.tan(self.fConeAngle/2)*aHeight)*((1-np.cos(self.fPhiEnd))*2)**.5
        aHeightSegment = aHeight / np.cos(self.fConeAngle/2)

        # Calculate X and Y
        aX, aY = aChordsHorizontal/2, aHeightSegment

        return create_closed_symmetrical_contour(aX, aY)
    
class CDiskGenerator():
    
    def __init__(self, fDiameter: float, iNumberOfSegments: int = 5, fHoleDiameter: float = 0.0):
        
        self.fCanopyDiameter = np.clip(fDiameter, 0.0, None)
        self.iNumberOfSegments = np.clip(iNumberOfSegments, 5, None)
        self.fHoleDiameter = np.clip(fHoleDiameter, 0.0, self.fCanopyDiameter)
        self.iNPoints = 2

        # Polar coordinates
        # Radius
        self.fRadiusStart = self.fHoleDiameter/2 if self.fHoleDiameter > 0.0 else 0.0
        self.fRadiusEnd = self.fCanopyDiameter/2

        # Phi
        self.fPhiStart = 0.0
        self.fPhiEnd = 2.0*np.pi/self.iNumberOfSegments

    def get3DRepresentation(self):

        aRadius = np.linspace(self.fRadiusStart,self.fRadiusEnd,self.iNPoints)
        aPhi = np.linspace(0,2.0*np.pi,self.iNumberOfSegments+1)

        u, v = np.meshgrid(aPhi, aRadius)

        aX = np.cos(u) * v
        aY = np.sin(u) * v
        aZ = np.zeros_like(u)

        return aX, aY, aZ
    
    def get2DRepresentation(self):

        aRadius = np.linspace(self.fRadiusStart,self.fRadiusEnd,self.iNPoints)

        # Chords and segment height
        aChords = aRadius*((1-np.cos(self.fPhiEnd))*2)**.5
        aHeights = aRadius * np.cos(self.fPhiEnd/2)

        # Calculate X and Y
        aX, aY = aChords/2, aHeights

        return create_closed_symmetrical_contour(aX, aY)