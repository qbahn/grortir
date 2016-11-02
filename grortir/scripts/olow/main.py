import pickle

from numpy import genfromtxt
from sklearn.neural_network import MLPRegressor

from grortir.main.model.core.abstract_process import AbstractProcess
from grortir.main.model.stages.calls_stage import CallsStage
from grortir.main.optimizers.grouping_strategy import GroupingStrategy
from grortir.main.pso.calls_optimization_strategy import \
    CallsOptimizationStrategy
from grortir.main.pso.pso_algorithm import PsoAlgorithm

m1_data0 = genfromtxt('data/M1_data0.csv', delimiter=',')

mlpr1_1 = MLPRegressor(hidden_layer_sizes=(11, 13,), max_iter=100000,
                       solver='lbfgs')
mlpr1_2 = MLPRegressor(hidden_layer_sizes=(24,), max_iter=100000,
                       solver='lbfgs')
mlpr1_3 = MLPRegressor(hidden_layer_sizes=(22, 14,), max_iter=100000,
                       solver='lbfgs')

x = m1_data0[:, [0, 2]]

y1 = m1_data0[:, 3]
y2 = m1_data0[:, 4]
y3 = m1_data0[:, 5]

y1_ = mlpr1_1.fit(x, y1)
y2_ = mlpr1_2.fit(x, y2)
y3_ = mlpr1_3.fit(x, y3)

# mlpr = pickle.load(open("model.p","rb"))

m1_dataTest = genfromtxt('data/M1_dataTest.csv', delimiter=',')

x_pred = m1_dataTest[:, [0, 2]]
y_pred_1 = mlpr1_1.predict(x_pred)
y_pred_2 = mlpr1_2.predict(x_pred)
y_pred_3 = mlpr1_3.predict(x_pred)

pickle.dump(mlpr1_1, open("model1_1.p", "wb"))
pickle.dump(mlpr1_2, open("model1_2.p", "wb"))
pickle.dump(mlpr1_3, open("model1_3.p", "wb"))

y_real_1 = m1_dataTest[:, 3]
y_real_2 = m1_dataTest[:, 4]
y_real_3 = m1_dataTest[:, 5]

print(max(abs(y_pred_1 - y_real_1)))
print(max(abs(y_pred_2 - y_real_2)))
print(max(abs(y_pred_3 - y_real_3)))

# generowanie modeli dla etapu 2
m2_data0 = genfromtxt('data/M2_data0.csv', delimiter=',')

mlpr2_1 = MLPRegressor(hidden_layer_sizes=(27, 9,), max_iter=500000,
                       solver='lbfgs', learning_rate='invscaling')
mlpr2_2 = MLPRegressor(hidden_layer_sizes=(13,), max_iter=500000,
                       solver='lbfgs', learning_rate='invscaling')
mlpr2_3 = MLPRegressor(hidden_layer_sizes=(24, 12,), max_iter=500000,
                       solver='lbfgs', learning_rate='invscaling')

x = m2_data0[:, [0, 5]]

y1 = m2_data0[:, 6]
y2 = m2_data0[:, 7]
y3 = m2_data0[:, 8]

y1_ = mlpr2_1.fit(x, y1)
y2_ = mlpr2_2.fit(x, y2)
y3_ = mlpr2_3.fit(x, y3)

# mlpr = pickle.load(open("model.p","rb"))

m2_dataTest = genfromtxt('data/M2_dataTest.csv', delimiter=',')

x_pred = m2_dataTest[:, [0, 5]]
y_pred_1 = mlpr2_1.predict(x_pred)
y_pred_2 = mlpr2_2.predict(x_pred)
y_pred_3 = mlpr2_3.predict(x_pred)

pickle.dump(mlpr2_1, open("model2_1.p", "wb"))
pickle.dump(mlpr2_2, open("model2_2.p", "wb"))
pickle.dump(mlpr2_3, open("model2_3.p", "wb"))

y_real_1 = m2_dataTest[:, 6]
y_real_2 = m2_dataTest[:, 7]
y_real_3 = m2_dataTest[:, 8]

print("Bledy dla modeli etapu 2:")
print(max(abs(y_pred_1 - y_real_1) / y_real_1))
print(max(abs(y_pred_2 - y_real_2) / y_real_2))
print(max(abs(y_pred_3 - y_real_3) / y_real_3))

# generowanie modeli dla etapu 3
m3_data0 = genfromtxt('data/M3_data0.csv', delimiter=',')

