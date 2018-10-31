import unittest

class StatsCollectorTest(unittest.TestCase):

    def test_remove_empty_stats_from_final_list(self):
        """
        O método build_statistic_for_response() deve retornar None caso a task
        em questão não tenha estatisticas anteriores já no cache.

        Os cálculos são feitos apenas quando já temos uma leitura anterior.
        """
        self.fail()
