"""
MTConnect Component Models

Component hierarchy representing the physical and logical organization of 
manufacturing equipment in the MTConnect device information model.

Reference: MTConnect Standard v2.6 - Device Information Model
"""

from dataclasses import dataclass, field
from typing import Optional, List
from mtconnect.types.primitives import ID, UUID


@dataclass
class Component:
    """
    Base class for all MTConnect components.
    
    Components represent functional sub-units of a Device, organized in a 
    hierarchical structure that models the physical and logical organization
    of manufacturing equipment.
    
    Reference: https://model.mtconnect.org/#Package__EAPK_7E9F9609_E982_40e1_88EC_28890F7ECF79
    """
    id: ID
    name: str
    uuid: Optional[UUID] = None
    native_name: Optional[str] = None
    sample_interval: Optional[float] = None
    sample_rate: Optional[float] = None
    components: List['Component'] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate component after initialization"""
        if not isinstance(self.id, (ID, str)):
            raise TypeError(f"Component id must be ID or str, got {type(self.id)}")
        if isinstance(self.id, str):
            self.id = ID(self.id)
        
        if self.uuid and isinstance(self.uuid, str):
            self.uuid = UUID(self.uuid)


@dataclass
class Description:
    """
    Descriptive information about a piece of equipment.
    
    Provides manufacturer, model, serial number, and other identifying 
    information for a Device.
    """
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial_number: Optional[str] = None
    station: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Device(Component):
    """
    Top-level Component representing a piece of equipment.
    
    A Device is a Component that organizes all information for a single piece
    of manufacturing equipment. It represents the root of the component hierarchy
    and contains Axes, Controllers, Systems, and other sub-components.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1623082330438_892066_4246
    """
    description: Optional[Description] = None
    iso_841_class: Optional[str] = None
    mtconnect_version: str = "2.6.0"
    
    def add_component(self, component: 'Component') -> None:
        """Add a child component to this device"""
        self.components.append(component)


@dataclass
class Controller(Component):
    """
    Component that provides regulation or management of other components.
    
    The Controller component manages program execution, operating modes, and 
    coordination of machine functions. It typically contains DataItems for
    EXECUTION, CONTROLLER_MODE, PROGRAM, and other control-related observatio ns.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799456819_785370_14052
    """
    pass


@dataclass
class Axes(Component):
    """
    Logical or physical grouping of Linear and Rotary axis components.
    
    The Axes component acts as an organizational element that contains the
    individual axis components (Linear and Rotary) for a piece of equipment.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799316063_857872_13803
    """
    pass


@dataclass
class Linear(Component):
    """
    Linear axis component providing prismatic motion.
    
    Represents a linear axis of motion (typically X, Y, Z, U, V, W) that provides
    straight-line travel. Contains DataItems for POSITION, VELOCITY, LOAD, and
    other linear motion measurements.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799506195_652120_14283
    """
    pass


@dataclass
class Rotary(Component):
    """
    Rotary axis component providing angular motion.
    
    Represents a rotary axis of motion (typically A, B, C) that provides  
    rotational travel about an axis. Contains DataItems for ANGLE, ROTARY_VELOCITY,
    LOAD, and other rotary motion measurements.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799548115_711880_14514
    """
    pass


@dataclass
class Spindle(Component):
    """
    Rotary axis with a tool or workpiece interface.
    
    A Spindle is a rotary axis that holds and rotates a cutting tool or workpiece.
    It contains DataItems for ROTARY_VELOCITY (spindle speed), LOAD, and other
    spindle-specific measurements.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799597139_486662_14745
    """
    pass


@dataclass
class Path(Component):
    """
    Independent operation of a Controller.
    
    For multi-path machines (e.g., multi-tasking lathes), each Path represents
    an independent channel of execution with its own coordinate system, program,
    and control state.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799470571_344459_14052
    """
    pass


@dataclass
class Systems(Component):
    """
    Organizational component for supporting system sub-components.
    
    The Systems component groups related supporting systems such as Coolant,
    Electric, Hydraulic, Pneumatic, and Lubrication systems.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799651906_519301_14976
    """
    pass


@dataclass
class Coolant(Component):
    """
    Component representing the coolant system.
    
    Delivers coolant to the cutting zone for chip removal and temperature control.
    Contains DataItems for flow rate, pressure, concentration, and temperature.
    """
    pass


@dataclass
class Electric(Component):
    """
    Component representing the electrical system.
    
    Provides and monitors electrical power distribution. Contains DataItems for
    voltage, amperage, frequency, and power consumption.
    """
    pass


@dataclass
class Hydraulic(Component):
    """
    Component representing the hydraulic system.
    
    Provides hydraulic power and actuation. Contains DataItems for pressure,
    flow rate, and temperature.
    """
    pass


@dataclass
class Pneumatic(Component):
    """
    Component representing the pneumatic system.
    
    Provides compressed air for pneumatic actuation. Contains DataItems for
    pressure and flow rate.
    """
    pass


@dataclass
class Lubrication(Component):
    """
    Component representing the lubrication system.
    
    Delivers lubricant to reduce friction and wear. Contains DataItems for
    flow rate, pressure, and level.
    """
    pass


@dataclass
class Door(Component):
    """
    Component representing a mechanical mechanism for access to equipment interior.
    
    Provides information about the state (OPEN, CLOSED, UNLATCHED) and interlock
    status of access doors and guards.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622799375331_100374_14034
    """
    pass


@dataclass
class Chuck(Component):
    """
    Component representing a mechanism that holds a part or workpiece.
    
    A Chuck is a work holding device that grips the workpiece during machining.
    Contains DataItems for CHUCK_STATE (OPEN, CLOSED, UNLATCHED) and clamping
    status.
    
    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1622798925923_459673_13555
    """
    pass


@dataclass
class Auxiliaries(Component):
    """
    Organizational component for auxiliary equipment components.
    
    Groups auxiliary devices such as bar feeders, part catchers, tool changers,
    and other peripheral equipment.
    """
    pass
