import sys, os

files_path = sys.argv[1]
result_path = sys.argv[2]
n = int(sys.argv[3])

def prep(n, files_path, result_path):
	files_list = os.listdir(files_path)
	print(files_list)
	with open(result_path, 'a+') as f:
		for i in range(len(files_list) // n):
			f.write(' '.join(files_list[n*i:n*(i+1)]) + '\n')
			# print(files_list[n*i:(n+1)*i])
		f.write(' '.join(files_list[(len(files_list)//n) * n:]))

if __name__ == '__main__':
	prep(n, files_path, result_path)