"""
MTConnect Component Models

Component hierarchy representing the physical and logical organization of
manufacturing equipment in the MTConnect device information model.

Reference: MTConnect Standard v2.6 Normative Model
Auto-generated from: model_2.6.xml
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Optional, List

from mtconnect.models.configurations import Configuration
from mtconnect.types.primitives import ID, UUID

if TYPE_CHECKING:
    from mtconnect.models.data_items import (
        DataItem,
        AxisFeedrate, CharacteristicPersistentId, CharacteristicStatus, Communications, Concentration,
        ControllerMode, Device, DoorState, EmergencyStop, Execution,
        FeatureMeasurement, FeaturePersisitentId, InterfaceState, Length, Load,
        LockState, LogicProgram, MeasurementType, MeasurementUnits, MeasurementValue,
        PartCount, PartGroupId, PartId, PartKindId, PartStatus,
        PartUniqueId, PathFeedrate, PathFeedrateOverride, ProcessAggregateId, ProcessKindId,
        ProcessOccurrenceId, ProcessTime, Program, RotaryVelocity, RotaryVelocityOverride,
        Temperature, Uncertainty, UncertaintyType, User, Wattage
    )


@dataclass
class Description:
    """
    Descriptive information about a piece of equipment.

    Provides manufacturer, model, serial number, and other identifying
    information for a Device.
    """
    manufacturer: str | None = None
    model: str | None = None
    serial_number: str | None = None
    station: str | None = None
    description: str | None = None



@dataclass
class ComponentBase:
    """
    Base class for all MTConnect components.

    Components represent functional sub-units of a Device, organized in a
    hierarchical structure that models the physical and logical organization
    of manufacturing equipment.

    Reference: https://model.mtconnect.org/#Package__EAPK_7E9F9609_E982_40e1_88EC_28890F7ECF79
    """
    id: ID
    name: str
    uuid: UUID | None = None
    native_name: str | None = None
    sample_interval: float | None = None
    sample_rate: float | None = None
    description: Description | None = None
    configuration: Configuration | None = None
    data_items: list[DataItem] = field(default_factory=list)

    def __post_init__(self):
        """Validate component after initialization"""
        if not isinstance(self.id, (ID, str)):
            msg = f"Component id must be ID or str, got {type(self.id)}"
            raise TypeError(msg)
        if isinstance(self.id, str):
            self.id = ID(self.id)

        if self.uuid and isinstance(self.uuid, str):
            self.uuid = UUID(self.uuid)



@dataclass
class Component(ComponentBase):
    """
    Component with child component support.
    
    Non-leaf components can contain other components in a hierarchical structure.
    Leaf components do not have this field.
    """
    components: list[Component] = field(default_factory=list)



@dataclass
class Device(Component):
    """
    Top-level Component representing a piece of equipment.

    A Device is a Component that organizes all information for a single piece
    of manufacturing equipment. It represents the root of the component hierarchy
    and contains Axes, Controllers, Systems, and other sub-components.

    Reference: https://model.mtconnect.org/#Package___19_0_3_68e0225_1623082330438_892066_4246
    """
    iso_841_class: str | None = None
    mtconnect_version: str = "2.6.0"

    def add_component(self, component: Component) -> None:
        """Add a child component to this device"""
        self.components.append(component)

    def add_data_item(self, data_item: DataItem) -> None:
        """Add a data item to this device"""
        self.data_items.append(data_item)



@dataclass
class Adapter(Component):
    """Component that provides information about the data source for an MTConnect Agent.
    """
    is_adapter_of: 'Device' = None


@dataclass
class Adapters(Component):
    """Organizer that groups Adapter components."""
    adapters: list[Adapter] = field(default_factory=list)


@dataclass
class Agent(Device):
    """Device composed of an MTConnect Agent and all its connected data sources.
    """
    pass


@dataclass
class Amplifier(ComponentBase):
    """leaf Component composed of an electronic component or circuit that amplifies power, ele...
    """
    pass


@dataclass
class Auxiliaries(Component):
    """Organizer that groups Auxiliary components."""
    auxiliaries: list[Auxiliary] = field(default_factory=list)


@dataclass
class Auxiliary(Component):
    """abstract Component composed of removable part(s) of a piece of equipment that provides ...
    """
    is_auxiliary_of: 'Device' = None


@dataclass
class CuttingTorch(Auxiliary):
    """Auxiliary that employs a concentrated flame to both sever materials through cutting and...
    """
    pass


@dataclass
class Deposition(Auxiliary):
    """Auxiliary that manages the addition of material or state change of material being perfo...
    """
    pass


@dataclass
class Electrode(Auxiliary):
    """Auxiliary that is used for many electrical discharge manufacturing processes like welding.
    """
    pass


@dataclass
class Loader(Auxiliary):
    """Auxiliary that provides movement and distribution of materials, parts, tooling, and oth...
    """
    pass


@dataclass
class BarFeeder(Loader):
    """Loader that delivers bar stock to a piece of equipment.
    """
    pass


@dataclass
class ToolingDelivery(Auxiliary):
    """Auxiliary that manages, positions, stores, and delivers tooling within a piece of equip...
    """
    pass


@dataclass
class AutomaticToolChanger(ToolingDelivery):
    """ToolingDelivery composed of a tool delivery mechanism that moves tools between a ToolMa...
    """
    pass


@dataclass
class GangToolBar(ToolingDelivery):
    """ToolingDelivery composed of a tool mounting mechanism that holds any number of tools.
    """
    pass


@dataclass
class ToolMagazine(ToolingDelivery):
    """ToolingDelivery composed of a tool storage mechanism that holds any number of tools.
    """
    pass


@dataclass
class ToolRack(ToolingDelivery):
    """ToolingDelivery composed of a linear or matrixed tool storage mechanism that holds any ...
    """
    pass


@dataclass
class Turret(ToolingDelivery):
    """ToolingDelivery composed of a tool mounting mechanism that holds any number of tools.
    """
    pass


@dataclass
class WasteDisposal(Auxiliary):
    """Auxiliary that removes manufacturing byproducts from a piece of equipment.
    """
    pass


@dataclass
class Axes(Component):
    """Organizer that groups Axis components."""
    axes: list[Axis] = field(default_factory=list)


@dataclass
class Axis(Component):
    """abstract Component composed of a motion system that provides linear or rotational motio...
    """
    is_axis_of: 'Device' = None


@dataclass
class Linear(Axis):
    """Component Types::Axis that provides prismatic motion along a fixed axis.

    MTConnect Relationships:
    - observesLoad [0..1]
    - observesTemperature [0..1]
    - observesAxisFeedrateActual [0..1]
    """
    load: Optional['Load'] = None
    temperature: Optional['Temperature'] = None
    axis_feedrate_actual: Optional['AxisFeedrate.Actual'] = None


@dataclass
class Rotary(Axis):
    """Component Types::Axis that provides rotation about a fixed axis.

    MTConnect Relationships:
    - observesLoad [0..1]
    - observesTemperature [0..1]
    - observesRotaryVelocity [0..1]
    - observesAxisFeedrate [0..1]
    """
    load: Optional['Load'] = None
    temperature: Optional['Temperature'] = None
    rotary_velocity: Optional['RotaryVelocity'] = None
    axis_feedrate: Optional['AxisFeedrate'] = None


@dataclass
class Spindle(Axis):
    """Component that provides an axis of rotation for the purpose of rapidly rotating a part ...
    """
    pass


@dataclass
class Ballscrew(ComponentBase):
    """leaf Component composed of a mechanical structure that transforms rotary motion into li...
    """
    pass


@dataclass
class Belt(ComponentBase):
    """leaf Component composed of an endless flexible band that transmits motion for a piece o...
    """
    pass


@dataclass
class Brake(ComponentBase):
    """leaf Component that slows or stops a moving object by the absorption or transfer of the...
    """
    pass


@dataclass
class Chain(ComponentBase):
    """leaf Component composed of interconnected series of objects that band together and are ...
    """
    pass


@dataclass
class Chopper(ComponentBase):
    """leaf Component that breaks material into smaller pieces.
    """
    pass


@dataclass
class Chuck(ComponentBase):
    """leaf Component composed of a mechanism that holds a part or stock material in place.
    """
    pass


@dataclass
class Chute(ComponentBase):
    """leaf Component composed of an inclined channel that conveys material.
    """
    pass


@dataclass
class CircuitBreaker(ComponentBase):
    """leaf Component that interrupts an electric circuit.
    """
    pass


@dataclass
class Clamp(ComponentBase):
    """leaf Component that strengthens, support, or fastens objects in place.
    """
    pass


@dataclass
class Composition(Component):
    """Component belonging to a Component and not composed of any Component.
    """
    belongs_to: 'Component' = None


@dataclass
class Compressor(ComponentBase):
    """leaf Component composed of a pump or other mechanism that reduces volume and increases ...
    """
    pass


@dataclass
class Controllers(Component):
    """Organizer that groups Controller components."""
    controllers: list[Controller] = field(default_factory=list)


@dataclass
class CoolingTower(ComponentBase):
    """leaf Component composed of a heat exchange system that uses a fluid to transfer heat to...
    """
    pass


@dataclass
class Door(Component):
    """Component composed of a mechanical mechanism or closure that can cover a physical acces...

    MTConnect Relationships:
    - observesDoorState [1..1]
    """
    door_state: 'DoorState' = None

    def __post_init__(self):
        if self.door_state is None:
            raise ValueError("observesDoorState: required relationship [1..1] cannot be None")
        super().__post_init__()


@dataclass
class Drain(ComponentBase):
    """leaf Component that allows material to flow for the purpose of drainage from, for examp...
    """
    pass


@dataclass
class Encoder(ComponentBase):
    """leaf Component that measures position.
    """
    pass


@dataclass
class Environmental(Component):
    """Component that observes the surroundings of another Component.
    """
    pass


@dataclass
class ExpiredPot(ComponentBase):
    """leaf Component that is a Pot for a tool that is no longer usable for removal from a Too...
    """
    pass


@dataclass
class ExposureUnit(ComponentBase):
    """leaf Component that emits a type of radiation.
    """
    pass


@dataclass
class ExtrusionUnit(ComponentBase):
    """leaf Component that dispenses liquid or powered materials.
    """
    pass


@dataclass
class Fan(ComponentBase):
    """leaf Component that produces a current of air.
    """
    pass


@dataclass
class Filter(ComponentBase):
    """leaf Component through which liquids or gases are passed to remove suspended impurities...
    """
    pass


@dataclass
class Galvanomotor(ComponentBase):
    """leaf Component composed of an electromechanical actuator that produces deflection of a ...
    """
    pass


@dataclass
class Gripper(ComponentBase):
    """leaf Component that holds a part, stock material, or any other item in place.
    """
    pass


@dataclass
class Hopper(ComponentBase):
    """leaf Component composed of a chamber or bin in which materials are stored temporarily, ...
    """
    pass


@dataclass
class Interface(Component):
    """abstract Component that coordinates actions and activities between pieces of equipment.

    MTConnect Relationships:
    - observesInterfaceState [1..1]
    """
    is_interface_of: 'Device' = None
    interface_state: 'InterfaceState' = None

    def __post_init__(self):
        if self.interface_state is None:
            raise ValueError("observesInterfaceState: required relationship [1..1] cannot be None")
        super().__post_init__()


@dataclass
class BarFeederInterface(Interface):
    """Interface that coordinates the operations between a bar feeder and another piece of equ...
    """
    pass


@dataclass
class ChuckInterface(Interface):
    """Interface that coordinates the operations between two pieces of equipment, one of which...
    """
    pass


@dataclass
class DoorInterface(Interface):
    """Interface that coordinates the operations between two pieces of equipment, one of which...
    """
    pass


@dataclass
class MaterialHandlerInterface(Interface):
    """Interface that coordinates the operations between a piece of equipment and another asso...
    """
    pass


@dataclass
class Requester(Interface):
    """Requester component.
    """
    pass


@dataclass
class Responder(Interface):
    """Responder component.
    """
    pass


@dataclass
class Interfaces(Component):
    """Organizer that groups Interface components."""
    interfaces: list[Interface] = field(default_factory=list)


@dataclass
class LinearPositionFeedback(ComponentBase):
    """leaf Component that measures linear motion or position.
    """
    pass


@dataclass
class Lock(Component):
    """Component that physically prohibits a Device or Component from opening or operating.

    MTConnect Relationships:
    - observesLockState [0..1]
    """
    lock_state: Optional['LockState'] = None


@dataclass
class Materials(Component):
    """Organizer that groups Material components."""
    materials: list[Material] = field(default_factory=list)


@dataclass
class Motor(ComponentBase):
    """leaf Component that converts electrical, pneumatic, or hydraulic energy into mechanical...
    """
    pass


@dataclass
class Oil(ComponentBase):
    """leaf Component composed of a viscous liquid.
    """
    pass


@dataclass
class Part(Component):
    """abstract Component composed of a part being processed by a piece of equipment.
    """
    is_worked_on: 'Device' = None


@dataclass
class PartOccurrence(Part):
    """Part that exists at a specific place and time, such as a specific instance of a bracket...

    MTConnect Relationships:
    - observesPartId [1..1]
    - observesPartUniqueId [0..1]
    - observesPartGroupId [0..1]
    - observesPartKindId [0..1]
    - observesPartCount [0..1]
    - observesPartStatus [0..1]
    - observesProcessOccurrenceId [0..1]
    - observesProcessTime [0..1]
    - observesUser [0..1]
    """
    part_id: 'PartId' = None
    part_unique_id: Optional['PartUniqueId'] = None
    part_group_id: Optional['PartGroupId'] = None
    part_kind_id: Optional['PartKindId'] = None
    part_count: Optional['PartCount'] = None
    part_status: Optional['PartStatus'] = None
    process_occurrence_id: Optional['ProcessOccurrenceId'] = None
    process_time: Optional['ProcessTime'] = None
    user: Optional['User'] = None

    def __post_init__(self):
        if self.part_id is None:
            raise ValueError("observesPartId: required relationship [1..1] cannot be None")
        super().__post_init__()


@dataclass
class FeatureOccurrence(PartOccurrence):
    """Component that provides information related to an individual feature.

    MTConnect Relationships:
    - observesFeaturePersisitentId [0..1]
    - observesFeatureMeasurement [0..1]
    - observesMeasurementType [0..1]
    - observesCharacteristicPersistentId [0..1]
    - observesCharacteristicStatus [0..1]
    - observesUncertainty [0..1]
    - observesUncertaintyType [0..1]
    - observesMeasurementUnits [0..1]
    - observesMeasurementValue [0..1]
    """
    feature_persisitent_id: Optional['FeaturePersisitentId'] = None
    feature_measurement: Optional['FeatureMeasurement'] = None
    measurement_type: Optional['MeasurementType'] = None
    characteristic_persistent_id: Optional['CharacteristicPersistentId'] = None
    characteristic_status: Optional['CharacteristicStatus'] = None
    uncertainty: Optional['Uncertainty'] = None
    uncertainty_type: Optional['UncertaintyType'] = None
    measurement_units: Optional['MeasurementUnits'] = None
    measurement_value: Optional['MeasurementValue'] = None


@dataclass
class Parts(Component):
    """Organizer that groups Part components."""
    parts: list[Part] = field(default_factory=list)


@dataclass
class Path(Component):
    """Component that organizes an independent operation or function within a Controller.

    MTConnect Relationships:
    - observesExecution [0..1]
    - observesProgram [0..1]
    - observesPathFeedrateOverrideProgrammed [0..1]
    - observesPathFeedrateOverrideRapid [0..1]
    - observesRotaryVelocityOverride [0..1]
    - observesPathFeedrate [0..1]
    - observesPartCount [0..1]
    """
    execution: Optional['Execution'] = None
    program: Optional['Program'] = None
    path_feedrate_override_programmed: Optional['PathFeedrateOverride.Programmed'] = None
    path_feedrate_override_rapid: Optional['PathFeedrateOverride.Rapid'] = None
    rotary_velocity_override: Optional['RotaryVelocityOverride'] = None
    path_feedrate: Optional['PathFeedrate'] = None
    part_count: Optional['PartCount'] = None


@dataclass
class Pot(ComponentBase):
    """leaf Component composed of a tool storage location associated with a ToolMagazine or Au...
    """
    pass


@dataclass
class PowerSupply(ComponentBase):
    """leaf Component that provides power to electric mechanisms.
    """
    pass


@dataclass
class Process(Component):
    """abstract Component composed of a manufacturing process being executed on a piece of equ...
    """
    is_executed_on: 'Device' = None


@dataclass
class ProcessOccurrence(Process):
    """Process that takes place at a specific place and time, such as a specific instance of p...

    MTConnect Relationships:
    - observesProcessOccurrenceId [1..1]
    - observesProcessAggregateId [0..1]
    - observesProcessTime [0..1]
    - observesProcessKindId [0..1]
    - observesUser [0..1]
    - observesProgram [0..1]
    - observesPartUniqueId [0..1]
    """
    process_occurrence_id: 'ProcessOccurrenceId' = None
    process_aggregate_id: Optional['ProcessAggregateId'] = None
    process_time: Optional['ProcessTime'] = None
    process_kind_id: Optional['ProcessKindId'] = None
    user: Optional['User'] = None
    program: Optional['Program'] = None
    part_unique_id: Optional['PartUniqueId'] = None

    def __post_init__(self):
        if self.process_occurrence_id is None:
            raise ValueError("observesProcessOccurrenceId: required relationship [1..1] cannot be None")
        super().__post_init__()


@dataclass
class Processes(Component):
    """Organizer that groups Process components."""
    processes: list[Process] = field(default_factory=list)


@dataclass
class Pulley(ComponentBase):
    """leaf Component composed of a mechanism or wheel that turns in a frame or block and serv...
    """
    pass


@dataclass
class Pump(ComponentBase):
    """leaf Component that raises, drives, exhausts, or compresses fluids or gases by means of...
    """
    pass


@dataclass
class Reel(ComponentBase):
    """leaf Component composed of a rotary storage unit for material.
    """
    pass


@dataclass
class RemovalPot(ComponentBase):
    """leaf Component that is a Pot for a tool that has to be removed from a ToolMagazine or T...
    """
    pass


@dataclass
class Resource(Component):
    """abstract Component composed of material or personnel involved in a manufacturing process.
    """
    is_resource_of: 'Device' = None


@dataclass
class Material(Resource):
    """Resource composed of material that is consumed or used by the piece of equipment for pr...
    """
    pass


@dataclass
class Stock(Material):
    """Material that is used in a manufacturing process and to which work is applied in a mach...

    MTConnect Relationships:
    - observesMaterial [0..1]
    - observesLengthRemaining [0..1]
    - observesLengthStandard [0..1]
    """
    material: Optional['Material'] = None
    length_remaining: Optional['Length.Remaining'] = None
    length_standard: Optional['Length.Standard'] = None


@dataclass
class Personnel(Resource):
    """Resource composed of an individual or individuals who either control, support, or other...

    MTConnect Relationships:
    - observesUserOperator [0..1]
    - observesUserMaintenance [0..1]
    """
    user_operator: Optional['User.Operator'] = None
    user_maintenance: Optional['User.Maintenance'] = None


@dataclass
class Resources(Component):
    """Organizer that groups Resource components."""
    resources: list[Resource] = field(default_factory=list)


@dataclass
class ReturnPot(ComponentBase):
    """leaf Component that is a Pot for a tool that has been removed from spindle or Turret an...
    """
    pass


@dataclass
class SensingElement(ComponentBase):
    """leaf Component that provides a signal or measured value.
    """
    pass


@dataclass
class Sensor(Component):
    """Component that responds to a physical stimulus and transmits a resulting impulse or val...
    """
    pass


@dataclass
class Spreader(ComponentBase):
    """leaf Component that flattens or spreading materials.
    """
    pass


@dataclass
class StagingPot(ComponentBase):
    """leaf Component that is a Pot for a tool that is awaiting transfer to a ToolMagazine or ...
    """
    pass


@dataclass
class Station(ComponentBase):
    """leaf Component composed of a storage or mounting location for a tool associated with a ...
    """
    pass


@dataclass
class StorageBattery(ComponentBase):
    """leaf Component composed of one or more cells in which chemical energy is converted into...
    """
    pass


@dataclass
class Structure(Component):
    """Component composed of part(s) comprising the rigid bodies of the piece of equipment.
    """
    is_structure_of: 'Device' = None


@dataclass
class Link(Structure):
    """Structure that provides a connection between Component entities.
    """
    pass


@dataclass
class Structures(Component):
    """Organizer that groups Structure components."""
    structures: list[Structure] = field(default_factory=list)


@dataclass
class Switch(ComponentBase):
    """leaf Component that turns on or off an electric current or makes or breaks a circuit.
    """
    pass


@dataclass
class System(Component):
    """abstract Component that is permanently integrated into the piece of equipment.
    """
    is_system_of: 'Device' = None


@dataclass
class Actuator(System):
    """Component composed of a physical apparatus that moves or controls a mechanism or system.
    """
    pass


@dataclass
class Hydraulic(Actuator):
    """System that provides movement and distribution of pressurized liquid throughout the pie...

    MTConnect Relationships:
    - observesPressure [0..1]
    """
    pressure: Optional['Pressure'] = None


@dataclass
class Pneumatic(Actuator):
    """System that uses compressed gasses to actuate components or do work within the piece of...

    MTConnect Relationships:
    - observesPressure [0..1]
    """
    pressure: Optional['Pressure'] = None


@dataclass
class AirHandler(System):
    """system that circulates air or regulates airflow without altering temperature or humidity.
    """
    pass


@dataclass
class Controller(System):
    """System that provides regulation or management of a system or component.

    MTConnect Relationships:
    - hasPath [0..*]
    - observesEmergencyStop [0..1]
    - observesSystemCondition [0..1]
    - observesControllerMode [0..1]
    - observesCommunicationsCondition [0..1]
    - observesLogicProgramCondition [0..1]
    """
    path: List['Path'] = field(default_factory=list)
    is_controller_of: 'Device' = None
    emergency_stop: Optional['EmergencyStop'] = None
    system_condition: Optional['System'] = None
    controller_mode: Optional['ControllerMode'] = None
    communications_condition: Optional['Communications'] = None
    logic_program_condition: Optional['LogicProgram'] = None


@dataclass
class Coolant(System):
    """System that provides distribution and management of fluids that remove heat from a piec...

    MTConnect Relationships:
    - observesConcentration [0..1]
    """
    concentration: Optional['Concentration'] = None


@dataclass
class Cooling(System):
    """System that extracts controlled amounts of heat to achieve a target temperature at a sp...
    """
    pass


@dataclass
class Dielectric(System):
    """System that manages a chemical mixture used in a manufacturing process being performed ...
    """
    pass


@dataclass
class Electric(System):
    """System composed of the main power supply for the piece of equipment that provides distr...

    MTConnect Relationships:
    - observesWattage [0..1]
    """
    wattage: Optional['Wattage'] = None


@dataclass
class Enclosure(System):
    """System composed of a structure that is used to contain or isolate a piece of equipment ...
    """
    pass


@dataclass
class EndEffector(System):
    """System composed of functions that form the last link segment of a piece of equipment.
    """
    pass


@dataclass
class Feeder(System):
    """System that manages the delivery of materials within a piece of equipment.
    """
    pass


@dataclass
class Heating(System):
    """System that delivers controlled amounts of heat to achieve a target temperature at a sp...
    """
    pass


@dataclass
class Lubrication(System):
    """System that provides distribution and management of fluids used to lubricate portions o...
    """
    pass


@dataclass
class Pressure(System):
    """System that delivers compressed gas or fluid and controls the pressure and rate of pres...
    """
    pass


@dataclass
class ProcessPower(System):
    """System composed of a power source associated with a piece of equipment that supplies en...
    """
    pass


@dataclass
class Protective(System):
    """System that provides functions used to detect or prevent harm or damage to equipment or...
    """
    pass


@dataclass
class Vacuum(System):
    """System that evacuates gases and liquids from an enclosed and sealed space to a controll...
    """
    pass


@dataclass
class WorkEnvelope(System):
    """System composed of the physical process execution space within a piece of equipment.
    """
    pass


@dataclass
class Systems(Component):
    """Organizer that groups System components."""
    systems: list[System] = field(default_factory=list)


@dataclass
class Table(ComponentBase):
    """leaf Component composed of a surface for holding an object or material.
    """
    pass


@dataclass
class Tank(ComponentBase):
    """leaf Component generally composed of an enclosed container.
    """
    pass


@dataclass
class Tensioner(ComponentBase):
    """leaf Component that provides or applies a stretch or strain to another mechanism.
    """
    pass


@dataclass
class TransferArm(ComponentBase):
    """leaf Component that physically moves a tool from one location to another.
    """
    pass


@dataclass
class TransferPot(ComponentBase):
    """leaf Component that is a Pot for a tool that is awaiting transfer from a ToolMagazine t...
    """
    pass


@dataclass
class Transformer(ComponentBase):
    """leaf Component that transforms electric energy from a source to a secondary circuit.
    """
    pass


@dataclass
class Valve(ComponentBase):
    """leaf Component that halts or controls the flow of a liquid, gas, or other material thro...
    """
    pass


@dataclass
class Vat(ComponentBase):
    """leaf Component generally composed of an open container.
    """
    pass


@dataclass
class Water(ComponentBase):
    """leaf Component composed of H_2 O.
    """
    pass


@dataclass
class Wire(ComponentBase):
    """leaf Component composed of a string like piece or filament of relatively rigid or flexi...
    """
    pass


@dataclass
class Workpiece(ComponentBase):
    """leaf Component composed of an object or material on which a form of work is performed.
    """
    pass
