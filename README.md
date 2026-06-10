# Lab 04b - Robot Architecture - ROS

Turtlebot3-basierte ROS-Applikation mit autonomer Steuerung, Kameraverarbeitung, Custom Messages, Logging und Services.

## Voraussetzungen

- Ubuntu 20.04
- ROS Noetic
- Turtlebot3 Packages (Source-Installation)
- OpenCV: `sudo apt-get install -y ros-noetic-cv-bridge python3-opencv`

## Build

```bash
cd ~/catkin_ws && catkin_make && source devel/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
```

## Starten

**Wall Follower:**
```bash
roslaunch lab4 wall_follower.launch
```

**Move Between Objects:**
```bash
roslaunch lab4 move_between_objects.launch
```

## Logging ein-/ausschalten

```bash
rosservice call /toggle_logging "enable: false"
rosservice call /toggle_logging "enable: true"
```

## Package-Struktur
lab4/
├── CMakeLists.txt
├── package.xml
├── README.md
├── msg/
│   └── RobotStatus.msg
├── srv/
│   └── ToggleLogging.srv
├── scripts/
│   ├── camera_node.py
│   ├── status_publisher.py
│   ├── logger.py
│   ├── wall_follower.py
│   └── move_between_objects.py
├── launch/
│   ├── wall_follower.launch
│   └── move_between_objects.launch
├── worlds/
│   └── two_objects.world
└── logs/

## Knoten

| Knoten | Beschreibung |
|---|---|
| camera_node | Kamerabild via cv_bridge, Kantendetektion mit OpenCV |
| status_publisher | Publiziert RobotStatus (Geschwindigkeit + LiDAR-Abstände) |
| logger | Schreibt RobotStatus mit Timestamp in CSV |
| wall_follower | Regelbasierte Wandverfolgung via LiDAR |
| move_between_objects | Fährt zwischen zwei Objekten hin und her |
