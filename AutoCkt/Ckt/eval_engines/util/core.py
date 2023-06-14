import numpy as np
import sys
from copy import deepcopy, copy

class IDEncoder(object):
    # example: input = [1,2,3], bases = [10, 3, 8]
    # [10, 3, 8] -> [3x8, 8, 0]
    # [1, 2, 3] x [3x8, 8, 0] = [24, 16 , 0] -> 24+16+0 = 40
    # 40 -> [k] in base 62 (0,...,9,a,...,z,A,....,Z) and then we pad it to [0,k] and then return '0k'

    def __init__(self, params_vec):
        self._bases = np.array([len(vec) for vec in params_vec.values()])
        self._mulipliers = self._compute_multipliers()
        self._lookup_dict = self._create_lookup()
        self.length_letters = self._compute_length_letter()

    def _compute_length_letter(self):
        cur_multiplier = 1
        for base in self._bases:
            cur_multiplier = cur_multiplier * base

        max_number = cur_multiplier
        ret_vec = self._convert_2_base_letters(max_number)
        return len(ret_vec)

    @classmethod
    def _create_lookup(cls):
        lookup = {}
        n_letters = ord('z') - ord('a') + 1
        for i in range(10):
            lookup[i] = str(i)
        for i in range(n_letters):
            lookup[i+10] = chr(ord('a')+i)
        for i in range(n_letters):
            lookup[i+10+n_letters] = chr(ord('A')+i)
        return lookup

    def _compute_multipliers(self):
        """
        computes [3x8, 8, 0] in our example
        :return:
        """
        cur_multiplier = 1
        ret_list = []
        for base in self._bases[::-1]:
            cur_multiplier = cur_multiplier * base
            ret_list.insert(0, cur_multiplier)
            assert cur_multiplier < sys.float_info.max, 'search space too large, cannot be represented by this machine'

        print(cur_multiplier)
        ret_list[:-1] = ret_list[1:]
        ret_list[-1] = 0
        return np.array(ret_list)

    def _convert_2_base_10(self, input_vec):
        assert len(input_vec) == len(self._bases)
        return np.sum(np.array(input_vec) * self._mulipliers)

    def _convert_2_base_letters(self, input_base_10):
        x = input_base_10
        ret_list = []
        while x:
            key = int(x % len(self._lookup_dict))
            ret_list.insert(0, self._lookup_dict[key])
            x = int(x / len(self._lookup_dict))

        return ret_list

    def _pad(self, input_base_letter):
        while len(input_base_letter) < self.length_letters:
            input_base_letter.insert(0, '0')
        return input_base_letter

    def convert_list_2_id(self, input_list):
        base10 = self._convert_2_base_10(input_list)
        base_letter = self._convert_2_base_letters(base10)
        padded = self._pad(base_letter)
        return ''.join(padded)


class Design(list):

    def __init__(self, spec_range, id_encoder, seq=()):
        """
        :param spec_range: Dict[Str : [a,b]] -> kwrds are used for spec property creation of
        Design objects
        :param seq: input parameter vector as a List
        """
        list.__init__(self, seq)
        self.cost =     None
        self.fitness =  None
        self.specs = {}
        # uniquely determines the id of the design given the list values
        self.id_encoder = id_encoder
        self.spec_range = spec_range
        for spec_kwrd in spec_range.keys():
            self.specs[spec_kwrd] = None

        self.parent1 = None
        self.parent2 = None
        self.sibling = None

    def set_parents_and_sibling(self, parent1, parent2, sibling):
        self.parent1 = parent1
        self.parent2 = parent2
        self.sibling = sibling

    def is_init_population(self):
        if self.parent1 is None:
            return True
        else:
            return False
    def is_mutated(self):
        if self.parent1 is not None:
            if self.parent2 is None:
                return True
        else:
            return False

    @property
    def id(self):
        return self.id_encoder.convert_list_2_id(list(self))

    @property
    def cost(self):
        return self.__cost

    @property
    def fitness(self):
        return self.__fitness

    @cost.setter
    def cost(self, x):
        self.__cost = x
        self.__fitness = -x if x is not None else None

    @fitness.setter
    def fitness(self, x):
        self.__fitness = x
        self.__cost = -x if x is not None else None

    @staticmethod
    def recreate_design(spec_range, old_design, eval_core):
        dsn = Design(spec_range, eval_core.id_encoder, old_design)
        dsn.specs.update(**old_design.specs)
        for attr in dsn.__dict__.keys():
            if (attr in old_design.__dict__.keys()) and (attr not in ['specs']):
                dsn.__dict__[attr] = deepcopy(old_design.__dict__[attr])
        return dsn

    @staticmethod
    def genocide(*args):
        for dsn in args:
            dsn.parent1 = None
            dsn.parent2 = None
            dsn.sibling = None

    def copy(self):
        new = copy(self)
        new.specs = deepcopy(self.specs)
        return new