mlpr3_1 = MLPRegressor(hidden_layer_sizes=(24, 12,), max_iter=100000,
                       solver='lbfgs')

x = m3_data0[:, [0, 4]]

y1 = m3_data0[:, 5]

y1_ = mlpr3_1.fit(x, y1)

m3_dataTest = genfromtxt('data/M3_dataTest.csv', delimiter=',')

x_pred = m3_dataTest[:, [0, 4]]
y_pred_1 = mlpr3_1.predict(x_pred)

pickle.dump(mlpr3_1, open("model3_1.p", "wb"))

y_real_1 = m3_dataTest[:, 5]

print("Bledy dla modeli etapu 3:")
print(max(abs(y_pred_1 - y_real_1) / y_real_1))


class AbstractLoadStage(CallsStage):
    def __init__(self, name, max_calls, input_vector,
                 maximum_acceptable_quality,
                 control_params, lower_bounds, upper_bounds):
        super().__init__(name, max_calls, input_vector,
                         maximum_acceptable_quality)
        self.control_params = control_params
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds


class LeadStage1(AbstractLoadStage):
    @staticmethod
    def get_output_of_stage(input_vector, control_params):
        """

        Args:
            input_vector (list): Pb, Sb
            control_params: Air

        Returns:
            list: [Pb, O_2, Zn, Sb]
        """
        vec = input_vector[0:2] + control_params[0:1]
        res = [mlpr1_1.predict(vec), mlpr1_2.predict(vec)]
        output = [input_vector[0], input_vector[1], res[0], res[1]]
        return output

    def get_quality(self, input_vector=None, control_params=None):
        """

        Args:
            input_vector:
            control_params:

        Returns:
            float: quality
        """
        vec = input_vector[0:2] + control_params[0:1]
        res = mlpr1_3.predict(vec)
        return res


class LeadStage2(AbstractLoadStage):
    @staticmethod
    def get_output_of_stage(self, input_vector, control_params):
        """

        Args:
            self:
            input_vector (list): output of stage 1
            control_params (list): Fuel, O2

        Returns:
            list: Pb, Sb
        """
        vec = input_vector + control_params[0:2]
        res = [mlpr2_2.predict(vec), mlpr2_3.predict(vec)]
        return res

    def get_quality(self, input_vector=None, control_params=None):
        vec = input_vector + control_params[0:2]
        res = mlpr2_1.predict(vec)
        return res


class LeadStage3(AbstractLoadStage):
    @staticmethod
    def get_output_of_stage(input_vector, control_params):
        """

        Args:
            input_vector (list): Pb,Sb
            control_params (list): Fuel,O_2,N_2

        Returns:
            float: Pb
        """
        vec = input_vector[0:2] + control_params[0:3]
        res = [mlpr3_1.predict(vec)]
        return res

    def get_quality(self, input_vector=None, control_params=None):
        """

        Args:
            input_vector (list): Pb,Sb
            control_params (list): Fuel,O_2,N_2

        Returns:
            float: Pb
        """
        vec = input_vector[0:2] + control_params[0:3]
        res = mlpr3_1.predict(vec)
        return res


class LeadProcess(AbstractProcess):
    pass


process = LeadProcess()
# TODO: Params to set
MAX_CALLS = 1000
INPUT_VECTOR = [30, 20]
EXPECTED_QUALITY_1 = 0.001
stage1 = LeadStage1("LeadStage1", MAX_CALLS, INPUT_VECTOR, EXPECTED_QUALITY_1,
                    (0,), [607.7], [643.9])
stage2 = LeadStage2("LeadStage2", MAX_CALLS, [], EXPECTED_QUALITY_1, (0, 0),
                    [20, 49.7], [50, 84.4])
stage3 = LeadStage3("LeadStage3", MAX_CALLS, [], EXPECTED_QUALITY_1, (0, 0, 0),
                    [20, 71.9, 5.6], [30, 107, 399])
process.add_edge(stage1, stage2)
process.add_edge(stage2, stage3)

ordered_stages = [stage1, stage2, stage3]
GROUPING_STRATEGY = GroupingStrategy(ordered_stages)
GROUPING_STRATEGY.define_group(ordered_stages)

OPTIMIZATION_STRATEGY = CallsOptimizationStrategy()

pso_algorithm = PsoAlgorithm(process, GROUPING_STRATEGY, OPTIMIZATION_STRATEGY)
pso_algorithm.run()

print("Result: " + pso_algorithm.process.optimization_status)
