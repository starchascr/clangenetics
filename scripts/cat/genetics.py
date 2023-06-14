import random

import ujson

from scripts.game_structure.game_essentials import game

class Genetics:
	def __init__(self,
				locus_a=None,
				locus_b=None
				):
		self.locus_a = locus_a if locus_a else []
		self.locus_b = locus_b if locus_b else []

	def check_load_genetics(cat):

	        if not cat.genotype:
	            cat.load_genetics()

	@staticmethod
	def make_dict(cat):
		genetics_dict = {
			"locus_a": cat.genotype[:2],
			"locus_b": cat.genotype[2:4],
		}
		return genetics_dict