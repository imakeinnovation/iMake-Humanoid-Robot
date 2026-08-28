# Developer status report — iMake Humanoid Robot workspace

**Date:** 2026-08-28  
**Branch:** `ubuntu`  
**Repos:** [imakeinnovation/iMake-Humanoid-Robot](https://github.com/imakeinnovation/iMake-Humanoid-Robot)

Plain-language overview of the **whole monorepo** and where lab work stands.
Real-robot detail lives in the low-level submodule docs.


## One-sentence bottom line

The workspace can train/sim policies and (now) talk to SocketCAN motors from
the robot PC — but the **physical biped is not walkable**. Only one Recoil
actuator has answered ping. Keep Isaac / sim work separate from unfinished
hardware bring-up.


## Repository layout

| Piece | Path | Role | Runs on |
| --- | --- | --- | --- |
| Isaac Lab tasks | `source/imake_humanoid_robot/` | Training / sim environments | Dev / GPU machine |
| Assets | `source/imake_humanoid_robot_assets/` | URDF / MJCF / USD models | Sim + tooling |
| Low-level | `source/imake_humanoid_robot_lowlevel/` | CAN, Recoil, gamepad, policy on hardware | **Robot PC** |

Assets and low-level are **git submodules**:

- Assets → [iMake-Humanoid-Robot-Assets](https://github.com/imakeinnovation/iMake-Humanoid-Robot-Assets)
- Low-level → [iMake-Humanoid-Robot-Lowlevel](https://github.com/imakeinnovation/iMake-Humanoid-Robot-Lowlevel)

Only the low-level tree is required to deploy to the real robot.


## Git / release state

| Item | State |
| --- | --- |
| Active lab branch | **`ubuntu`** (synced with `origin/ubuntu`) |
| Parent PR | [#2](https://github.com/imakeinnovation/iMake-Humanoid-Robot/pull/2) — lowlevel submodule bump (merged) |
| Lowlevel PR | [#2](https://github.com/imakeinnovation/iMake-Humanoid-Robot-Lowlevel/pull/2) — lab Recoil bring-up (merged) |
| Other branch | `ubuntu-simrat` — earlier gamepad work; bring-up tree has its own gamepad fixes |
| `main` | Default on GitHub; diverged from `ubuntu`. Treat **`ubuntu` as lab source of truth** for now |

Clone with submodules:

```bash
git clone https://github.com/imakeinnovation/iMake-Humanoid-Robot.git
cd iMake-Humanoid-Robot
git checkout ubuntu
git submodule update --init --recursive
```


## What recently landed (lab bring-up)

Merged 2026-08-28 into `ubuntu` on both parent and low-level:

- Ubuntu 24-friendly Python path (apt `python3-can` / numpy; no broken system pip)
- Safer CAN bring-up scripts and clearer SocketCAN error messages
- Bench tools: ping wrappers, ID scan, electrical offset, jog-around-encoder,
  phase-order helper, actuator connection test
- Gamepad stick calibration for Linux 8-bit pads
- Operator docs in low-level: `docs/STATUS.md`, `docs/BRINGUP.md`

Full low-level report:  
[source/imake_humanoid_robot_lowlevel/docs/DEVELOPER_REPORT.md](../source/imake_humanoid_robot_lowlevel/docs/DEVELOPER_REPORT.md)


## Hardware gate (do not skip)

| Working | Not ready |
| --- | --- |
| SocketCAN software stack | Rest of biped (most IDs offline last scan) |
| One Recoil: **can1 id 3** online | USB-CAN names unstable after unplug/replug |
| Electrical offset *ran* on that motor | First spin was wrong direction (CW then CCW) |
| | `Humanoid()`, joint zeros, IMU stack, RL on hardware |

**Safety:** do not start full robot control until about **12** biped actuators
ping on **can0** (left) and **can1** (right).

Intended ID map and ordered next steps are in the [low-level developer
report](../source/imake_humanoid_robot_lowlevel/docs/DEVELOPER_REPORT.md) and
[STATUS.md](../source/imake_humanoid_robot_lowlevel/docs/STATUS.md).


## Simulation / training side

Top-level `scripts/` still holds Isaac Lab entry points (`rsl_rl`, sim2sim,
sim2real, teleop). That path was **not** the focus of the Aug 27 hardware
session. Day-to-day **robot** progress is gated by low-level CAN bring-up, not
by missing Isaac code.


## Do not change yet (hardware phase)

- Recoil ping payload `0xCA`
- Actuator IDs / joint order
- RL gains inside `Humanoid()`
- IMU transforms

Fix wiring and commutation direction first. See low-level BRINGUP.md before
swapping motor phase wires or reflashing Recoil.


## Doc map

| Doc | Repo | Purpose |
| --- | --- | --- |
| This file | Parent | Monorepo + git overview |
| [lowlevel DEVELOPER_REPORT.md](../source/imake_humanoid_robot_lowlevel/docs/DEVELOPER_REPORT.md) | Lowlevel submodule | Architecture + lab status |
| [STATUS.md](../source/imake_humanoid_robot_lowlevel/docs/STATUS.md) | Lowlevel | 2026-08-27 status snapshot |
| [BRINGUP.md](../source/imake_humanoid_robot_lowlevel/docs/BRINGUP.md) | Lowlevel | Commands + error catalog |
| [README.md](../README.md) | Parent | Project intro |
| [lowlevel README.md](../source/imake_humanoid_robot_lowlevel/README.md) | Lowlevel | Robot-PC install + workflow |
