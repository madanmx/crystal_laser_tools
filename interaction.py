import math
from .constants import *
from .utils import get_float_input, get_int_input, get_str_input
from .crystal import calculate_chromophore_concentration, determine_crystal_system, calculate_unit_cell_volume

def calculate_penetration_depth(ext_coeff, conc):
    """Calculate 1/e penetration depth.
    
    Args:
        ext_coeff: Extinction coefficient (l/(mol cm))
        conc: Concentration (mol/l)
    
    Returns:
        Penetration depth in meters
    """
    return -math.log10(1/math.e) / (conc * (ext_coeff * 100))

def calculate_laser_sample_interaction(
    extinction_coefficient=45600,
    sample_thickness=5e-6,
    chromophore_concentration=0.02,
    pulse_energy=0.25e-6,
    beam_diameter_input=100e-6,
    beam_diameter_type="FWHM",
    pulse_duration=145e-15,
    wavelength=532e-9,
    laser_offset=0,
    verify_with_crystal=False,
    crystal_params=None
):
    """Calculate laser-sample interaction parameters.
    
    Args:
        Various laser and sample parameters with defaults
        verify_with_crystal: Whether to verify concentration with crystal parameters
        crystal_params: Dictionary of crystal parameters if verification is needed
    
    Returns:
        Dictionary of calculated results
    """
    # Calculate 1/e penetration depth
    penetration_depth = calculate_penetration_depth(extinction_coefficient, chromophore_concentration)
    
    # Calculate beam parameters
    if beam_diameter_type == "FWHM":
        beam_diameter_1e2 = beam_diameter_input * 1.699  # Convert FWHM to 1/e² diameter
    else:
        beam_diameter_1e2 = beam_diameter_input
    
    beam_radius_1e2 = beam_diameter_1e2 / 2  # 1/e² radius in m
    
    # Calculate fluence (peak)
    beam_area = 0.5 * math.pi * (beam_radius_1e2)**2
    fluence_peak = pulse_energy / beam_area  # J/m²
    
    # Calculate reduction factor at interaction point (IP)
    reduction_factor = math.exp(-2 * (laser_offset)**2 / (beam_radius_1e2)**2)
    intensity_percent_at_IP = reduction_factor * 100
    
    # Calculate fluence at IP
    fluence_at_IP = fluence_peak * reduction_factor
    
    # Calculate power density
    power_density_peak = fluence_peak / pulse_duration  # W/m²
    power_density_at_IP = power_density_peak * reduction_factor
    
    # Calculate photon energy and density
    photon_energy = (PLANCK * SPEED_OF_LIGHT) / wavelength  # J
    photon_density_at_IP = fluence_at_IP / photon_energy  # photons/m²
    
    # Calculate chromophore particle density (molecules/m³)
    chromophore_density = chromophore_concentration * AVOGADRO  # molecules/l
    chromophore_density *= 1000  # convert to molecules/m³
    
    # Calculate absorption fraction in sample thickness
    absorption_term = extinction_coefficient * 100 * chromophore_concentration * sample_thickness
    absorption_fraction = 1 - 10**(-absorption_term)
    
    # Calculate number of molecules per area in sample thickness
    molecules_per_area = chromophore_density * sample_thickness  # molecules/m²
    
    # Calculate absorbed photons per molecule
    absorbed_photons_per_molecule = (absorption_fraction * photon_density_at_IP) / molecules_per_area
    
    # Optional crystal verification
    crystal_verification = None
    if verify_with_crystal and crystal_params:
        try:
            a = crystal_params.get('a', DEFAULT_A) * 1e-10
            b = crystal_params.get('b', DEFAULT_B) * 1e-10
            c = crystal_params.get('c', DEFAULT_C) * 1e-10
            alpha = math.radians(crystal_params.get('alpha', DEFAULT_ALPHA))
            beta = math.radians(crystal_params.get('beta', DEFAULT_BETA))
            gamma = math.radians(crystal_params.get('gamma', DEFAULT_GAMMA))
            Z = crystal_params.get('Z', DEFAULT_Z)
            
            unit_cell_volume = calculate_unit_cell_volume(a, b, c, alpha, beta, gamma)
            crystal_system = determine_crystal_system(a, b, c, alpha, beta, gamma)
            crystal_concentration = (Z / AVOGADRO) / (unit_cell_volume * 1000)  # mol/l
            
            crystal_verification = {
                'calculated_concentration': crystal_concentration,
                'input_concentration': chromophore_concentration,
                'difference': abs(crystal_concentration - chromophore_concentration),
                'crystal_system': crystal_system.name,
                'unit_cell_volume': unit_cell_volume
            }
        except Exception as e:
            crystal_verification = {'error': str(e)}
    
    # Return results as a dictionary
    return {
        'concentration': chromophore_concentration,
        'penetration_depth': penetration_depth,
        'beam_diameter_1e2': beam_diameter_1e2,
        'intensity_percent_at_IP': intensity_percent_at_IP,
        'fluence': {
            'at_IP': fluence_at_IP,
            'peak': fluence_peak
        },
        'power_density': {
            'at_IP': power_density_at_IP,
            'peak': power_density_peak
        },
        'photon_energy': photon_energy,
        'photon_density_at_IP': photon_density_at_IP,
        'absorption_fraction': absorption_fraction,
        'absorbed_photons_per_molecule': absorbed_photons_per_molecule,
        'crystal_verification': crystal_verification
    }
