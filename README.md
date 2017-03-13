# Planetarium

Planetarium is a 2D astromechanical engine to create and simulate systems of planets and stars.

The simulations can be visualized in a pygame GUI.

Planetarium allows to create '.planet' files to define the bodies' (planets or stars) properties and manage simulation cases more easily:
- mass
- initial position
- initial velocity (direction and speed)

Multiple integration methods are available:
- Euler integration
- Verlet integration
- Runge-Kutta methods
- ...


## Deriving the astronomical form of equations of motion

### Adapting the unit system

To avoid dealing with very large or very small numbers and reduce numerical errors, a change in the units is necessary.

| Quantity 	| ISU 	| Astronomical equivalent 	| Conversion        	|
|----------	|:---:	|-------------------------	|-------------------	|
| Distance 	| m   	| AU                      	| 1AU = 1.496e11 m   	|
| Time     	| s   	| yr                      	| 1 yr = 3.156e7 s  	|
| Mass     	| kg  	| Ms                      	| 1 Ms = 1.99e30 kg 	|
| Force    	| N   	| F                      	| 1 F = 2.989e23 N 	|

where:
- AU = astronomical unit
- yr = year
- Ms = solar mass
- F = arbitrary unit computed as `Ms * AU / yr^2`
