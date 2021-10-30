from abc import ABC


class Distribution(ABC):

    def __init__(self, ordered_parameters: list = None, **kwargs):
        """
        A parent class to all :class:`.Distribution` classes.

        All distributions possess a number of methods to perform basic probabilistic operations. For most of the
        predefined distributions in :py:mod:`UQpy` these methods are inherited from the :py:mod:`scipy.stats` package.
        These include standard operations such as computing probability density/mass functions, cumulative distribution
        functions and their inverse, drawing random samples, computing moments and parameter fitting. However, for
        user-defined distributions, any desired method can be constructed into the child class structure.

        For bookkeeping purposes, all :class:`.Distribution` objects possesses :meth:`get_parameters` and
        :meth:`update_parameters` methods. These are described in more detail below.

        Any :class:`.Distribution` further inherits from one of the following classes:

        - :class:`DistributionContinuous1D`: Parent class to 1-dimensional continuous probability distributions.
        - :class:`DistributionDiscrete1D`: Parent class to 1-dimensional discrete probability distributions.
        - :class:`DistributionND`: Parent class to multivariate probability distributions.

        :param ordered_parameters: Ordered list of parameter names, useful when parameter values are stored in vectors
         and must be passed to the :meth:`update_parameters` method.
        :param kwargs: Parameters of the distribution. Note: this attribute is not defined for certain
         :class:`.Distribution` objects such as those of type :class:`.JointIndependent` or :class:`.JointCopula`. The
         user is advised to use the :meth:`get_parameters` method to access the parameters.
        """
        self.parameters = kwargs
        self.ordered_parameters = ordered_parameters
        if self.ordered_parameters is None:
            self.ordered_parameters = tuple(kwargs.keys())
        if len(self.ordered_parameters) != len(self.parameters):
            raise ValueError(
                "Inconsistent dimensions between order_params tuple and params dictionary."
            )

    def update_parameters(self, **kwargs):
        """
        Update the parameters of a :class:`.Distribution` object.

        To update the parameters of a :class:`.JointIndependent` or a :class:`.JointCopula` distribution, each parameter
        is assigned a unique string identifier as `key_index` - where `key` is the parameter name and `index` the index
        of the marginal (e.g., location parameter of the 2nd marginal is identified as `loc_1`).

        :param kwargs: Parameters to be updated, designated by their respective keywords.
        """
        for key in kwargs.keys():
            if key not in self.get_parameters().keys():
                raise ValueError("Wrong parameter name.")
            self.parameters[key] = kwargs[key]

    def get_parameters(self):
        """
        Return the parameters of a :class:`.Distribution` object.

        To update the parameters of a :class:`.JointIndependent` or a :class:`.JointCopula` distribution, each parameter
        is assigned a unique string identifier as `key_index` - where `key` is the parameter name and `index` the index
        of the marginal (e.g., location parameter of the 2nd marginal is identified as `loc_1`).

        :return: Parameters of the distribution.
        """
        return self.parameters

    @property
    def ordered_parameters(self) -> list:
        """
        :return: Ordered list of parameter names, useful when parameter values are stored in vectors and must be passed
        to the  update_params method.
        """
        return self.ordered_parameters

    @property
    def parameters(self) -> dict:
        """
        :return: Parameters of the distribution. Note: this attribute is not defined for certain :class:`.Distribution`
        objects  such as those of type :class:`.JointIndependent` or :class:`.JointCopula`. The user is advised to use
        the get_params method to access the  parameters.
        """
        return self.parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = value

    @ordered_parameters.setter
    def ordered_parameters(self, value):
        self._ordered_parameters = value