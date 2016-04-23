import sys

def parseLine(line):
	s = ''
	field = 0
	d = 0
	data = []
	for c in line:
		if (c != ','):
			s = s + c
		else:
			if (field == 0):
				d = int(s)
			else:
				d = float(s)
			field += 1
			s = ''
			data.append(d)
	d = float(s)
	data.append(d)
	data.append(1)
	return (data)

all_data = 'data.txt'
main_data = 'data_avg.txt'
if (len(sys.argv)>1):
	all_data = sys.argv[1]
if (len(sys.argv)>2):
	main_data = sys.argv[2]
out_file = open(main_data,'w')
data_list = []
with open(all_data,'r') as f:
	for line in f:
		data = parseLine(line)
		i = 0
		match = False
		while (i < len(data_list)):
			data_element = data_list[i]
			if (data_element[0] == data[0]):
				match = True
				j = 1
				while (j < len(data_list[i])):
					data_list[i][j] += data[j]
					j += 1
				break
			i += 1
		if (match == False):
			data_list.append(data)
i = 0
output_list = []
while (i < len(data_list)):
	item_id = data_list[i][0]
	item_ratio = data_list[i][1]
	item_b = data_list[i][2]
	item_g = data_list[i][3]
	item_r = data_list[i][4]
	num = data_list[i][5]
	item_ratio = item_ratio / num
	item_b = item_b / num
	item_g = item_g / num
	item_r = item_r / num
	item_data = [item_id,item_ratio,item_b,item_g,item_r]
	output_list.append(item_data)
	i += 1
i = 0
o = open(main_data,'w')
while (i<len(output_list)):
	output = str(output_list[i][0]) + ',' + str(output_list[i][1]) + ',' + str(output_list[i][2]) + ',' + str(output_list[i][3]) + ',' + str(output_list[i][4]) + '\n'
	o.write(output)
	i += 1
exit()
