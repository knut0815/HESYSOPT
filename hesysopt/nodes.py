"""New components subclassed from oemof.solph components are defined in this
   file.
"""
import numpy as np
from oemof.solph import LinearTransformer, Bus
from oemof.solph.plumbing import Sequence

# ############################# Busses ########################################

class ResourceBus(Bus):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class HeatBus(Bus):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ElectricalBus(Bus):
    """
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# ############################# Components ####################################

class ExtractionTurbine(LinearTransformer):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)
        self.efficiency_condensing = kwargs.get('efficiency_condensing')
        self.power_loss_index = Sequence(kwargs.get('power_loss_index'))

    def _input(self):
        """Returns first and only input of the extraction turbine.
        """
        return [i for i in self.inputs][0]

    def _power_output(self):
        """
        """
        return [o for o in self.outputs if 'electrical_balance' in o.label][0]

    def _heat_output(self):
        """
        """
        return [o for o in self.outputs if 'heat_balance' in o.label][0]

class ExtractionTurbineExtended(ExtractionTurbine):
    """
    An ExtractionCHP uses half-space representation to model the P-Q-relation
    # points in p/q diagramm
    *0=(100,0) --
                 -- *2

     *1=(50,0) --
                  -- *3
    """
    lower_name = "simple_extraction_chp"

    def __init__(self, **kwargs):
        """

        """
        super().__init__(**kwargs)
        self.efficiency_condesing_min = kwargs.get('efficiency_condesing_min')
        self.efficiency_total  = Sequence(kwargs.get('efficiency_total'))


    def calculate_coefficients(self):
        """ This will calculate the coefficients for half-space representation
        of the PQ-space.
        """
        #TODO : include timedepent max, min and beta
        outflow = self.outputs[self._power_output()]

        p = [outflow.max[0] * outflow.nominal_value,
             outflow.min[0] * outflow.nominal_value,
             None, None]

        q = [0, 0, None, None]

        eta_el = [self.efficiency_condensing,
                  self.efficiency_condesing_min]

        eta = self.efficiency_total

        # max / min fuel consumption
        h = [p[0] / eta_el[0],
             p[1] / eta_el[1]]

        # heat in stationary point 2,3
        q[2] = (h[0]*eta[0] - p[0]) / (1-self.power_loss_index[0])
        q[3] = (h[1]*eta[0] - p[1]) / (1-self.power_loss_index[0])

        # elctrical power in point 2,3  with: P = P0 - S * Q
        p[2] = p[0] - self.power_loss_index[0] * q[2]
        p[3] = p[1] - self.power_loss_index[0] * q[3]

        # determine coefficients for "backpressure"-mode constraint
        a = np.array([[1, q[2]],
                      [1, q[3]]])
        b = np.array([p[2],
                      p[3]])
        self.c = np.linalg.solve(a, b)


        # determine coeffcients for fuel consumption
        a = np.array([[1, p[0], 0],
                      [1, p[1], 0],
                      [1, p[2], q[2]]])
        b = np.array([h[0], h[1], h[0]])
        self.k = np.linalg.solve(a, b)
        self.p = p



class BackpressureTurbine(LinearTransformer):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)

    def _power_output(self):
        """
        """
        return [o for o in self.outputs
                if 'electrical_balance' in o.label][0]

    def _heat_output(self):
        """
        """
        return [o for o in self.outputs
                if 'heat_balance' in o.label][0]

class Boiler(LinearTransformer):
    """
    """
    def __init__(self, *args, **kwargs):
        """
        """
        super().__init__(*args, **kwargs)

    def _heat_output(self):
        """
        """
        return [o for o in self.outputs
                if 'heat_balance' in o.label][0]