from omega import *
from omegaToolkit import *

mm = MenuManager.createAndInitialize()
appMenu = mm.createMenu("contolPanel")

appMenu.addButton("OrbitScale +", "incrementOrbit()")
appMenu.addButton("OrbitScale -", "decrementOrbit()")
appMenu.addButton("RadiusScale +", "incrementRadius()")
appMenu.addButton("RadiusScale -", "decrementRadius()")

appMenu.addButton("Show Galaxy", "switchSystemInCave(galaxy)")
appMenu.addButton("Reset View", "resetView()")