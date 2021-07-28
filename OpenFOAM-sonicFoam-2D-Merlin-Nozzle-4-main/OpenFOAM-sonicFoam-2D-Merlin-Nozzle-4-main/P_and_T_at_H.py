"""Calculating Pressure & Temperature @ altitude"""

# specify values at a know altitude
precision = 5   # specify how many decimal points you want (must be an integer value)
P_0 = 101325    # pressure @ sea level [Pa]
h_a = 900       # known altitude [m]
T_a = 15        # temperature @ known altitude [C]

# Compute values at new location
print("\n===========================")
h = int(input("Altitude [m]: "))
print("---------------------------")
# altitude to calculate new parameters
T = T_a - 0.0065 * (h - h_a)                            # temperature @ h [C]
P = P_0 * (1 - (0.0065*h)/(T+0.0065*h+273.15))**5.257   # pressure @ h [Pa]

# Print values
print("Temperature:", round(T, precision), "[\N{DEGREE SIGN}C]")
print("Pressure:", round(P, precision), "[Pa]")
print("===========================")
print("\033[3m*note that this should only be used for a rough-estimate\033[0m")

