CENTER_OF_MASS = 'COM'
YOU = 'YOU'
SANTA = 'SAN'


def compose_map(orbit_list):
    satellite_map = {}
    for orbit in orbit_list:
        orbit_relationship = orbit.split(")")
        center = orbit_relationship[0]
        satellite = orbit_relationship[1]

        if center in satellite_map:
            satellite_map[center].append(satellite)
        else:
            satellite_map[center] = [satellite]

        if satellite not in satellite_map:
            satellite_map[satellite] = []

    return satellite_map;


def total_orbits(satellite_map, body, depth=0):
    direct_orbits = satellite_map[body]
    total = depth  # Shorthand accounting for indirect orbits
    for child in direct_orbits:
        total += total_orbits(satellite_map, child, depth=depth+1)
    return total


def distance_between_satellites(satellite_a, satellite_b, body, satellite_map):
    direct_orbits = satellite_map[body]
    distance_to_a = 0
    distance_to_b = 0
    for child in direct_orbits:
        if child == satellite_a:
            distance_to_a = 1
        elif child == satellite_b:
            distance_to_b = 1
        else:
            search_result = distance_between_satellites(satellite_a, satellite_b, child, satellite_map)
            if type(search_result) == int:
                return search_result
            if search_result[0] > 0:
                distance_to_a = search_result[0] + 1
            if search_result[1] > 0:
                distance_to_b = search_result[1] + 1

    if distance_to_a > 0 and distance_to_b > 0:
        # NOTE THE -2, to account for shifting into the same orbit, not reaching the actual satellite
        return distance_to_a + distance_to_b - 2
    return distance_to_a, distance_to_b


fp = open('input.txt', 'r')
orbits = fp.read().splitlines()
orbit_map = compose_map(orbits)
print(orbit_map)

print("TOTAL ORBITS", total_orbits(orbit_map, CENTER_OF_MASS))
print("Distances: ", distance_between_satellites(YOU, SANTA, CENTER_OF_MASS, orbit_map))