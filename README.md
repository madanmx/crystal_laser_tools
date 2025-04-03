Program Description: Photon Absorption Calculator

This program calculates the number of photons absorbed per molecule in a light-absorbing sample, based on specified sample properties and illumination conditions. The current implementation uses a simplified model that assumes equal probabilities for both single- and multi-photon absorption processes.

Key Assumptions:

Uniform Fluence: The incident pump laser fluence is considered constant across the entire illuminated area. This models experimental setups where:

The probe beam is significantly smaller than the pump beam

Typical application: Serial Femtosecond Crystallography (SFX) experiments where:

Optical pump pulses are focused to ~100 μm diameter

X-ray probe beams are focused to ~1 μm diameter at the interaction point

Beam Alignment: By default, calculations assume:

The probe beam is perfectly centered within the pump beam

Sampled molecules experience peak pump intensity

Optional parameter allows for off-center probing (intensity gradient sampling)

Beam Characteristics:

Pump pulse intensity is time-independent (no temporal variation)

Spatial intensity profile follows a Gaussian distribution

Note: This represents a first-order approximation that intentionally simplifies certain physical aspects of photon absorption dynamics for modeling purposes. The model can be extended to incorporate more complex scenarios as needed.
