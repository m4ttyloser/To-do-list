while True:
    todo_list = []

    print('1.Add task')
    print('2.Remove task')
    print('3.Show task')
    print('Quit program')

    pick = int(input('Your action:'))

    if pick == 1:
        task = input('Enter task:')
        todo_list.append(task)
    
    elif pick == 2:
        
        for i in todo_list:
            y = 1
            print(f'{y}.{i}')
            y += 1
        
        remove = int(input('Whats the number of task you want to remove:'))