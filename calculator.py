#!/usr/bin/env python3
"""
Agri Drone Power Sizing Calculator
Estimate load per axis, thrust/weight ratio, hover power and hover time
for multirotor agriculture spray drones.

Component data: see components.csv (sourced from https://bharatskytech.com/)
MIT License.
"""
import argparse
import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load_components():
    motors, batteries = {}, {}
    with open(os.path.join(HERE, "components.csv"), newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["type"] == "motor":
                motors[row["id"]] = row
            elif row["type"] == "battery":
                batteries[row["id"]] = row
    return motors, batteries


def num(v):
    return float(v) if v not in ("", None) else None


def main():
    motors, batteries = load_components()
    p = argparse.ArgumentParser(description="Agriculture drone power sizing")
    p.add_argument("--auw", type=float, required=True, help="All-up weight in kg (full tank)")
    p.add_argument("--axes", type=int, required=True, choices=[4, 6, 8], help="Number of motors")
    p.add_argument("--motor", required=True, choices=sorted(motors), help="Motor/prop combo id")
    p.add_argument("--battery", required=True, choices=sorted(batteries), help="Battery pack id")
    p.add_argument("--series", type=int, default=1, help="Packs in series (2x 6S = 12S)")
    p.add_argument("--parallel", type=int, default=1, help="Packs in parallel")
    p.add_argument("--eff", type=float, help="Override efficiency in g/W at hover")
    p.add_argument("--usable", type=float, default=0.8, help="Usable capacity fraction (default 0.8)")
    a = p.parse_args()

    m, b = motors[a.motor], batteries[a.battery]

    load = a.auw / a.axes
    tow_min, tow_max = num(m["tow_min_kg"]), num(m["tow_max_kg"])
    status = "OK" if tow_min <= load <= tow_max else ("UNDER-LOADED" if load < tow_min else "OVERLOADED")
    print(f"Load per axis        : {load:.2f} kg  (recommended {tow_min:g}–{tow_max:g} kg)  {status}")

    tw = num(m["max_thrust_kg"]) * a.axes / a.auw
    print(f"Thrust/weight ratio  : {tw:.2f} : 1{'':28}{'OK' if tw >= 1.8 else 'LOW - below 1.8:1'}")

    cells = int(b["cells"]) * a.series
    volts = float(b["nominal_v"]) * a.series
    ah = float(b["capacity_mah"]) / 1000 * a.parallel
    wh = volts * ah
    print(f"Battery              : {cells}S {ah*1000:.0f}mAh  ({wh:.1f} Wh)")
    smin, smax = int(m["cells_min"]), int(m["cells_max"])
    if not smin <= cells <= smax:
        print(f"  WARNING: motor is rated for {smin}–{smax}S, battery is {cells}S")

    eff = a.eff
    if eff is None and m["eff_g_per_w_min"]:
        eff = (num(m["eff_g_per_w_min"]) + num(m["eff_g_per_w_max"])) / 2
    if eff is None:
        print("Est. hover power     : n/a - no published g/W figure for this motor; pass --eff")
        sys.exit(0)

    power = a.auw * 1000 / eff
    t = wh * a.usable / power * 60
    print(f"Est. hover power     : ~{power:,.0f} W  (at {eff:.2f} g/W)")
    print(f"Est. hover time      : ~{t:.1f} min at {a.usable:.0%} usable capacity")


if __name__ == "__main__":
    main()
