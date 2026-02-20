"""
MTConnect Component Models

Component hierarchy representing the physical and logical organization of
manufacturing equipment in the MTConnect device information model.

Reference: MTConnect Standard v2.6 Normative Model
Auto-generated from: model_2.6.xml
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from mtconnect.models.configurations import Configuration
from mtconnect.types.primitives import ID, UUID

if TYPE_CHECKING:
    from mtconnect.models.data_items import DataItem



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
    uuid: UUID | None = None
    native_name: str | None = None
    sample_interval: float | None = None
    sample_rate: float | None = None
    description: Description | None = None
    configuration: Configuration | None = None
    data_items: list[DataItem] = field(default_factory=list)
    components: list[Component] = field(default_factory=list)

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
    """Component that provides information about the data source for an MTConnect Agent."""


@dataclass
class Adapters(Component):
    """Organizer that groups Adapter components."""
    adapters: list[Adapter] = field(default_factory=list)


@dataclass
class Amplifier(Component):
    """leaf Component composed of an electronic component or circuit that amplifies power, ele..."""


@dataclass
class Auxiliaries(Component):
    """Organizer that groups Auxiliary components."""
    auxiliaries: list[Auxiliary] = field(default_factory=list)


@dataclass
class Auxiliary(Component):
    """abstract Component composed of removable part(s) of a piece of equipment that provides ..."""


@dataclass
class CuttingTorch(Auxiliary):
    """Auxiliary that employs a concentrated flame to both sever materials through cutting and..."""


@dataclass
class Deposition(Auxiliary):
    """Auxiliary that manages the addition of material or state change of material being perfo..."""


@dataclass
class Electrode(Auxiliary):
    """Auxiliary that is used for many electrical discharge manufacturing processes like welding."""


@dataclass
class Loader(Auxiliary):
    """Auxiliary that provides movement and distribution of materials, parts, tooling, and oth..."""


@dataclass
class BarFeeder(Loader):
    """Loader that delivers bar stock to a piece of equipment."""


@dataclass
class ToolingDelivery(Auxiliary):
    """Auxiliary that manages, positions, stores, and delivers tooling within a piece of equip..."""


@dataclass
class AutomaticToolChanger(ToolingDelivery):
    """ToolingDelivery composed of a tool delivery mechanism that moves tools between a ToolMa..."""


@dataclass
class GangToolBar(ToolingDelivery):
    """ToolingDelivery composed of a tool mounting mechanism that holds any number of tools."""


@dataclass
class ToolMagazine(ToolingDelivery):
    """ToolingDelivery composed of a tool storage mechanism that holds any number of tools."""


@dataclass
class ToolRack(ToolingDelivery):
    """ToolingDelivery composed of a linear or matrixed tool storage mechanism that holds any ..."""


@dataclass
class Turret(ToolingDelivery):
    """ToolingDelivery composed of a tool mounting mechanism that holds any number of tools."""


@dataclass
class WasteDisposal(Auxiliary):
    """Auxiliary that removes manufacturing byproducts from a piece of equipment."""


@dataclass
class Axes(Component):
    """Organizer that groups Axis components."""
    axes: list[Axis] = field(default_factory=list)


@dataclass
class Axis(Component):
    """abstract Component composed of a motion system that provides linear or rotational motio..."""


@dataclass
class Linear(Axis):
    """Component Types::Axis that provides prismatic motion along a fixed axis."""


@dataclass
class Rotary(Axis):
    """Component Types::Axis that provides rotation about a fixed axis."""


@dataclass
class Spindle(Axis):
    """Component that provides an axis of rotation for the purpose of rapidly rotating a part ..."""


@dataclass
class Ballscrew(Component):
    """leaf Component composed of a mechanical structure that transforms rotary motion into li..."""


@dataclass
class Belt(Component):
    """leaf Component composed of an endless flexible band that transmits motion for a piece o..."""


@dataclass
class Brake(Component):
    """leaf Component that slows or stops a moving object by the absorption or transfer of the..."""


@dataclass
class Chain(Component):
    """leaf Component composed of interconnected series of objects that band together and are ..."""


@dataclass
class Chopper(Component):
    """leaf Component that breaks material into smaller pieces."""


@dataclass
class Chuck(Component):
    """leaf Component composed of a mechanism that holds a part or stock material in place."""


@dataclass
class Chute(Component):
    """leaf Component composed of an inclined channel that conveys material."""


@dataclass
class CircuitBreaker(Component):
    """leaf Component that interrupts an electric circuit."""


@dataclass
class Clamp(Component):
    """leaf Component that strengthens, support, or fastens objects in place."""


@dataclass
class Compressor(Component):
    """leaf Component composed of a pump or other mechanism that reduces volume and increases ..."""


@dataclass
class Controllers(Component):
    """Organizer that groups Controller components."""
    controllers: list[Controller] = field(default_factory=list)


@dataclass
class CoolingTower(Component):
    """leaf Component composed of a heat exchange system that uses a fluid to transfer heat to..."""


@dataclass
class Door(Component):
    """Component composed of a mechanical mechanism or closure that can cover a physical acces..."""


@dataclass
class Drain(Component):
    """leaf Component that allows material to flow for the purpose of drainage from, for examp..."""


@dataclass
class Encoder(Component):
    """leaf Component that measures position."""


@dataclass
class Environmental(Component):
    """Component that observes the surroundings of another Component."""


@dataclass
class ExpiredPot(Component):
    """leaf Component that is a Pot for a tool that is no longer usable for removal from a Too..."""


@dataclass
class ExposureUnit(Component):
    """leaf Component that emits a type of radiation."""


@dataclass
class ExtrusionUnit(Component):
    """leaf Component that dispenses liquid or powered materials."""


@dataclass
class Fan(Component):
    """leaf Component that produces a current of air."""


@dataclass
class Filter(Component):
    """leaf Component through which liquids or gases are passed to remove suspended impurities..."""


@dataclass
class Galvanomotor(Component):
    """leaf Component composed of an electromechanical actuator that produces deflection of a ..."""


@dataclass
class Gripper(Component):
    """leaf Component that holds a part, stock material, or any other item in place."""


@dataclass
class Hopper(Component):
    """leaf Component composed of a chamber or bin in which materials are stored temporarily, ..."""


@dataclass
class Interface(Component):
    """abstract Component that coordinates actions and activities between pieces of equipment."""


@dataclass
class BarFeederInterface(Interface):
    """Interface that coordinates the operations between a bar feeder and another piece of equ..."""


@dataclass
class ChuckInterface(Interface):
    """Interface that coordinates the operations between two pieces of equipment, one of which..."""


@dataclass
class DoorInterface(Interface):
    """Interface that coordinates the operations between two pieces of equipment, one of which..."""


@dataclass
class MaterialHandlerInterface(Interface):
    """Interface that coordinates the operations between a piece of equipment and another asso..."""


@dataclass
class Requester(Interface):
    """Requester component."""


@dataclass
class Responder(Interface):
    """Responder component."""


@dataclass
class Interfaces(Component):
    """Organizer that groups Interface components."""
    interfaces: list[Interface] = field(default_factory=list)


@dataclass
class LinearPositionFeedback(Component):
    """leaf Component that measures linear motion or position."""


@dataclass
class Lock(Component):
    """Component that physically prohibits a Device or Component from opening or operating."""


@dataclass
class Materials(Component):
    """Organizer that groups Material components."""
    materials: list[Material] = field(default_factory=list)


@dataclass
class Motor(Component):
    """leaf Component that converts electrical, pneumatic, or hydraulic energy into mechanical..."""


@dataclass
class Oil(Component):
    """leaf Component composed of a viscous liquid."""


@dataclass
class Part(Component):
    """abstract Component composed of a part being processed by a piece of equipment."""


@dataclass
class PartOccurrence(Part):
    """Part that exists at a specific place and time, such as a specific instance of a bracket..."""


@dataclass
class FeatureOccurrence(PartOccurrence):
    """Component that provides information related to an individual feature."""


@dataclass
class Parts(Component):
    """Organizer that groups Part components."""
    parts: list[Part] = field(default_factory=list)


@dataclass
class Path(Component):
    """Component that organizes an independent operation or function within a Controller."""


@dataclass
class Pot(Component):
    """leaf Component composed of a tool storage location associated with a ToolMagazine or Au..."""


@dataclass
class PowerSupply(Component):
    """leaf Component that provides power to electric mechanisms."""


@dataclass
class Process(Component):
    """abstract Component composed of a manufacturing process being executed on a piece of equ..."""


@dataclass
class ProcessOccurrence(Process):
    """Process that takes place at a specific place and time, such as a specific instance of p..."""


@dataclass
class Processes(Component):
    """Organizer that groups Process components."""
    processes: list[Process] = field(default_factory=list)


@dataclass
class Pulley(Component):
    """leaf Component composed of a mechanism or wheel that turns in a frame or block and serv..."""


@dataclass
class Pump(Component):
    """leaf Component that raises, drives, exhausts, or compresses fluids or gases by means of..."""


@dataclass
class Reel(Component):
    """leaf Component composed of a rotary storage unit for material."""


@dataclass
class RemovalPot(Component):
    """leaf Component that is a Pot for a tool that has to be removed from a ToolMagazine or T..."""


@dataclass
class Resource(Component):
    """abstract Component composed of material or personnel involved in a manufacturing process."""


@dataclass
class Material(Resource):
    """Resource composed of material that is consumed or used by the piece of equipment for pr..."""


@dataclass
class Stock(Material):
    """Material that is used in a manufacturing process and to which work is applied in a mach..."""


@dataclass
class Personnel(Resource):
    """Resource composed of an individual or individuals who either control, support, or other..."""


@dataclass
class Resources(Component):
    """Organizer that groups Resource components."""
    resources: list[Resource] = field(default_factory=list)


@dataclass
class ReturnPot(Component):
    """leaf Component that is a Pot for a tool that has been removed from spindle or Turret an..."""


@dataclass
class SensingElement(Component):
    """leaf Component that provides a signal or measured value."""


@dataclass
class Sensor(Component):
    """Component that responds to a physical stimulus and transmits a resulting impulse or val..."""


@dataclass
class Spreader(Component):
    """leaf Component that flattens or spreading materials."""


@dataclass
class StagingPot(Component):
    """leaf Component that is a Pot for a tool that is awaiting transfer to a ToolMagazine or ..."""


@dataclass
class Station(Component):
    """leaf Component composed of a storage or mounting location for a tool associated with a ..."""


@dataclass
class StorageBattery(Component):
    """leaf Component composed of one or more cells in which chemical energy is converted into..."""


@dataclass
class Structure(Component):
    """Component composed of part(s) comprising the rigid bodies of the piece of equipment."""


@dataclass
class Link(Structure):
    """Structure that provides a connection between Component entities."""


@dataclass
class Structures(Component):
    """Organizer that groups Structure components."""
    structures: list[Structure] = field(default_factory=list)


@dataclass
class Switch(Component):
    """leaf Component that turns on or off an electric current or makes or breaks a circuit."""


@dataclass
class System(Component):
    """abstract Component that is permanently integrated into the piece of equipment."""


@dataclass
class Actuator(System):
    """Component composed of a physical apparatus that moves or controls a mechanism or system."""


@dataclass
class Hydraulic(Actuator):
    """System that provides movement and distribution of pressurized liquid throughout the pie..."""


@dataclass
class Pneumatic(Actuator):
    """System that uses compressed gasses to actuate components or do work within the piece of..."""


@dataclass
class AirHandler(System):
    """system that circulates air or regulates airflow without altering temperature or humidity."""


@dataclass
class Controller(System):
    """System that provides regulation or management of a system or component."""


@dataclass
class Coolant(System):
    """System that provides distribution and management of fluids that remove heat from a piec..."""


@dataclass
class Cooling(System):
    """System that extracts controlled amounts of heat to achieve a target temperature at a sp..."""


@dataclass
class Dielectric(System):
    """System that manages a chemical mixture used in a manufacturing process being performed ..."""


@dataclass
class Electric(System):
    """System composed of the main power supply for the piece of equipment that provides distr..."""


@dataclass
class Enclosure(System):
    """System composed of a structure that is used to contain or isolate a piece of equipment ..."""


@dataclass
class EndEffector(System):
    """System composed of functions that form the last link segment of a piece of equipment."""


@dataclass
class Feeder(System):
    """System that manages the delivery of materials within a piece of equipment."""


@dataclass
class Heating(System):
    """System that delivers controlled amounts of heat to achieve a target temperature at a sp..."""


@dataclass
class Lubrication(System):
    """System that provides distribution and management of fluids used to lubricate portions o..."""


@dataclass
class Pressure(System):
    """System that delivers compressed gas or fluid and controls the pressure and rate of pres..."""


@dataclass
class ProcessPower(System):
    """System composed of a power source associated with a piece of equipment that supplies en..."""


@dataclass
class Protective(System):
    """System that provides functions used to detect or prevent harm or damage to equipment or..."""


@dataclass
class Vacuum(System):
    """System that evacuates gases and liquids from an enclosed and sealed space to a controll..."""


@dataclass
class WorkEnvelope(System):
    """System composed of the physical process execution space within a piece of equipment."""


@dataclass
class Systems(Component):
    """Organizer that groups System components."""
    systems: list[System] = field(default_factory=list)


@dataclass
class Table(Component):
    """leaf Component composed of a surface for holding an object or material."""


@dataclass
class Tank(Component):
    """leaf Component generally composed of an enclosed container."""


@dataclass
class Tensioner(Component):
    """leaf Component that provides or applies a stretch or strain to another mechanism."""


@dataclass
class TransferArm(Component):
    """leaf Component that physically moves a tool from one location to another."""


@dataclass
class TransferPot(Component):
    """leaf Component that is a Pot for a tool that is awaiting transfer from a ToolMagazine t..."""


@dataclass
class Transformer(Component):
    """leaf Component that transforms electric energy from a source to a secondary circuit."""


@dataclass
class Valve(Component):
    """leaf Component that halts or controls the flow of a liquid, gas, or other material thro..."""


@dataclass
class Vat(Component):
    """leaf Component generally composed of an open container."""


@dataclass
class Water(Component):
    """leaf Component composed of H_2 O."""


@dataclass
class Wire(Component):
    """leaf Component composed of a string like piece or filament of relatively rigid or flexi..."""


@dataclass
class Workpiece(Component):
    """leaf Component composed of an object or material on which a form of work is performed."""
