from .crystal import calculate_chromophore_concentration
from .interaction import calculate_laser_sample_interaction
from .utils import get_float_input, get_int_input, get_str_input, format_results

def interactive_chromophore_concentration():
    """Interactive chromophore concentration calculation."""
    print("\n=== Chromophore Concentration Calculator ===")
    print("Please enter the crystal cell parameters (press Enter for defaults):\n")
    
    # Get user input with defaults
    a = get_float_input("a (Å)", 62) * 1e-10  # Convert Å to m
    b = get_float_input("b (Å)", 62) * 1e-10
    c = get_float_input("c (Å)", 111) * 1e-10
    alpha = math.radians(get_float_input("α (degrees)", 90))
    beta = math.radians(get_float_input("β (degrees)", 90))
    gamma = math.radians(get_float_input("γ (degrees)", 120))
    Z = get_int_input("Number of absorbing molecules per unit cell", 6)

    # Calculate concentration
    C_mol_per_L, C_mol_per_m3, crystal_system, V_cell = calculate_chromophore_concentration(
        a, b, c, alpha, beta, gamma, Z
    )

    # Print results
    print("\n=== Results ===")
    print(f"Crystal system: {crystal_system.name}")
    print(f"Unit cell volume: {V_cell*1e30:.2f} Å³")
    print(f"Chromophore concentration: {C_mol_per_L:.6f} mol/L")
    print(f"Chromophore concentration: {C_mol_per_m3:.2f} mol/m³")
    
    return C_mol_per_L

def interactive_laser_sample_interaction(chromophore_concentration=None):
    """Interactive laser-sample interaction calculation."""
    print("\n=== Laser-Sample Interaction Calculator ===")
    print("Enter values or press Enter to use defaults\n")
    
    # Get input parameters
    extinction_coefficient = get_float_input("Extinction coefficient (l/(mol cm))", 45600)
    sample_thickness = get_float_input("Sample thickness (µm)", 5) * 1e-6  # Convert µm to m
    
    # Use provided concentration or ask for it
    if chromophore_concentration is None:
        chromophore_concentration = get_float_input("Chromophore concentration (mol/l)", 0.02)
    
    pulse_energy = get_float_input("Pulse energy (µJ)", 0.25) * 1e-6  # Convert µJ to J
    beam_diameter_input = get_float_input("Beam diameter (µm)", 100) * 1e-6  # Convert µm to m
    beam_diameter_type = get_str_input("Beam diameter type (FWHM/1/e²)", "FWHM", ["FWHM", "1/e²"])
    pulse_duration = get_float_input("Pulse duration (fs)", 145) * 1e-15  # Convert fs to s
    wavelength = get_float_input("Wavelength (nm)", 532) * 1e-9  # Convert nm to m
    laser_offset = get_float_input("Laser offset (µm)", 0) * 1e-6  # Convert µm to m
    
    # Optional crystal verification
    crystal_params = None
    use_crystal = get_str_input("Use crystal parameters to verify concentration? (y/n)", "n", ["y", "n"])
    
    if use_crystal.lower() == 'y':
        print("\n=== Crystal Parameters ===")
        crystal_params = {
            'a': get_float_input("a (Å)", 62),
            'b': get_float_input("b (Å)", 62),
            'c': get_float_input("c (Å)", 111),
            'alpha': get_float_input("alpha (degrees)", 90),
            'beta': get_float_input("beta (degrees)", 90),
            'gamma': get_float_input("gamma (degrees)", 120),
            'Z': get_int_input("Molecules per unit cell", 6)
        }
    
    # Calculate interaction
    results = calculate_laser_sample_interaction(
        extinction_coefficient=extinction_coefficient,
        sample_thickness=sample_thickness,
        chromophore_concentration=chromophore_concentration,
        pulse_energy=pulse_energy,
        beam_diameter_input=beam_diameter_input,
        beam_diameter_type=beam_diameter_type,
        pulse_duration=pulse_duration,
        wavelength=wavelength,
        laser_offset=laser_offset,
        verify_with_crystal=(use_crystal.lower() == 'y'),
        crystal_params=crystal_params
    )
    
    print(format_results(results))
    return results

def main_menu():
    """Main menu for the command-line interface."""
    while True:
        print("\n=== Main Menu ===")
        print("1. Calculate chromophore concentration from crystal parameters")
        print("2. Calculate laser-sample interaction parameters")
        print("3. Full workflow (both calculations)")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            interactive_chromophore_concentration()
            input("\nPress Enter to continue...")
        elif choice == "2":
            interactive_laser_sample_interaction()
            input("\nPress Enter to continue...")
        elif choice == "3":
            conc = interactive_chromophore_concentration()
            input("\nPress Enter to continue to laser-sample interaction...")
            interactive_laser_sample_interaction(conc)
            input("\nPress Enter to continue...")
        elif choice == "4":
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please enter 1-4.")
