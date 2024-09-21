from dataclasses import dataclass
from typing import List, Union
from time import time 

import numpy as np
import sys

# Part two reverses (is a seed with location one in the book? what about location two...) part one because I only have 
# to check 84,999,999 options before hitting the solution while if you go forward, you need to compute the values of 
# 2,549,759,327 seeds to find the min value meaning I only had to do 3% of the work so it takes a single minute.

seeds = [] # [(start, end), ...]

@dataclass
class Mapping_Range():
	destination_range_start: int
	source_range_start: int
	range_length: int
	def __init__(self, string):
		self.destination_range_start, self.source_range_start, self.range_length = [int(i) for i in string.split(" ")]

@dataclass
class Mapping():
	title: str
	mapping_ranges: List[Mapping_Range]
	previous_mapping: Union[None, "Mapping"] = None

def parse(file_name:str) -> List[Mapping]:
	file = open(file_name, "r")
	lines = [line for line in file.read().splitlines() if line != ""]
	file.close()
	
	global seeds
	seeds_values = [int(i) for i in lines[0].split(" ")[1:]]
	seeds = [(seeds_values[i*2], seeds_values[i*2] + seeds_values[i*2+1]) for i in range(int(len(seeds_values)/2))]
	
	title, maps, mapping_objects = "", [], []
	for line in lines[1:]:
		if line[0].isalpha():
			if title != "":
				mapping_objects.append(Mapping(
					title=title, 
					mapping_ranges=[Mapping_Range(map) for map in maps]
				))
				if len(mapping_objects) > 1: mapping_objects[-1].previous_mapping = mapping_objects[-2]
			title, maps= line[:-1], []
		else: maps.append(line)
	# mapping_objects.append(Mapping(
	# 	title=title, 
	# 	mapping_ranges=[Mapping_Range(map) for map in maps],
	# 	previous_mapping=mapping_objects[-2]
	# ))
	return mapping_objects + [Mapping(
		title=title, 
		mapping_ranges=[Mapping_Range(map) for map in maps],
		previous_mapping=mapping_objects[-2]
	)]

def part_two(mappings):
	steps = 5_000_000
	for i in range(sys.maxsize):
		indices = np.arange(steps, dtype=np.uintc) + steps * i
		print(f"working on {indices[0]} to {indices[-1]}")
		
		for mapping in mappings:
			new_indices = np.zeros(indices.shape, dtype=np.uintc)
			
			for rule in mapping.mapping_ranges:
				condition = np.logical_and(
					indices >= rule.destination_range_start, 
					indices < rule.destination_range_start + rule.range_length
				)
				new_indices[condition] = indices[condition] - rule.destination_range_start + rule.source_range_start
			indices = np.where(new_indices != 0, new_indices, indices)
		
		are_seeds = np.zeros(indices.shape, dtype=np.uintc)
		for seed in seeds: are_seeds |= (indices >= seed[0]) & (indices < seed[1])
		highest_value = np.argmax(are_seeds)
		
		if are_seeds[highest_value] == 1:
			print(f"\n\nthe answer is {int(highest_value)+steps*i}")
			break
		else: print("no answer\n")
		

if __name__ == "__main__":
	start = time()
	# mappings = parse("example.txt")
	mappings = parse("input.txt")
	mappings.reverse()
	part_two(mappings)
	print(f"the total time is {time() - start} seconds")
