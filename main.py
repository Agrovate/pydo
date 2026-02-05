import argparse
import psycopg2

conn = psycopg2.connect(
                database='todo',
                user = 'nishant',
                password='',
                host = '127.0.0.1',
                port = 5432
        )

curr = conn.cursor()
curr.execute("select * from tasks;")
tasks = curr.fetchall()

#Add Task
def add(args):
    if args.task == None:
        print("Task name not given")
        exit()

    curr.execute('''insert into tasks(task, description, status)
                 values(%s, %s, %s)''',
                 (args.task, args.desc, args.status)
    )
    print(f"{args.task} successfully")
    conn.commit()



#Delete Task
def dele(args):
    global tasks
    curr.execute('delete from tasks where id = %s returning *',args.id)
    print("Deleted successfully")
    conn.commit()

def mod(args):
    global tasks
    
    if args.id != None:
        curr.execute('''
            update tasks
            set task = coalesce(%s, task),
                description = coalesce(%s, description),
                status = coalesce(%s, status)
            where id = %s
            returning *;
                 ''',
            (args.task, args.desc, args.status, args.id)
        )
        conn.commit()
    else:
        print("no id")

def show(args):
    curr.execute("select * from tasks;")
    tasks = curr.fetchall()
   
    print("ID\tTASK\tDESCRIPTION\t\t\tSTATUS")
    for task in tasks:
        id, name, desc, status = task
        print(f"{id}\t{name}\t{desc}\t\t{status}")



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
mod_parser.add_argument('--desc', '-d')
mod_parser.add_argument('--status', '-s')
mod_parser.set_defaults(func=mod)

#Display
show_parser = subparser.add_parser('show')
show_parser.set_defaults(func=show)


args = parser.parse_args()

if hasattr(args, 'func'):
    args.func(args)

conn.close()
