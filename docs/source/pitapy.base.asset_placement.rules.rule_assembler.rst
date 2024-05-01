RuleAssembler Module
===================

Overview
--------

The `RuleAssembler` class streamlines the process of mapping user-defined rules to their corresponding rule objects and assembling them into site-rule pairings. This functionality allows for a high degree of customization in how rules are applied to simulation environments, ensuring that user specifications are accurately translated into actionable constraints.

Key Features
------------

- **Dynamic Rule Mapping**: Interprets user configurations to instantiate the appropriate rule objects, supporting a range of rule types including `HeightRule`, `BoundaryRule`, and `MinDistanceMujocoPhysicsRule`.

- **Site-Rule Pairing**: Organizes rules by their associated sites, enabling targeted application of constraints based on the specific characteristics or requirements of each site.

- **Customizable Rule Application**: Offers flexibility in defining and applying rules, accommodating a variety of simulation scenarios and requirements through user-defined configurations.

Usage
-----

The `RuleAssembler` is implemented within the simulation setup:

1. **Initialization**:  `RuleAssembler` instatiated with a dictionary of user-defined rules, detailing the constraints and parameters for each rule. This is provided in the config.yml of the user.

2. **Rule Object Creation**: `_get_rule_object` method  dynamically create rule objects based on the specified rule names and parameters.

3. **Assemble Site-Rule Pairs**: the `assemble_site_rules_pairs` method organizes the created rule objects into pairs with their respective sites, facilitating their application within the simulation environment.


.. automodule:: pitapy.base.asset_placement.rules.rule_assembler
   :members:
   :undoc-members:
   :show-inheritance:
   :private-members:
