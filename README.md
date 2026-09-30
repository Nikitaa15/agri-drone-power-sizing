# Agri Drone Power Sizing

An open calculator and component reference for sizing the **motor, propeller and battery** of 10L–30L agriculture spray drones. It is built for Indian drone builders, OEMs, RPTO students and university drone teams.

Maintained by [Bharat Skytech](https://bharatskytech.com/), an agriculture drone component supplier based in Gurugram, India.

---

## What this does

Tell it your all-up weight (AUW), number of motors and battery. It returns:

- the **load per motor**, checked against the manufacturer's recommended takeoff weight per axis
- the **thrust-to-weight ratio**, with a warning when it drops below 1.8 : 1
- an estimated **hover power** and **hover flight time**

```bash
python calculator.py --auw 50 --axes 4 --motor x9-plus-g2l-4314 --battery evercell-6s-22000 --series 2
```

Example output (a 20L-class quad with two 6S packs in series):

```
Load per axis        : 12.50 kg  (recommended 12–14 kg)  OK
Thrust/weight ratio  : 2.24 : 1                            OK
Battery              : 12S 22000mAh  (976.8 Wh)
Est. hover power     : ~6,024 W  (at 8.30 g/W)
Est. hover time      : ~7.8 min at 80% usable capacity
```

If a motor has no published g/W figure, pass your own measured value with `--eff`.

> These are estimates for planning. Real flight time depends on spray payload drawdown, wind, temperature, altitude and battery age. Always validate with a tethered or low-altitude hover test.

---

## The sizing method

**1. Load per axis**

```
load_per_axis (kg) = AUW (kg) / number_of_motors
```

Hobbywing publishes a *recommended takeoff weight per axis* for each power system. Stay inside that band. Running above it cuts efficiency and overheats the motor and ESC.

**2. Thrust-to-weight**

```
T/W = (max_thrust_per_axis × axes) / AUW
```

A **T/W of at least 1.8–2.0 : 1** is a common rule of thumb for spray drones, because they must climb and brake with a full tank.

**3. Hover power and time**

Manufacturers publish efficiency in **g/W** at the recommended load.

```
hover_power (W) = AUW (g) / efficiency (g/W)
battery_energy (Wh) = nominal_voltage × capacity (Ah)
hover_time (min) = battery_energy × usable_fraction / hover_power × 60
```

Use 0.8 for `usable_fraction`. Draining a LiPo to 0% shortens its life sharply.

---

## Component reference data

All figures are copied from the product pages linked below. See [`components.csv`](components.csv).

### Motor + propeller power systems

| Power system | KV | Voltage | Max thrust / axis | Recommended TOW / axis | Weight | Arm tube |
|---|---|---|---|---|---|---|
| [Hobbywing X6 Plus + 2480 prop](https://bharatskytech.com/product/hobbywing-x6-plus-motor-agriculture-drones/) | 150 | 12–14S | 11.8 kg | 3.5–5.5 kg | ~790 g | 28/30 mm |
| [Hobbywing X9 G2L + 3611 prop](https://bharatskytech.com/product/hobbywing-x9-g2l-motor-with-3611-propeller-combo/) | 110 | 12–14S | 24 kg | 7–12 kg | 1532 g | 40 mm |
| [Hobbywing X9 Plus G2L + 4314 prop](https://bharatskytech.com/product/hobbywing-x9-plus-g2l-motor-with-4314-propeller-combo/) | 80 | 12–14S | 28 kg | 12–14 kg | 1852 g | 45 mm |

### What each power system suits, by frame layout

This is calculated as recommended TOW per axis × number of motors.

| Power system | Quad (4) | Hex (6) | Octo (8) | Typical tank class |
|---|---|---|---|---|
| X6 Plus | 14–22 kg | 21–33 kg | 28–44 kg | 10L hex |
| X9 G2L 3611 | 28–48 kg | 42–72 kg | — | 16L quad |
| X9 Plus G2L 4314 | 48–56 kg | 72–84 kg | — | 20–30L quad |

### Battery

| Battery | Config | Capacity | Energy | Discharge | Weight | Connector |
|---|---|---|---|---|---|---|
| [Evercell 6S 22000mAh LiPo](https://bharatskytech.com/product/evercell-6s-22-2v-22000mah-25c-lipo-battery-for-drone/) (Make in India) | 6S 22.2 V | 22000 mAh | 488.4 Wh | 10C cont. / 25C pulse | 2.55 kg | XT90 / AS150 |

Wiring **two 6S packs in series** gives the 12S (44.4 V) bus that the Hobbywing X-series systems above need.

### Frame

| Frame | Wheelbase | Props | Max takeoff weight | Weight |
|---|---|---|---|---|
| [EFT X950 industrial frame](https://bharatskytech.com/product/x950-drone-frame/) | 950 mm | 23 in | 10 kg | 3.9 kg |

---

## Further reading

- [Drone Motor KV Rating Explained: Choosing KV and Thrust Class for 10L–30L Agriculture Drones](https://bharatskytech.com/drone-motor-kv-rating-explained-choosing-kv-and-thrust-class-for-10l-to-30l-agriculture-drones/)
- [22000mAh Battery: How to Match It With Your Drone Motor](https://bharatskytech.com/22000mah-battery-how-to-match-it-with-your-drone-motor/)
- [Agriculture Drone Power System Explained (2026 Guide)](https://bharatskytech.com/agriculture-drone-power-system-explained-2026-guide/)
- [How to Choose the Right Propeller Size for Your Agriculture Drone](https://bharatskytech.com/how-to-choose-the-right-propeller-size-for-your-agriculture-drone-in-india/)
- [Hobbywing X9 Plus vs X11 Plus](https://bharatskytech.com/hobbywing-x9-plus-vs-x11-plus-which-motor-delivers-better-performance-for-agriculture-drones/)

## Contributing

PRs are welcome, especially:

- measured hover-current logs from real builds (these help calibrate the estimates)
- data for more motors (T-Motor, X11, X13), batteries and frames
- translations of this README into Hindi, Marathi, Telugu or Tamil

## License

MIT. Use it, fork it, and teach with it.

---

<sub>Component questions? Contact [Bharat Skytech](https://bharatskytech.com/) · info@bharatskytech.com · +91 62613 13136</sub>
