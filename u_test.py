import unittest
from tournament import preventRematch


# def preventRematch(all_pairs, pairs_list):
#     """Checking if any pair from current (for this round) pairs list is
#        already is in all_pairs list (list of pairs for all rounds) and
#        fixing this by shuffeling players
#     Args:
#       all_pairs: 'all_pairs' - list of all pairs for all rounds,
#                   looks like [(id1, name1, id2, name2),()...]
#       pairs_list: list of pairs for current round, looks like
#                   [(id1, name1, id2, name2),()...]
#     Returns:
#       pairs_list: A list of fixed pairs
#                   [(id_fixed, name_fixed, id2, name2),()...]
#     """


class TestFunction(unittest.TestCase):

    def setUp(self):
        """for all cases, all_pairs (matches that were hold)
            list first; then pairs_list (matches for cur round)"""
        self.test_list = (
            # first test case
            ([(1, 'testa', 2, 'testb')],  # matches that were hold
             [(1, 'testa', 2, 'testb'), (3, 'testc', 4, 'testd')]),
            # second test case
            ([(1, 'testa', 2, 'testb'), (1, 'testa', 3, 'testc')],
             [(1, 'testa', 2, 'testb'), (3, 'testc', 4, 'testd')]),
            # third case, odd number of players
            ([(1, 'testa', 2, 'testb'), (1, 'testa', 3, 'testc'),
              (5, 'teste', 6, 'BYE')],
             [(1, 'testa', 2, 'testb'), (3, 'testc', 4, 'testd'),
              (5, 'teste', 6, 'BYE')]),
        )
        """I expect that players
            would be shuffeled like this"""
        self.expected_output = (
            # for the first test case i excpect
            [(1, 'testa', 3, 'testc'), (2, 'testb', 4, 'testd')],
            # for the second test case i excpect
            [(1, 'testa', 4, 'testd'), (3, 'testc', 2, 'testb')],
            # for the third test case i excpect
            [(1, 'testa', 4, 'testd'), (3, 'testc', 5, 'teste'),
             (2, 'testb', 6, 'BYE')],
        )

    def test_func(self):
        for ind, case in enumerate(self.test_list):
            self.assertEqual(
                preventRematch(case[0], case[1]), self.expected_output[ind]
            )


if __name__ == '__main__':
    unittest.main()
