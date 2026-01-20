from dataclasses import dataclass


@dataclass
class MotionConfig:
    min_area: int = 500
    aspect_ratio_thresh: float = 1.2
    check_period: int = 5


@dataclass
class HumanConfig:
    conf_threshold: float = 0.5
    fps_skip: int = 5


@dataclass
class AlertConfig:
    cooldown_seconds: int = 300


@dataclass
class DisplayConfig:
    frame_size: tuple = (320, 240)


@dataclass
class AppConfig:
    motion: MotionConfig = MotionConfig()
    human: HumanConfig = HumanConfig()
    alert: AlertConfig = AlertConfig()
    display: DisplayConfig = DisplayConfig()
