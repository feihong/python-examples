
with open('big_file.txt', 'w') as fp:
    end = int(10e5)
    for i in range(1, end):
        fp.write('%s. 你好\n' % i)
