'''
IBEHS 1P10 DP2 Main Computing File

Team Number: 24

Student Details (Name, Student Number): Ahmed Khaleel, 400459125


Student Details (Name, Student Number): Taite Beggs, 400473665


Date: 2022-12-07
'''

# Worked together on code, did not individually assign objectives

import math

# Subprogram 1

def calc_min_stem_dia(body_weight, canal_diameter, femoral_head_offset, ult_ten_strength):
    stem_dia = 0.85 * canal_diameter # Initial estimate
    fracture_risk = 1 # Initializing variable to use in while loop

    while fracture_risk >= 1:
        # Calculate axial stress
        F = 3.25 * body_weight
        A = (math.pi)*(stem_dia/2)**2
        axial_stress = F / A

        # Calculate bending moment
        M = F * femoral_head_offset
        y = 0.5 * stem_dia
        I = (math.pi/64)*(stem_dia)**4
        bending_stress = M*y/I

        # Calculate fracture risk
        app_ten_stress = axial_stress + bending_stress
        fracture_risk = app_ten_stress / ult_ten_strength

        # Now slightly increase the stem diameter
        stem_dia += 0.1

    min_stem_dia = stem_dia

    print(f"The body weight is {body_weight:0.1f} N. The canal diamater is {canal_diameter} mm. The ultimate tensile strength is {ult_ten_strength} MPa.")
    print(f"The minimum stem diameter is {min_stem_dia:0.1f} mm.")
    print(f"The applied tensile stress that corresponds to the minimum allowable stem diameter is {app_ten_stress:0.1f} MPa.")

# Subprogram 2

def calc_fatigue_life(stem_dia, body_weight, team_number, filename):

    # Area calculated from given stem diameter
    A = math.pi/4 * stem_dia**2

    # Undergoes maximum cyclical loads
    F_max = 10*body_weight
    F_min = -10*body_weight

    stress_amp = (F_max - F_min)/(2*A)

    # Initialize lists to append to
    S = []
    N = []

    # Open SN Data file, convert to number types, and append
    file = open(filename, "r")
    for line in file:
        data = line.split()
        S.append(float(data[0]))
        N.append(int(data[1]))
    file.close()

    cycles_fail = 0

    # Calcaulte Kn for each N, and the adjusted stress amplitude
    for i in range(len(S)):
        K_n = 9.25 + math.log(N[i],10)**(0.65 * (team_number/40))
        stress_amp_adj = K_n * stress_amp

        # Once adjusted stress amplitude is greater than a given stress amplitude, break
        if stress_amp_adj > S[i]:
            cycles_fail = N[i]
            stress_fail = stress_amp_adj
            break

    if cycles_fail == 0:
        print("The implant will not fail.")
    else:
        print(f"The number of cycles to failure is equal to {cycles_fail}.")
        print(f"The adjusted stress amplitude is equal to {stress_fail:0.1f} MPa")

# Subprogram 3

def calc_fracture_risk(body_weight, outer_dia, canal_diameter, modulus_bone, modulus_implant):

    # Calculate compressive stress
    F = 28 * body_weight 
    A = (math.pi / 4) * (outer_dia**2 - canal_diameter**2)
    comp_stress = F / A

    # Calculate reduced compressive stress
    stress_reduc = comp_stress * ((4*modulus_bone) / (modulus_bone + modulus_implant))**(1/3)

    # Calculate modulus ratio
    E_ratio = (modulus_implant/modulus_bone)**(1/2)

    # Calcualte failure stress, given number of years
    x = 0
    while True:
        comp_strength = 0.0012*(x**2)-3.725*x*E_ratio+186.42
        if comp_strength < stress_reduc:
            stress_fail = comp_strength
            yrs_fail = x
            break
        else:
            print(f"At {x} years after implantation, the compressive strength is {comp_strength:0.1f} MPa.")
            x += 1
    print(f"At {yrs_fail} years after implantation, there is a risk of femoral fracture. The corresponding failure stress is {stress_fail:0.1f} MPa.")

# Menu

def main():

    # Define variables

    team_number = 24
    mass = 51.5 #kg
    body_weight = mass * 9.81
    outer_dia = 22 #mm
    canal_diameter = 11.5 #mm
    femoral_head_offset = 32 #mm
    modulus_bone = 18.6 #GPa, Source: https://pubmed.ncbi.nlm.nih.gov/14517712/
    ult_ten_strength = 290 #MPa, Zirconia toughened alumina
    modulus_implant = 360 #GPa, Zirconia toughened alumina
    stem_dia = 11 #mm, approximate average stem diameter from 3D model

    filename = "SN Data - Sample Ceramic.txt" # For subprogram 2
    
    print("DP2 Team 24")

    while True:
        program = input("\nChoose a subprogram (1-3) or 'e' to exit:\t")
        if program == '1':
            print("\nRunning program 1\n")
            calc_min_stem_dia(body_weight, canal_diameter, femoral_head_offset, ult_ten_strength)
            # Currently, min_stem_dia is larger than our canal diameter since this does take into account the stress that goes to the femur, and therefore it will be a reasonable number in subprogram 3
        elif program == '2':
            print("\nRunning program 2\n")
            calc_fatigue_life(stem_dia, body_weight, team_number, filename)
            # For our patient, our fatigue life is less than what is available from the data, so the minimum ceramic cycles to failure is shown
        elif program == '3':
            print("\nRunning program 3\n")
            calc_fracture_risk(body_weight, outer_dia, canal_diameter, modulus_bone, modulus_implant)
        elif program == 'e':
            print("\nClosing program\n")
            break
        else:
            print("\nInput a number from 1 to 3 or 'e' to exit.")

main()