# MTConnect XMI/UML Pattern Reference

This document defines how to interpret the MTConnect v2.6 XMI model for Python code generation.

## XMI Element Types

| **xmi:type** | **Python Mapping** | **Usage** |
|---|---|---|
| `uml:Package` | Module/package organization | Logical grouping |
| `uml:Class` | `@dataclass` | Entity definitions |
| `uml:Enumeration` | `Enum` class | Fixed value sets |
| `uml:Association` | Property with relationship | Links between classes |
| `uml:Property` | Dataclass field | Attributes and relationships |
| `uml:Generalization` | Class inheritance | Type hierarchies |
| `uml:DataType` | Type alias or dataclass | Complex types |
| `uml:PrimitiveType` | Python primitive | Basic types |
| `uml:Comment` | Docstring | Documentation |

## Cardinality Interpretation

### Rules

- **lowerValue=1** → Required (no default value)
- **lowerValue=0** or missing → Optional (with `= None` or `= field(default_factory=list)`)
- **upperValue=1** → Single value
- **upperValue=\*** → List (use `field(default_factory=list)`)

### Patterns

| **lowerValue** | **upperValue** | **Python Type** |
|---|---|---|
| 1 | 1 | `FieldType` (required, no default) |
| 0 | 1 | `Optional[FieldType] = None` |
| 1 | * | `List[FieldType]` (validate non-empty) |
| 0 | * | `List[FieldType] = field(default_factory=list)` |

### XML Examples

```xml
<!-- Required single [1..1] -->
<ownedAttribute name="id" type="ID_TYPE_XMI_ID">
    <lowerValue xmi:type='uml:LiteralInteger' value='1'/>
    <upperValue xmi:type='uml:LiteralUnlimitedNatural' value='1'/>
</ownedAttribute>
```
→ `id: ID`

```xml
<!-- Optional single [0..1] -->
<ownedAttribute name="href" type="STRING_TYPE_XMI_ID">
    <lowerValue xmi:type='uml:LiteralInteger' value='0'/>
    <upperValue xmi:type='uml:LiteralUnlimitedNatural' value='1'/>
</ownedAttribute>
```
→ `href: Optional[str] = None`

```xml
<!-- Optional list [0..*] -->
<ownedAttribute name="hasPath" type="PATH_XMI_ID">
    <lowerValue xmi:type='uml:LiteralInteger'/>  <!-- Missing value = 0 -->
    <upperValue xmi:type='uml:LiteralUnlimitedNatural' value='*'/>
</ownedAttribute>
```
→ `has_path: List[Path] = field(default_factory=list)`

## Aggregation Semantics

- **aggregation='composite'** → Strong ownership (parent owns child lifecycle)
  - In Configuration classes: Nested composition objects (Transformation, Origin, etc.)
  - In Component relationships: Child component/DataItem constraints
  - In observes* relationships: DataItem type requirements

## Type Resolution

### Primitive Type Mappings

| **XMI ID** | **Type Name** | **Python Type** |
|---|---|---|
| `_19_0_3_91b028d_1579272245466_691733_672` | ID | `ID` (from primitives) |
| `_19_0_3_91b028d_1579272360416_763325_681` | string | `str` |
| `_19_0_3_91b028d_1579272233011_597138_670` | datetime | `datetime` |
| `_19_0_3_91b028d_1579272506322_914606_702` | float | `float` |
| `_19_0_3_91b028d_1579278876899_683310_3821` | boolean | `bool` |
| `_19_0_3_91b028d_1579272271512_537408_674` | integer | `int` |

### Resolution Algorithm

1. Extract `type` attribute from `<ownedAttribute>`
2. Find element with matching `xmi:id` in model
3. Check `xmi:type`:
   - `uml:Class` → Use class name
   - `uml:Enumeration` → Use enum name + "Enum"
   - `uml:DataType`/`uml:PrimitiveType` → Map to Python primitive

### Field Naming Convention

**Strip relationship prefixes** when generating Python field names:
- `hasPath` → `path`
- `hasComponent` → `component`  
- `observesDoorState` → `door_state`
- `observesRotaryMode` → `rotary_mode`

Convert to snake_case after stripping prefix.

## Association Patterns

### Structure

```xml
<packagedElement xmi:type='uml:Association' xmi:id='ASSOC_ID'>
    <memberEnd xmi:idref='CLASS_A_ATTR_ID'/>  <!-- Forward reference -->
    <memberEnd xmi:idref='OWNEDEND_ID'/>      <!-- Back-reference -->
    <ownedEnd xmi:type='uml:Property' xmi:id='OWNEDEND_ID' 
              type='CLASS_A_ID' association='ASSOC_ID'/>
</packagedElement>
```

### Interpretation

- Focus on forward direction (first memberEnd)
- Back-references (ownedEnd) typically not generated in Python
- Association links two classes bidirectionally

