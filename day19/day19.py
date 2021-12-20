from funcy import print_durations
import numpy as np
import pandas as pd
from io import StringIO
from collections import deque

# Puzzle: https://adventofcode.com/2021/day/19
# - an assortment of beacons and scanners float motionless in the water
# - each scanner is capable of detecting all beacons in a cube centered on the scanner
# - scanners do not know their own position
# - scanner regions overlap
# - at least 12 beacons within each overlap between scanner pair
# - each scanner could be in any of 24 different orientations:
#   facing positive or negative x, y, or z, four directions "up" from that facing
#
# task: how many beacons are there
# input: relative 3D positions of beacons detected by each scanner
#
# solution:
# (I) find scanner pairs with overlap
#  - for all beacons in a scan as reference beacon, hash all beacons in scan
#  - compare with all other beacons hashes in all other scans
#  - >= 12 matching hashes? -> overlap, found pair
# (II) find transforms between scanners
#  - scanner 0 is reference at (0, 0, 0), direction xyz
#  - for any matching overlap, take 4 points, compute transform
# (III) transform all beacons, return take unique number

def read_scans(file):
    scans = []
    with open(file, "r") as f:
        for scan_chunk in f.read().split("\n\n"):
            beacons = np.loadtxt(StringIO(scan_chunk), skiprows=1, dtype=np.int16, delimiter=",")
            ones = np.ones((beacons.shape[0], 1), dtype=np.int16)
            beacons_homogeneous = np.hstack((beacons, ones))
            scans.append(beacons_homogeneous)

    return scans

def beacon_hash(beacon_list, reference_beacon):
    # hash function: manhatten distance to reference beacon
    return np.abs(beacon_list - reference_beacon).sum(axis=1)

def build_lookup(scan):
    lookup_beacons = []
    lookup_sets = []
    for ref_beacon in scan:
        bh = beacon_hash(scan, ref_beacon)
        lookup_beacons.append(bh)
        lookup_sets.append(set(bh))
    
    return lookup_beacons, lookup_sets

def transform_beacons(beacons, orientation):
    pass

def find_transform(source_transform, source_scan, target_scan, source_lookups, target_lookups):
    matching_beacon_hashes = list(set(source_lookups) & set(target_lookups))
    source_matches = []
    target_matches = []
    for match_id, match in enumerate(matching_beacon_hashes):
        source_match_id = np.nonzero(source_lookups==match)[0]
        target_match_id = np.nonzero(target_lookups==match)[0]

        # drop multiple matches
        if len(source_match_id) == 1 and len(target_match_id) == 1:
            source_matches.append(source_scan[source_match_id[0]])
            target_matches.append(target_scan[target_match_id[0]])

    source_matches = np.array(source_matches)    
    target_matches = np.array(target_matches)

    # transform ource matches in reference view (scan #0)
    source_matches_ref = np.dot(source_matches, source_transform)

    # find transform target matches to reference view
    transform = np.linalg.solve(target_matches[:4], source_matches_ref[:4])
    transform = np.rint(transform).astype(np.int16)

    return transform



def day19(file):

    scans = read_scans(file)
    scan_lookup_sets = []
    scan_lookup_beacons = []
    for scan in scans:
        lb, ls = build_lookup(scan)
        scan_lookup_beacons.append(lb)
        scan_lookup_sets.append(ls)

    scores = []

    for query_scan_id, query_scan in enumerate(scans):
        for qs_lookup_id, qs_lookup in enumerate(scan_lookup_sets[query_scan_id]):
            for match_scan_id, match_lookups in enumerate(scan_lookup_sets):

                if match_scan_id == query_scan_id:
                    continue

                for match_lookup_id, match_lookup in enumerate(match_lookups):
                    score = len(qs_lookup & match_lookup)
                    if score >= 12:
                        scores.append((query_scan_id, qs_lookup_id, match_scan_id, match_lookup_id, score))

    scores = sorted(scores, key=lambda x: x[3], reverse=True)
    scdf = pd.DataFrame(scores, columns=["query_scan_id", "qs_lookup_id", "match_scan_id", "match_lookup_id", "score"])        
    connections = scdf[scdf.score >= 12].groupby("query_scan_id").match_scan_id.unique()
    
    known_transforms = {0: np.eye(4, dtype=np.int16)}
    next_to_match = deque()
    for match in connections[0]:
        next_to_match.append((0, int(match)))
    
    while len(known_transforms) < len(scans):
        source_id, target_id = next_to_match.popleft()
        if target_id not in known_transforms:
            some_match = scdf[(scdf.query_scan_id == source_id) & (scdf.match_scan_id == target_id)].iloc[0]
            found_transform = find_transform(known_transforms[source_id], scans[source_id], scans[target_id], scan_lookup_beacons[source_id][some_match.qs_lookup_id], scan_lookup_beacons[target_id][some_match.match_lookup_id])
            known_transforms[target_id] = found_transform
            for match in connections[target_id]:
                next_to_match.append((target_id, int(match)))

    all_beacons = []

    for scan_id, beacons in enumerate(scans):
        transformed = beacons @ known_transforms[scan_id]
        all_beacons.append(transformed)

    all_beacons = np.concatenate(all_beacons)
    unique_rows = np.unique(all_beacons, axis=0)
    # for all measurements
    #  translate and rotate into scan-0 view
    #  insert coords into set
    # return len(coordset)
    yield unique_rows.shape[0]

    # day19 b: what is the largest Manhattan distance between any two scanners?

    max_dist = 0

    for a in known_transforms.values():
        for b in known_transforms.values():
            manhatten_dist = np.abs(a[-1] - b[-1]).sum()
            max_dist = max(max_dist, manhatten_dist)

    yield max_dist

@print_durations
def run_expect(file, result_a, result_b):

    a, b = day19(file)

    print(f"Day 19a {file}: {a}")
    assert a == result_a

    if result_b:
        print(f"Day 19b {file}: {b}")
        assert b == result_b


if __name__ == "__main__":

    run_expect("test_input.txt", 79, 3621)
    run_expect("input.txt", 306, 9764)


