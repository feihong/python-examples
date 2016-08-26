import threading


def task(n, label):
    import time
    for i in range(n):
        print('%d %s' % (i, label))
        time.sleep(0.1)


thread = threading.Thread(target=task, args=(10, 'topsy'))
thread.start()
print('Thread was started')
thread.join()
print('Thread finished')
