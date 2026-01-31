import argparse

class Task:
    def __init__(self, task, desc, status) -> None:
        self.task = task
        self.desc = desc
        self.status = status

t_id = 1 
tasks = {}

#Add Task
def add(args):
    if args.task == None:
        print("Task name not given")
        exit()
    
    tasks[t_id] = Task(args.task, args.desc, args.status)
    print(tasks[1].task)


#Delete Task
def dele(args):
    global tasks
    val = tasks[0]
    if  args.id != None:
        val = tasks.pop(args.id, None)

    print(val.task, "is popped")

def mod(args):
    global tasks

    if args.id != None:
        tasks[t_id].status = args.status 



parser = argparse.ArgumentParser(
        prog='pydo',
        description='a python cli tool for creating and managing todo lists'
)

#Add tasks
subparser = parser.add_subparsers()
add_parser = subparser.add_parser('add')
add_parser.add_argument('--task', '-t')
add_parser.add_argument('--desc', '-d')
add_parser.add_argument('--status', '-s')
add_parser.set_defaults(func=add)

#Delete tasks
del_parser = subparser.add_parser('del')
del_parser.add_argument('--id', '-i')
del_parser.set_defaults(func=dele)

#Change status
mod_parser = subparser.add_parser('mod')
mod_parser.add_argument('--task', '-t')
mod_parser.add_argument('--id', '-i')
mod_parser.add_argument('--status', '-s')
del_parser.set_defaults(func=mod)

args = parser.parse_args()


if hasattr(args, 'func'):
    args.func(args)
