"""
Parachute class definition
"""

from calculations.ConstantParameters import *
import numpy as np
#import matplotlib.pyplot as plt
#import os, time

def getDiamaterFromVelocity(_TargetVelocity: np.ndarray | float, fMass: float, dcParameters: dict = INPUT_PARAMETERS):
    """
    Get required parachute area for given target velocity
    """
    return 2*np.sqrt((2*fMass*dcParameters["G_ACCELERATION"]/(dcParameters["AIR_DENSITY"]*_TargetVelocity**2*dcParameters["DRAG_COEFF"]))/np.pi)
    
def getVelocityFromDiameter(_Diameter: np.ndarray | float, fMass: float, dcParameters: dict = INPUT_PARAMETERS):
    """
    Get velocity for given parachute diameter
    """
    fArea = (_Diameter/2.0)**2*np.pi
    return np.sqrt(2*fMass*dcParameters["G_ACCELERATION"]/(dcParameters["AIR_DENSITY"]*fArea*dcParameters["DRAG_COEFF"]))

def calculateDiameterVelocityRelationship(
        fMass: float,
        tTargetVelocityRange: tuple | list = (5, 20),
        iSamples: int = 50,
        dcParameters: dict = INPUT_PARAMETERS
    ):
    aTargetVelocity = np.linspace(tTargetVelocityRange[0],tTargetVelocityRange[1],iSamples)
    aDiameters = getDiamaterFromVelocity(aTargetVelocity, fMass, dcParameters)
    return aTargetVelocity, aDiameters

class CParachute():

    def __init__(
            self,
            fMass: float,
            fCanopyDiameter: float,
            fOpenInitVelocity: float,
            dcParameters: dict = INPUT_PARAMETERS    
        ):
      
        # Constant parameters
        self.dcParameters = dcParameters
        # Mass
        self.fMass = fMass
        # Canopy parameters
        self.fCanopyDiameter = fCanopyDiameter
        self.fCanopyArea = (fCanopyDiameter/2.0)**2*np.pi
        # Velocity
        self.fOpenInitVelocity = fOpenInitVelocity
        # Drag
        self.fVehicleDragArea = self.dcParameters["DRAG_COEFF"]*self.fCanopyArea
        # Get inflation time
        # t_inf = n*D_0/(V_1**k)
        self.fInflationTime = self.dcParameters["INFLATION_CANOPY_FILL_CONST"]*self.fCanopyDiameter/(self.fOpenInitVelocity**self.dcParameters["DECCELERATION_EXPONENT"])
        
    def getBallisticParameter(self):
        """
        Ballistic parameter [-] - Pflanz method
        """ 
        # A = 2*m/(C_d*S_o*ro*V_1*t_inf)
        self.fBallisticParameter = 2.0*self.fMass/(self.fVehicleDragArea*self.dcParameters["AIR_DENSITY"]*self.fOpenInitVelocity*self.fInflationTime)
        return self.fBallisticParameter
    
    def getPeakOpeningLoadPflanz(self):
        """
        Peak opening load [N] - Pflanz method
        """
        # Dynamic pressure at the start of inflation
        # q_1 = (ro*V_1**2)/2        
        fPressure = self.dcParameters["AIR_DENSITY"]*self.fOpenInitVelocity**2/2
        # Peak opening load
        # F_max = q_1*C_d*S_o*C_x*X_1
        self.fPeakOpeningLoadPflanz = fPressure*self.dcParameters["OPENING_LOAD_SHOCK_FACTOR"]*self.fVehicleDragArea*self.dcParameters["OPENING_FORCE_REDUCTION_FACTOR"]
        return self.fPeakOpeningLoadPflanz
    
    def getPeakOpeningLoadOSCALC(self):
        """
        Peak opening load [N] - OSCALC method
        """
        # Standard non-dimensional inflation time
        # n_inf = t_inf*V_0/S_o
        fSNFInf = self.fInflationTime * self.fOpenInitVelocity / self.fCanopyArea
        # Generalized non-dimensional inflation time
        fGNFInf = fSNFInf * self.fCanopyArea * self.dcParameters["DRAG_INTEGRAL"] / np.sqrt(self.fVehicleDragArea)
        if fGNFInf < 4.0: print(f"Generalized non-dimensional inflation time is too low ({fGNFInf})!")
        # Mass ratio
        # R_m = ro*(C_d*S_o)**(3/2)/m
        self.fMassRatio = self.dcParameters["AIR_DENSITY"] * self.fVehicleDragArea**(3/2) / self.fMass 
        # Peak opening load
        self.fPeakOpeningLoadOSCALC = self.dcParameters["AIR_DENSITY"]/2.0*self.fOpenInitVelocity**2*self.fVehicleDragArea*1.25
        return self.fPeakOpeningLoadOSCALC
    
    def getPeakOpeningLoadSimplified(self):
        """
        Peak opening load [N] - Simplified method
        """
        self.fPeakOpeningLoadSimplified = self.dcParameters["AIR_DENSITY"]*self.fOpenInitVelocity**2*self.fVehicleDragArea*self.dcParameters["OPENING_LOAD_SHOCK_FACTOR"]*self.dcParameters["OPENING_FORCE_REDUCTION_FACTOR"]/2
        return self.fPeakOpeningLoadSimplified
    
    def getPeakOpeningLoad(self):
        """
        Peak opening load [N]:
        * Simplified method ('simplified')
        * OSCALC method ('oscalc')
        * Pflanz method ('pflanz')
        """
        dcDataOut = {}
        dcDataOut['oscalc'] = self.getPeakOpeningLoadOSCALC()
        dcDataOut['pflanz'] = self.getPeakOpeningLoadPflanz()
        dcDataOut['simplified'] = self.getPeakOpeningLoadSimplified()
        return dcDataOut
