import numpy as np

from calculations.ConstantParameters import *

def calculateHumidity(fRefHumidity: float, fHeightChange: float):
    return min(1.0,max(0.0, fRefHumidity+0.05*fHeightChange/1000.0))


def calculatePressure(fRefPressure: float, fRefTemp: float, fHeightChange: float, dcParameters: dict = INPUT_PARAMETERS):
    """
    Calculate atmospheric pressure at given altitude
    """
    return fRefPressure * ((fRefTemp + fHeightChange*LAPSE_RATE) / fRefTemp)**(dcParameters['G_ACCELERATION']*MOLAR_MASS_AIR/(UNIVERSAL_GAS_CONSTANT*LAPSE_RATE))

def getAirDensity(fRefPressure: float, fRefTemp: float, fHeightChange: float, fHumidity: float = 0.0, dcParameters: dict = INPUT_PARAMETERS):
    """
    Calculate air density at given altitude
    """
    fHumidity = calculateHumidity(fHumidity, fHeightChange)
    fPressure = calculatePressure(fRefPressure, fRefTemp, fHeightChange, dcParameters)
    fTemperature = getTemperature(fRefTemp, fHeightChange)
    fVapourPressure = getVapourPressure(fHumidity, fTemperature)
    fPartialPressure = fPressure-fVapourPressure
    return (MOLAR_MASS_VAPOUR*fVapourPressure + MOLAR_MASS_AIR*fPartialPressure) / (UNIVERSAL_GAS_CONSTANT*fTemperature)

def getTemperature(fRefTemp: float, fHeightChange: float):
    return  fRefTemp+fHeightChange*LAPSE_RATE

def getVapourPressure(fHumidity: float, fTemperature: float):
    return fHumidity * 6.1078**(7.5*fTemperature/(fTemperature+237.3))