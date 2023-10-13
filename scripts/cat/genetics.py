import random

import ujson

from scripts.game_structure.game_essentials import game

class Genetics:
	def __init__(self,
				locus_a=None,
				locus_b=None,
				locus_bm=None,
				locus_c=None,
				locus_d=None,
				locus_e=None,
				locus_i=None,
				locus_l=None,
				locus_mc=None,
				locus_o=None,
				locus_sp=None,
				locus_ta=None,
				locus_w=None,
				locus_wb=None
				):
		self.locus_a = locus_a if locus_a else []
		self.locus_b = locus_b if locus_b else []
		self.locus_bm = locus_bm if locus_bm else []
		self.locus_c = locus_c if locus_c else []
		self.locus_d = locus_d if locus_d else []
		self.locus_e = locus_e if locus_e else []
		self.locus_i = locus_i if locus_i else []
		self.locus_l = locus_l if locus_l else []
		self.locus_mc = locus_mc if locus_mc else []
		self.locus_o = locus_o if locus_o else []
		self.locus_sp = locus_sp if locus_sp else []
		self.locus_ta = locus_ta if locus_ta else []
		self.locus_w = locus_w if locus_w else []
		self.locus_wb = locus_wb if locus_wb else []

	def check_load_genetics(cat):
		if not cat.genotype:
			cat.load_genetics()

	@staticmethod
	def make_dict(cat):
		genetics_dict = {
			cat.ID: {
			"locus_a": cat.genotype[:2],
			"locus_b": cat.genotype[2:4],
			"locus_bm": cat.genotype[4:6],
			"locus_c": cat.genotype[6:8],
			"locus_d": cat.genotype[8:10],
			"locus_e": cat.genotype[10:12],
			"locus_i": cat.genotype[12:14],
			"locus_l": cat.genotype[14:16],
			"locus_mc": cat.genotype[16:18],
			"locus_o": cat.genotype[18:20],
			"locus_sp": cat.genotype[20:22],
			"locus_ta": cat.genotype[22:24],
			"locus_w": cat.genotype[24:26],
			"locus_wb": cat.genotype[26:28],
			}
		}
		return genetics_dict
	
	@staticmethod
	def random_genes():
		genes = [["Apb", "A", "a"], ["B", "b", "b1"], ["Bm", "bm"], ["C", "cb", "cm", "cs", "ca", "c"], ["D", "d"], ["E", "er", "e"], ["I", "i"], ["L", "l"], ["Mc", "mc"], ["O", "o"], ["Sp", "sp"], ["Ta", "ta"], ["W", "ws", "w"], ["Wb", "wb"]]
		genew = [[1, 10, 10], [5, 2, 1], [1, 15], [30, 10, 5, 10, 2, 1], [5, 1], [15, 2, 1], [1, 30], [20, 1], [2, 1], [1, 5], [1, 10], [1, 20], [1, 10, 30], [1, 30]]
		i = 0
		geno = []

		while i <= (len(genes)-1):
			a = random.choice(random.choices(genes[i], weights=genew[i]))
			b = random.choice(random.choices(genes[i], weights=genew[i]))
			if genes[i].index(a) <= genes[i].index(b):
				geno.append(a)
				geno.append(b)
			else:
				geno.append(b)
				geno.append(a)
			i += 1
		return geno

	def inheritance_genes(parents):
		pass
		'''genes = [["Apb", "A", "a"], ["B", "b", "b1"], ["Bm", "bm"], ["C", "cb", "cm", "cs", "ca", "c"], ["D", "d"], ["E", "er", "e"], ["I", "i"], ["L", "l"], ["Mc", "mc"], ["O", "o"], ["Sp", "sp"], ["Ta", "ta"], ["W", "ws", "w"], ["Wb", "wb"]]
		par1 = parents[0]
		par2 = parents[1]
		par2_genotype = []
		geno = []

		for p in parents:
			if p:
				Genetics.check_load_genetics(p)
			else:
				par2_genotype = random_genes()

		print(par1.ID)
		a = str(random.choice(par1.genotype.locus_w))
		print(a)
		print(par2.ID)
		b = str(random.choice(par2_genotype[24:26] if par2_genotype else par2.genotype.locus_w))
		print(b)
		if genes[12].index(a) <= genes[12].index(b):
			geno.append(a)
			geno.append(b)
		else:
			geno.append(b)
			geno.append(a)
		print(geno)
		return geno'''


