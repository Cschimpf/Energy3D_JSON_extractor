
def flatten(a_dict):
	newlist = []
	newlist.extend(a_dict.keys())
	newlist.extend(a_dict.values())

	return newlist
