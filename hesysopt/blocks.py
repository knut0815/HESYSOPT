# -*- coding: utf-8 -*-
"""

"""
from pyomo.core import (Constraint, BuildAction)
from pyomo.core.base.block import SimpleBlock

class ExtractionTurbine(SimpleBlock):
    """Block for the extraction turbine containing the constraints.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ Creates the linear constraint for the
        class:`.nodes.ExtractionTurbine`.

        Parameters
        ----------
        group : list
            List of :class:`ExtractionTurbine` objects
            e.g. group = [extr1, extr2, ...].
        """
        if group is None:
            return None

        m = self.parent_block()

        for n in group:
            n.power_heat_index = [
                n.conversion_factors[m.es.groups[n._power_output().label]][t] /
                n.conversion_factors[m.es.groups[n._heat_output().label]][t]
                for t in m.TIMESTEPS
            ]

        def _equivalent_power_rule(block):
            """
            """
            for t in m.TIMESTEPS:
                for n in group:
                    lhs = m.flow[n._input(), n, t]
                    rhs = (
                        (m.flow[n, n._power_output(), t] *
                             n.power_loss_index[t] +
                         m.flow[n, n._heat_output(), t]) /
                             n.efficiency_condensing
                        )
                    block.equivalent_power.add((n, t), (lhs == rhs))
        self.equivalent_power = Constraint(group, noruleinit=True)
        self.equivalent_power_build = BuildAction(rule=_equivalent_power_rule)

        def _power_to_heat_rule(block):
            """
            """
            for t in m.TIMESTEPS:
                for n in group:
                    lhs = m.flow[n, n._power_output(), t]
                    rhs = (m.flow[n, n._heat_output(), t] *
                           n.power_heat_index[t])
                    block.power_heat.add((n, t), (lhs >= rhs))
        self.power_heat = Constraint(group, noruleinit=True)
        self.power_heat_build = BuildAction(rule=_power_to_heat_rule)


class ExtractionTurbineExtended(SimpleBlock):
    """Block for the extraction turbine containing the constraints.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """
        """
        if group is None:
            return None

        m = self.parent_block()

        for n in group:
            n.efficiency_total = [
                n.conversion_factors[m.es.groups[n._power_output().label]][t] +
                n.conversion_factors[m.es.groups[n._heat_output().label]][t]
                for t in m.TIMESTEPS
            ]
            n.calculate_coefficients()

        self.TURBINES = [n for n in group]

        # 1) P <= p[0] - beta[0]*Q
        def _max_boiler_load_rule(block, n, t):
            """
            """
            lhs = m.flow[n, n._power_output(), t]
            rhs = (n.p[0] - n.power_loss_index[t] *
                    m.flow[n, n._heat_output(), t])
            return (lhs <= rhs)
        self.constraint_c1 = Constraint(self.TURBINES, m.TIMESTEPS,
                                        rule=_max_boiler_load_rule)

        # 2) P = c[0] + c[1] * Q
        def _power_heat_rule(block, n, t):
            lhs = m.flow[n, n._power_output(), t]
            rhs = m.flow[n, n._heat_output(), t] * n.c[1] + n.c[0]
            return (lhs >= rhs)
        self.constraint_c2= Constraint(self.TURBINES, m.TIMESTEPS,
                                       rule=_power_heat_rule)

        # 3) P >= p[1] - beta[1]*Q
        def _min_boiler_load_rule(block, n, t):
            if True: #n.outputs[n._power_output()].discrete is not None:
                lhs = m.flow[n, n._power_output(), t]
                rhs = (n.p[1] - n.power_loss_index[t] *
                       m.flow[n, n._heat_output(), t])
                return(lhs >= rhs)
            else:
                return(Constraint.Skip)
        self.constraint_c3 = Constraint(self.TURBINES, m.TIMESTEPS,
                                        rule=_min_boiler_load_rule)

        # H = k[0] + k[1]*P + k[2]*Q
        def _fuel_consumption_rule(block, n, t):
            lhs = m.flow[n._input(), n, t]
            rhs = (n.k[0] + n.k[1]*m.flow[n, n._power_output(), t] +
                       n.k[2] * m.flow[n, n._heat_output(), t])
            return(lhs == rhs)
        self.fuel_consumption = Constraint(self.TURBINES, m.TIMESTEPS,
                                           rule=_fuel_consumption_rule)



class BackpressureTurbine(SimpleBlock):
    """Block for the extraction turbine containing the constraints.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _create(self, group=None):
        """ Creates constraints for backpressure turbine.

        Parameters
        ----------
        group : list
            List of :class:`BackpressureTurbine` objects
            e.g. group = [bp1, bp2, ...].
        """
        if group is None:
            return None

        m = self.parent_block()

        def _electrical_efficiency_rule(block):
            """Rule definition for electrical efficiency relation of
            backpressure turbine.
            """
            for t in m.TIMESTEPS:
                for n in group:
                    lhs = (m.flow[n._input(), n, t] *
                               n.conversion_factors[n._power_output()][t])
                    rhs = m.flow[n, n._power_output(), t]
                    block.electrical_eff.add((n, t), (lhs == rhs))
        self.electrical_eff = Constraint(group, noruleinit=True)
        self.electrical_efficiency_build = BuildAction(
            rule=_electrical_efficiency_rule)

        def _power_to_heat_rule(block):
            """Rule definition of power to heat relation of backpressure
            turbine.
            """
            for t in m.TIMESTEPS:
                for n in group:
                    lhs = (m.flow[n, n._power_output(), t] /
                               n.conversion_factors[n._power_output()][t])
                    rhs = (m.flow[n, n._heat_output(), t] /
                               n.conversion_factors[n._heat_output()][t])
                    block.power_heat.add((n, t), (lhs == rhs))
        self.power_heat = Constraint(group, noruleinit=True)
        self.power_heat_build = BuildAction(rule=_power_to_heat_rule)