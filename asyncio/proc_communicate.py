import asyncio
from asyncio.subprocess import PIPE


async def main():
    # cmd = ['ls', '.']
    # cmd = ['ls', 'abc']
    # cmd = ['rapydscript', 'hello.py']
    cmd = ['rapydscript', 'task_cancel.py']

    proc = await asyncio.create_subprocess_exec(*cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = await proc.communicate()
    print('stdout:')
    print(stdout.decode('utf-8'))
    print('stderr:')
    print(stderr.decode('utf-8'))
    print(proc.returncode)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()        # prevents annoying signal handler error
