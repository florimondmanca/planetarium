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


## Equations

### Deriving the adimensional form of equations of motion

#### Classical form of equations of motion for one planet

Consider a system of N planets (or other bodies like stars). Label each planet with a number i, i = 1, 2, ..., N.
The gravitational force felt by planet i can be computed like so:

$(1)\ \ F_i = \sum_{j \ne i} \frac{-Gm_im_j}{r_{ij}^2}$

and the second law of Newton follows:

$(2)\ \ m_i \frac{dv_i}{dt} = F_i$

#### Adapting the unit system

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

#### Adimensional form of equations of motion for one planet

Given in such units, one can show that Newton's second law $(2)$ writes:

$(2^*)\ \ m_i^* \frac{dv_i^*}{dt^*} = F_i^*$

where $F_i^*$ is written as:

$(1^*)\ \ F_i^* = \sum_{j \ne i} \frac{-G^*m_i^*m_j^*}{r_{ij}^*2}$

## Implementation

blah