## Component Relationship Patterns

### observes* Pattern (DataItem Requirements)

```xml
<ownedAttribute name="observesDoorState" aggregation='composite' 
                type='DoorState_XMI_ID' association='...'>
    <lowerValue value='1'/>
    <upperValue value='1'/>
</ownedAttribute>
```

**Meaning**: Component MUST have DoorState DataItem in its data_items collection

**Python Generation**:
```python
@dataclass
class Door(Component):
    """Component with door mechanism.
    
    MTConnect Requirements:
    - MUST have exactly 1 DoorState (EVENT) DataItem [observesDoorState 1..1]
    """
    door_state: DoorState  # Required [1..1]
    
    def __post_init__(self):
        # Validation for required relationships handled by type system
        # (no default value means field is required)
        super().__post_init__()
```

### hasComponent* Pattern (Child Component Constraints)

```xml
<ownedAttribute name="hasPath" aggregation='composite' 
                type='Path_XMI_ID'>
    <lowerValue value='0'/>
    <upperValue value='*'/>
</ownedAttribute>
```

**Meaning**: Controller MAY contain 0 or more Path child components

**Python Generation**:
```python
@dataclass
class Controller(System):
    """Controller component.
    
    MTConnect Component Constraints:
    - MAY contain Path components [hasPath 0..*]
    """
    path: List[Path] = field(default_factory=list)
```

**Note**: When cardinality is [1..*] (required list), validate in `__post_init__`:
```python
@dataclass
class ExampleComponent(Component):
    required_items: List[Item]  # No default = must be provided
    
    def __post_init__(self):
        if not self.required_items:
            raise ValueError("required_items cannot be empty [1..*]")
        super().__post_init__()
```

## Configuration Nested Objects

### has* Pattern in Configuration Classes

```xml
<ownedAttribute name="hasTransformation" aggregation='composite' 
                type='Transformation_XMI_ID'>
    <lowerValue value='0'/>
    <upperValue value='1'/>
</ownedAttribute>
```

**Meaning**: SolidModel MAY contain a Transformation nested object

**Python Generation**:
```python
@dataclass
class SolidModel:
    id: ID                                    # Required
    media_type: MediaTypeEnum                  # Required
    transformation: Optional[Transformation] = None  # Optional nested object
```

## Special Attributes

### Abstract Classes

```xml
<packagedElement xmi:type='uml:Class' name='Component' isAbstract='true'>
```

→ Use `ABC` base class: `class Component(ABC)`

### Static/ReadOnly Attributes

```xml
<ownedAttribute name="type" isStatic='true' isReadOnly='true'>
    <defaultValue xmi:type='uml:InstanceValue' instance='ENUM_MEMBER_ID'/>
</ownedAttribute>
```

→ Use `ClassVar`: `type: ClassVar[EventEnum] = EventEnum.DOOR_STATE`

### Leaf Classes

```xml
<packagedElement xmi:type='uml:Class' name='Gripper' isLeaf='true'>
```

→ Cannot be subclassed (optionally use `@final` decorator)

## Package Structure

### Key Packages in model_2.6.xml

- **Components Package**: Line 46927, XMI ID: `EAPK_6F87CB48_AFED_473f_92DF_E7AFDAFD3CAC`
  - **Component Types**: Line 47160 (40+ concrete component classes)
- **DataItems Package**: Line 50099, XMI ID: `EAPK_0FAC31E7_7957_49d2_AD4C_BCFBEF9878FD`
  - **DataItem Types**: Line 50324 (300+ DataItem classes)
- **Compositions Package**: Line 49890, XMI ID: `EAPK_3D92D585_AB2B_4fe0_8B49_2F22359705CA`
- **References Package**: Line 51352, XMI ID: `EAPK_F54CCA63_E73C_468b_B64E_F97DEE70FFC6`
- **Configuration Package**: Line 51611+, XMI ID: `_19_0_3_91b028d_1579526876433_244855_7626`

## Documentation Extraction

### ownedComment Pattern

```xml
<ownedComment xmi:type='uml:Comment' body='Component description'>
    <annotatedElement xmi:idref='CLASS_XMI_ID'/>
</ownedComment>
```

### Cleaning Rules

Remove MTConnect template syntax:
- `{{block(X)}}` → `X`
- `{{term(X)}}` → `X`
- `{{property(X)}}` → `X`
- `{{sect(X)}}` → `X`

## Extension-Wrapped Elements (MagicDraw)

Some XMI exports wrap elements in `<xmi:Extension>`:

```xml
<xmi:Extension extender='MagicDraw UML 2024x'>
    <modelExtension>
        <lowerValue xmi:type='uml:LiteralInteger' value='1'/>
    </modelExtension>
</xmi:Extension>
```

**Parser must check both direct children AND extension-wrapped children.**
