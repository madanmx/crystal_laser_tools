from enum import Enum
import math
from .constants import *

class CrystalSystem(Enum):
    """Enumeration of crystal systems."""
    TRICLINIC = 1
    MONOCLINIC = 2
    ORTHORHOMBIC = 3
    TETRAGONAL = 4
    RHOMBOHEDRAL = 5
    HEXAGONAL = 6
    CUBIC = 7

def determine_crystal_system(a, b, c, alpha, beta, gamma):
    """Determine crystal system based on lattice parameters.
    
    Args:
        a, b, c: Unit cell lengths (in meters)
        alpha, beta, gamma: Unit cell angles (in radians)
    
    Returns:
        CrystalSystem enum member
    """
    tol = 1e-4  # Tolerance for floating point comparisons
    
    # Convert to radians if angles are in degrees
    if alpha > 2*math.pi: alpha = math.radians(alpha)
    if beta > 2*math.pi: beta = math.radians(beta)
    if gamma > 2*math.pi: gamma = math.radians(gamma)
    
    # Check for cubic system (a = b = c, α = β = γ = 90°)
    if (abs(a - b) < tol and abs(b - c) < tol and 
        abs(alpha - math.pi/2) < tol and 
        abs(beta - math.pi/2) < tol and 
        abs(gamma - math.pi/2) < tol):
        return CrystalSystem.CUBIC
    
    # Check for hexagonal (a = b ≠ c, α = β = 90°, γ = 120°)
    if (abs(a - b) < tol and abs(b - c) > tol and 
        abs(alpha - math.pi/2) < tol and 
        abs(beta - math.pi/2) < tol and 
        abs(gamma - 2*math.pi/3) < tol):
        return CrystalSystem.HEXAGONAL
    
    # Check for rhombohedral (a = b = c, α = β = γ ≠ 90°)
    if (abs(a - b) < tol and abs(b - c) < tol and 
        abs(alpha - beta) < tol and abs(beta - gamma) < tol and 
        abs(alpha - math.pi/2) > tol):
        return CrystalSystem.RHOMBOHEDRAL
    
    # Check for tetragonal (a = b ≠ c, α = β = γ = 90°)
    if (abs(a - b) < tol and abs(b - c) > tol and 
        abs(alpha - math.pi/2) < tol and 
        abs(beta - math.pi/2) < tol and 
        abs(gamma - math.pi/2) < tol):
        return CrystalSystem.TETRAGONAL
    
    # Check for orthorhombic (a ≠ b ≠ c, α = β = γ = 90°)
    if (abs(alpha - math.pi/2) < tol and 
        abs(beta - math.pi/2) < tol and 
        abs(gamma - math.pi/2) < tol):
        return CrystalSystem.ORTHORHOMBIC
    
    # Check for monoclinic (α = γ = 90° ≠ β)
    if (abs(alpha - math.pi/2) < tol and 
        abs(gamma - math.pi/2) < tol and 
        abs(beta - math.pi/2) > tol):
        return CrystalSystem.MONOCLINIC
    
    # Default to triclinic
    return CrystalSystem.TRICLINIC

def calculate_unit_cell_volume(a, b, c, alpha, beta, gamma):
    """Calculate unit cell volume based on crystal system.
    
    Args:
        a, b, c: Unit cell lengths (in meters)
        alpha, beta, gamma: Unit cell angles (in radians)
    
    Returns:
        Volume in cubic meters
    """
    system = determine_crystal_system(a, b, c, alpha, beta, gamma)
    
    # Convert angles to radians if they're in degrees
    if alpha > 2*math.pi: alpha = math.radians(alpha)
    if beta > 2*math.pi: beta = math.radians(beta)
    if gamma > 2*math.pi: gamma = math.radians(gamma)
    
    if system == CrystalSystem.CUBIC:
        return a ** 3
        
    elif system == CrystalSystem.TETRAGONAL:
        return a * a * c
        
    elif system == CrystalSystem.ORTHORHOMBIC:
        return a * b * c
        
    elif system == CrystalSystem.HEXAGONAL:
        return a * a * c * math.sin(2*math.pi/3)
        
    elif system == CrystalSystem.RHOMBOHEDRAL:
        cos_alpha = math.cos(alpha)
        return a**3 * math.sqrt(1 - 3*cos_alpha**2 + 2*cos_alpha**3)
        
    elif system == CrystalSystem.MONOCLINIC:
        return a * b * c * math.sin(beta)
        
    else:  # TRICLINIC
        cos_alpha = math.cos(alpha)
        cos_beta = math.cos(beta)
        cos_gamma = math.cos(gamma)
        return a * b * c * math.sqrt(
            1 + 2*cos_alpha*cos_beta*cos_gamma 
            - cos_alpha**2 - cos_beta**2 - cos_gamma**2
        )

def calculate_chromophore_concentration(a, b, c, alpha, beta, gamma, Z):
    """Calculate chromophore concentration from crystal parameters.
    
    Args:
        a, b, c: Unit cell lengths (in meters)
        alpha, beta, gamma: Unit cell angles (in radians)
        Z: Number of absorbing molecules per unit cell
    
    Returns:
        Tuple of (concentration in mol/L, concentration in mol/m³, crystal system, volume in m³)
    """
    # Determine crystal system and volume
    crystal_system = determine_crystal_system(a, b, c, alpha, beta, gamma)
    V_cell = calculate_unit_cell_volume(a, b, c, alpha, beta, gamma)

    # Calculate concentration
    C_mol_per_m3 = Z / (AVOGADRO * V_cell)
    C_mol_per_L = C_mol_per_m3 * 1e-3

    return C_mol_per_L, C_mol_per_m3, crystal_system, V_cell
