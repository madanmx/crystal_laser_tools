def get_float_input(prompt, default):
    """Get float input from user with a default value."""
    while True:
        try:
            value = input(f"{prompt} [default: {default}]: ") or default
            return float(value)
        except ValueError:
            print("Please enter a valid number")

def get_int_input(prompt, default):
    """Get integer input from user with a default value."""
    while True:
        try:
            value = input(f"{prompt} [default: {default}]: ") or default
            return int(value)
        except ValueError:
            print("Please enter a valid integer")

def get_str_input(prompt, default, options=None):
    """Get string input from user with a default value and optional validation."""
    while True:
        value = input(f"{prompt} [default: {default}]: ") or default
        if options is None or value in options:
            return value
        print(f"Please enter one of: {', '.join(options)}")

def format_results(results):
    """Format the results dictionary into a human-readable string."""
    output = f"""\n=== Results ===
Concentration of absorbing molecules:
    {results['concentration']:.9f}\tmol/l
1/e penetration depth of sample:
    {results['penetration_depth'] * 1e6:.9f}\tµm

Pump intensity at interaction point (IP) [% of peak value]:
    {results['intensity_percent_at_IP']:.1f}\t%
{results['beam_diameter_1e2'] * 1e6:.1f}\tµm\tbeam diameter (1/e²)

Laser fluence:
    at IP\t{results['fluence']['at_IP'] * 1e-1:.2E}\tmJ/cm²
    peak\t{results['fluence']['peak'] * 1e-1:.2E}\tmJ/cm²

Laser power density:
    at IP\t{results['power_density']['at_IP'] * 1e-7:.2E}\tGW/cm²
    peak\t{results['power_density']['peak'] * 1e-7:.2E}\tGW/cm²

Average number of absorbed photons/absorbing molecule:
    {results['absorbed_photons_per_molecule']:.1f}\tphotons/molecule"""

    if results['crystal_verification'] and 'error' not in results['crystal_verification']:
        output += f"""\n
Crystal verification:
    Calculated concentration: {results['crystal_verification']['calculated_concentration']:.6f} mol/L
    Difference: {results['crystal_verification']['difference']:.6f} mol/L
    Crystal system: {results['crystal_verification']['crystal_system']}
    Unit cell volume: {results['crystal_verification']['unit_cell_volume']:.3e} m³"""

    return output
