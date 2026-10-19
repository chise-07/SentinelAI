
from enum import Enum


class Sensitivity(str, Enum):
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"

from dataclasses import dataclass


@dataclass
class DataAsset:
    name: str
    sensitivity: Sensitivity
    description: str = ""

@dataclass
class WorkflowStep:
    step_id: str
    name: str
    description: str = ""

@dataclass
class Destination:
    destination_id: str
    name: str
    approved: bool = False
    description: str = ""

@dataclass
class DataFlow:
    source_id: str
    target_id: str
    asset_name: str
@dataclass
class Finding:
    asset_name: str
    destination_name: str
    severity: str
    message: str