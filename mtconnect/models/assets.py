"""
MTConnect Asset Models

Asset definitions representing lifecycle objects such as cutting tools, parts,
raw materials, and files that are tracked through the manufacturing process.

Reference: MTConnect Standard v2.6 - Asset Information Model
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import Enum

from mtconnect.types.primitives import ID, UUID, MTCDateTime


class AssetType(Enum):
    """Standard MTConnect asset types"""
    CUTTING_TOOL = "CuttingTool"
    PART = "Part"
    RAW_MATERIAL = "RawMaterial"
    QIF_DOCUMENT_WRAPPER = "QIFDocumentWrapper"
    FILE = "File"


@dataclass
class Asset:
    """
    Base class for all MTConnect assets.
    
    An Asset represents a lifecycle object that moves through the manufacturing
    process and can be associated with multiple devices over time. Assets have
    unique identifiers and track their status, location, and history.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622798866752_358680_13276
    """
    asset_id: ID
    timestamp: MTCDateTime
    device_uuid: Optional[UUID] = None
    removed: bool = False
    description: Optional[str] = None
    
    def __post_init__(self):
        """Validate asset after initialization"""
        if not isinstance(self.asset_id, (ID, str)):
            raise TypeError(f"Asset asset_id must be ID or str")
        if isinstance(self.asset_id, str):
            self.asset_id = ID(self.asset_id)
        
        if self.device_uuid and isinstance(self.device_uuid, str):
            self.device_uuid = UUID(self.device_uuid)
        
        if isinstance(self.timestamp, str):
            self.timestamp = MTCDateTime(self.timestamp)


class ToolLifeType(Enum):
    """Types of tool life measurement"""
    MINUTES = "MINUTES"
    PART_COUNT = "PART_COUNT"
    WEAR = "WEAR"
    CYCLES = "CYCLES"


class ToolLifeDirection(Enum):
    """Direction of tool life counting"""
    UP = "UP"  # Count up from zero
    DOWN = "DOWN"  # Count down from maximum


class CutterStatus(Enum):
    """Status values for cutting tools"""
    NEW = "NEW"
    AVAILABLE = "AVAILABLE"
    UNAVAILABLE = "UNAVAILABLE"
    ALLOCATED = "ALLOCATED"
    UNALLOCATED = "UNALLOCATED"
    MEASURED = "MEASURED"
    RECONDITIONED = "RECONDITIONED"
    USED = "USED"
    EXPIRED = "EXPIRED"
    BROKEN = "BROKEN"
    NOT_REGISTERED = "NOT_REGISTERED"
    UNKNOWN = "UNKNOWN"


@dataclass
class ToolLife:
    """
    Tool life tracking for a cutting tool.
    
    Tracks remaining or accumulated tool life based on time, part count,
    or wear measurements.
    """
    type: ToolLifeType
    value: float
    count_direction: ToolLifeDirection = ToolLifeDirection.UP
    warning: Optional[float] = None
    limit: Optional[float] = None
    initial: Optional[float] = None


@dataclass
class Location:
    """
    Physical location of a tool or part.
    
    Specifies where an asset is located, such as pot number in a tool magazine,
    spindle number, or staging area.
    """
    type: str  # POT, SPINDLE, STATION, CRIB
    value: str  # Location identifier (pot number, spindle ID, etc.)
    negative_overlap: Optional[int] = None
    positive_overlap: Optional[int] = None
    turret_id: Optional[str] = None


@dataclass
class Measurement:
    """
    Physical measurement of a tool dimension.
    
    Records critical dimensions such as cutting diameter, functional length,
    overall length, etc.
    """
    code: str  # Measurement type code (e.g., "BDX" for body diameter, "LF" for functional length)
    value: float
    units: str  # MILLIMETER, INCH
    name: Optional[str] = None
    native_units: Optional[str] = None
    significant_digits: Optional[int] = None
    minimum: Optional[float] = None
    maximum: Optional[float] = None
    nominal: Optional[float] = None


@dataclass
class CuttingToolLifeCycle:
    """
    Lifecycle tracking for a cutting tool.
    
    Manages the complete lifecycle of a cutting tool including measurements,
    location, tool life, and status throughout its use in manufacturing.
    """
    tool_life: Optional[ToolLife] = None
    location: Optional[Location] = None
    program_tool_number: Optional[str] = None
    program_tool_group: Optional[str] = None
    connection_code_machine_side: Optional[str] = None
    measurements: List[Measurement] = field(default_factory=list)
    cutter_status: Optional[CutterStatus] = None
    recondition_count: int = 0
    process_spindle_speed: Optional[float] = None
    process_feed_rate: Optional[float] = None


@dataclass
class CuttingTool(Asset):
    """
    Cutting tool asset with lifecycle tracking.
    
    Represents a cutting tool assembly including the tool holder and cutting
    inserts. Tracks tool life, location in tool magazine, measurements, and
    usage history.
    
    Example: End mill, drill, turning insert, boring bar
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622798982811_591134_13786
    """
    serial_number: Optional[str] = None
    tool_id: Optional[str] = None
    manufacturers: Optional[List[str]] = None
    cutting_tool_lifecycle: Optional[CuttingToolLifeCycle] = None
    
    def is_expired(self) -> bool:
        """Check if tool has exceeded its life limit"""
        if not self.cutting_tool_lifecycle or not self.cutting_tool_lifecycle.tool_life:
            return False
        
        life = self.cutting_tool_lifecycle.tool_life
        if life.limit is None:
            return False
        
        if life.count_direction == ToolLifeDirection.DOWN:
            return life.value <= 0
        else:  # UP
            return life.value >= life.limit
    
    def remaining_life_percent(self) -> Optional[float]:
        """Calculate remaining tool life as percentage"""
        if not self.cutting_tool_lifecycle or not self.cutting_tool_lifecycle.tool_life:
            return None
        
        life = self.cutting_tool_lifecycle.tool_life
        if life.limit is None or life.initial is None:
            return None
        
        if life.count_direction == ToolLifeDirection.DOWN:
            return (life.value / life.initial) * 100.0
        else:  # UP
            used = life.value - (life.initial or 0)
            return ((life.limit - used) / life.limit) * 100.0


class PartStatus(Enum):
    """Manufacturing status of a part"""
    COMPLETE = "COMPLETE"
    INCOMPLETE = "INCOMPLETE"
    PASS = "PASS"
    FAIL = "FAIL"
    SCRAPPED = "SCRAPPED"
    IN_PROCESS = "IN_PROCESS"
    WAITING = "WAITING"


@dataclass
class Part(Asset):
    """
    Workpiece or part asset.
    
    Represents a part being manufactured, including its identification,
    status, and manufacturing history.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799219188_31823_13555
    """
    name: Optional[str] = None
    part_number: Optional[str] = None
    serial_number: Optional[str] = None
    lot_id: Optional[str] = None
    part_status: Optional[PartStatus] = None
    manufacturing_date: Optional[datetime] = None
    first_use_date: Optional[datetime] = None


class MaterialType(Enum):
    """Types of raw material forms"""
    BAR = "BAR"
    BLOCK = "BLOCK"
    CASTING = "CASTING"
    FORGING = "FORGING"
    GEL = "GEL"
    LIQUID = "LIQUID"
    POWDER = "POWDER"
    SHEET = "SHEET"
    TUBE = "TUBE"


@dataclass
class RawMaterial(Asset):
    """
    Raw material stock asset.
    
    Represents raw material inventory such as bar stock, sheet metal, castings,
    or other stock forms used in manufacturing.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799264259_946346_13786
    """
    name: Optional[str] = None
    material_type: Optional[MaterialType] = None
    container_id: Optional[str] = None
    lot_id: Optional[str] = None
    manufacturer_lot_id: Optional[str] = None
    material: Optional[str] = None  # Material specification (e.g., "6061-T6 Aluminum")
    manufacturing_date: Optional[datetime] = None
    first_use_date: Optional[datetime] = None


class FileState(Enum):
    """State of a file asset"""
    EXPERIMENTAL = "EXPERIMENTAL"
    REVISION = "REVISION"
    PRODUCTION = "PRODUCTION"


@dataclass
class File(Asset):
    """
    File asset representing NC programs, documentation, or media.
    
    Tracks files associated with manufacturing operations including NC programs,
    setup sheets, inspection reports, and other documents.
    """
    name: Optional[str] = None
    media_type: Optional[str] = None  # MIME type
    application_category: Optional[str] = None
    application_type: Optional[str] = None
    size: Optional[int] = None  # Size in bytes
    version_id: Optional[str] = None
    state: Optional[FileState] = None
    file_location: Optional[str] = None  # URL or path
    file_name: Optional[str] = None
    creation_time: Optional[datetime] = None
    modification_time: Optional[datetime] = None


@dataclass
class QIFDocumentWrapper(Asset):
    """
    Quality Information Framework (QIF) document wrapper.
    
    Contains quality inspection and measurement data in QIF format,
    providing dimensional inspection results and statistical process control data.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799309508_449823_14014
    """
    qif_document_type: Optional[str] = None  # MeasurementsResults, Plan, ProductDefinition, etc.
    qif_document: Optional[str] = None  # XML content of QIF document
