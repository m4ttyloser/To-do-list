todo_list = []

while True:
    print('+----------------------------+')
    print('1.Add task')
    print('2.Remove task')
    print('3.Show task')
    print('4.Quit program')
    print('+----------------------------+')

    pick = int(input('Your action:'))

    if pick == 1:
        task = input('Enter task:').lower()
        todo_list.append(task)
    
    elif pick == 2:
        
        for i in todo_list:
            y = 1
            print(f'{y}.{i}')
            y += 1
        
        remove = input('What task do you want to remove:').lower()

        if remove in todo_list:
            todo_list.remove(remove)
            print('task removed')
        else:
            print('Task not found!')

    elif pick == 3:
        z = 1
        for x in todo_list:
            print(f'{z}.{x}')
            z += 1

    elif pick == 4:
        print('Exiting')
        break

    else:
        print('Number is not recognized')