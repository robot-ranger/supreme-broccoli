"""
Tests for MTConnect Component models.
"""

from mtconnect.models.components import (
    Actuator,
    Agent,
    Auxiliary,
    Axes,
    Axis,
    Component,
    ComponentBase,
    Composition,
    Controller,
    Controllers,
    Description,
    Device,
    Encoder,
    FeatureOccurrence,
    Hydraulic,
    Linear,
    Link,
    Material,
    Materials,
    Motor,
    Part,
    PartOccurrence,
    Pneumatic,
    Process,
    ProcessOccurrence,
    Resource,
    Resources,
    Spindle,
    Stock,
    Structure,
    System,
    Valve,
)
from mtconnect.types.primitives import ID, UUID


def test_device_creation():
    """Test Device creation with required fields"""
    device = Device(
        id=ID("mill"),
        name="Mill-01",
        uuid=UUID("M8010W4194N")
    )

    assert device.id == ID("mill")
    assert device.name == "Mill-01"
    assert device.uuid == UUID("M8010W4194N")


def test_device_with_description():
    """Test Device with Description metadata"""
    desc = Description(
        manufacturer="ACME Corp",
        model="CNC-5000",
        serial_number="SN12345"
    )

    device = Device(
        id=ID("mill"),
        name="Mill-01",
        description=desc
    )

    assert device.description.manufacturer == "ACME Corp"
    assert device.description.serial_number == "SN12345"


def test_device_add_component():
    """Test adding components to a device"""
    device = Device(id=ID("mill"), name="Mill-01")
    controller = Controller(id=ID("cnc"), name="Controller")

    device.add_component(controller)

    assert len(device.components) == 1
    assert device.components[0] == controller


def test_linear_component():
    """Test Linear component creation"""
    x_axis = Linear(
        id=ID("x"),
        name="X",
        native_name="X-Axis"
    )

    assert x_axis.id == ID("x")
    assert x_axis.name == "X"
    assert x_axis.native_name == "X-Axis"


def test_spindle_component():
    """Test Spindle component creation"""
    spindle = Spindle(
        id=ID("sp1"),
        name="Spindle"
    )

    assert spindle.id == ID("sp1")


# --- New tests for abstract base types ---


def test_axis_abstract_base():
    """Test Axis abstract base can be instantiated"""
    axis = Axis(id=ID("ax1"), name="Axis-1")
    assert axis.id == ID("ax1")
    assert axis.name == "Axis-1"


def test_system_abstract_base():
    """Test System abstract base can be instantiated"""
    system = System(id=ID("sys1"), name="System-1")
    assert system.id == ID("sys1")


def test_auxiliary_abstract_base():
    """Test Auxiliary abstract base can be instantiated"""
    aux = Auxiliary(id=ID("aux1"), name="Auxiliary-1")
    assert aux.id == ID("aux1")


def test_resource_abstract_base():
    """Test Resource abstract base can be instantiated"""
    res = Resource(id=ID("res1"), name="Resource-1")
    assert res.id == ID("res1")


# --- New tests for organizer types ---


def test_axes_organizer():
    """Test Axes organizer can hold typed children"""
    axes = Axes(id=ID("axes1"), name="Axes")
    linear = Linear(id=ID("x"), name="X")
    axes.axes.append(linear)
    assert len(axes.axes) == 1
    assert isinstance(axes.axes[0], Axis)


def test_resources_organizer():
    """Test Resources organizer can hold typed children"""
    resources = Resources(id=ID("res"), name="Resources")
    mat = Material(id=ID("mat1"), name="Material-1")
    resources.resources.append(mat)
    assert len(resources.resources) == 1
    assert isinstance(resources.resources[0], Resource)


def test_controllers_organizer():
    """Test Controllers organizer can hold typed children"""
    controllers = Controllers(id=ID("ctrls"), name="Controllers")
    ctrl = Controller(id=ID("ctrl1"), name="Controller-1")
    controllers.controllers.append(ctrl)
    assert len(controllers.controllers) == 1


def test_materials_organizer():
    """Test Materials organizer can hold typed children"""
    materials = Materials(id=ID("mats"), name="Materials")
    stock = Stock(id=ID("stk1"), name="Stock-1")
    materials.materials.append(stock)
    assert len(materials.materials) == 1


# --- New tests for leaf types ---


def test_motor_leaf():
    """Test Motor leaf component instantiation"""
    motor = Motor(id=ID("m1"), name="Motor-1")
    assert motor.id == ID("m1")
    assert isinstance(motor, ComponentBase)
    # Leaf components should NOT have 'components' field
    assert not hasattr(motor, 'components')


def test_encoder_leaf():
    """Test Encoder leaf component instantiation"""
    encoder = Encoder(id=ID("enc1"), name="Encoder-1")
    assert encoder.id == ID("enc1")
    assert isinstance(encoder, ComponentBase)
    # Leaf components should NOT have 'components' field
    assert not hasattr(encoder, 'components')


def test_valve_leaf():
    """Test Valve leaf component instantiation"""
    valve = Valve(id=ID("v1"), name="Valve-1")
    assert valve.id == ID("v1")
    assert isinstance(valve, ComponentBase)
    # Leaf components should NOT have 'components' field
    assert not hasattr(valve, 'components')


# --- Inheritance checks ---


def test_linear_extends_axis():
    """Test Linear inherits from Axis"""
    linear = Linear(id=ID("x"), name="X")
    assert isinstance(linear, Axis)
    assert isinstance(linear, Component)


def test_controller_extends_system():
    """Test Controller inherits from System"""
    ctrl = Controller(id=ID("ctrl1"), name="Controller")
    assert isinstance(ctrl, System)
    assert isinstance(ctrl, Component)


def test_hydraulic_extends_actuator():
    """Test Hydraulic inherits from Actuator"""
    hyd = Hydraulic(id=ID("hyd1"), name="Hydraulic")
    assert isinstance(hyd, Actuator)
    assert isinstance(hyd, System)
    assert isinstance(hyd, Component)


def test_pneumatic_extends_actuator():
    """Test Pneumatic inherits from Actuator"""
    pneu = Pneumatic(id=ID("pneu1"), name="Pneumatic")
    assert isinstance(pneu, Actuator)


def test_stock_extends_material():
    """Test Stock inherits from Material"""
    stock = Stock(id=ID("stk1"), name="Stock")
    assert isinstance(stock, Material)
    assert isinstance(stock, Resource)
    assert isinstance(stock, Component)


def test_link_extends_structure():
    """Test Link inherits from Structure"""
    link = Link(id=ID("lnk1"), name="Link")
    assert isinstance(link, Structure)
    assert isinstance(link, Component)


# --- New subtypes ---


def test_feature_occurrence():
    """Test FeatureOccurrence instantiation"""
    fo = FeatureOccurrence(id=ID("fo1"), name="Feature-1")
    assert isinstance(fo, PartOccurrence)
    assert isinstance(fo, Part)
    assert isinstance(fo, Component)


def test_process_occurrence():
    """Test ProcessOccurrence instantiation"""
    po = ProcessOccurrence(id=ID("po1"), name="Process-1")
    assert isinstance(po, Process)
    assert isinstance(po, Component)


def test_agent_extends_device():
    """Test Agent inherits from Device"""
    agent = Agent(id=ID("agent1"), name="Agent-1")
    assert isinstance(agent, Device)
    assert isinstance(agent, Component)


def test_composition_extends_component():
    """Test Composition inherits from Component"""
    comp = Composition(id=ID("comp1"), name="Composition-1")
    assert isinstance(comp, Component)
