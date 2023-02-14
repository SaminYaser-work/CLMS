def print_title() -> None:
    title = '''
                                           .         .                         
    ,o888888o.    8 8888                  ,8.       ,8.            d888888o.   
   8888     `88.  8 8888                 ,888.     ,888.         .`8888:' `88. 
,8 8888       `8. 8 8888                .`8888.   .`8888.        8.`8888.   Y8 
88 8888           8 8888               ,8.`8888. ,8.`8888.       `8.`8888.     
88 8888           8 8888              ,8'8.`8888,8^8.`8888.       `8.`8888.    
88 8888           8 8888             ,8' `8.`8888' `8.`8888.       `8.`8888.   
88 8888           8 8888            ,8'   `8.`88'   `8.`8888.       `8.`8888.  
`8 8888       .8' 8 8888           ,8'     `8.`'     `8.`8888.  8b   `8.`8888. 
   8888     ,88'  8 8888          ,8'       `8        `8.`8888. `8b.  ;8.`8888 
    `8888888P'    8 888888888888 ,8'         `         `8.`8888. `Y8888P ,88P' 

                                                     Yaser, Samin - 19-39442-1
    '''
    print(title)


STATUS = ['ACTIVE', 'INACTIVE', 'BROKEN', 'UNKNOWN']
OS = ['WINDOWS', 'MAC', 'LINUX', 'UNKNOWN']


# Test data
data = [
    {
        "id": 1,
        "status": STATUS[0],
        "os": OS[0]
    },
    {
        "id": 2,
        "status": STATUS[1],
        "os": OS[1]
    },
    {
        "id": 3,
        "status": STATUS[2],
        "os": OS[2]
    },
]


def todo():
    print('TODO')


def is_id_unique(id: int) -> bool:
    if id in [pc['id'] for pc in data]:
        return False
    return True


def print_exception_msg(msg: str) -> None:
    print(f'\nError: {msg} must be an integer\n')


def print_invalid_choice_msg() -> None:
    print('\nInvalid choice\n')


def get_os_and_status() -> None:
    for os in OS:
        print(f'{OS.index(os) + 1}: {os}')

    while True:
        try:
            os_choice = int(input('Choose OS: ')) - 1
            if os_choice >= 0 and os_choice < len(OS):
                break
            else:
                print_invalid_choice_msg()
        except:
            print_exception_msg('OS')

    for idx, status in enumerate(STATUS):
        print(f'{idx + 1}: {status}')

    while True:
        try:
            status_choice = int(input('Choose status: ')) - 1
            if status_choice >= 0 and status_choice < len(STATUS):
                break
            else:
                print_invalid_choice_msg()
        except:
            print_exception_msg('Status')

    return os_choice, status_choice


def add_new_pc() -> None:
    while True:
        try:
            id = int(input('Enter ID: '))
            break
        except ValueError:
            print_exception_msg('ID')

    if not is_id_unique(id):
        print('ID already exists')
        # TODO: ask if user wants to update or remove the PC
        return

    os_choice, status_choice = get_os_and_status()

    data.append({
        "id": id,
        "status": STATUS[status_choice],
        "os": OS[os_choice]
    })

    print('\nPC added successfully\n')


def update_pc() -> None:
    print('\nUpdate PC\n')
    while True:
        try:
            id = int(input('Enter ID to Update (0 to go back): '))
            if id == 0:
                print('\nCancelling Update...\n')
                return
            if id in [pc['id'] for pc in data]:
                break
            else:
                print('\nID not found\n')
        except ValueError:
            print_exception_msg('ID')

    os_choice, status_choice = get_os_and_status()

    for pc in data:
        if pc['id'] == id:
            pc['status'] = STATUS[status_choice]
            pc['os'] = OS[os_choice]
            break

    print(f'\nPC with ID {id} updated successfully\n')


def remove_pc() -> None:
    print('\nRemove PC\n')
    while True:
        try:
            id = int(input('Enter ID to Remove (0 to go back): '))
            if id == 0:
                print('\nCancelling Remove...\n')
                return
            if id in [pc['id'] for pc in data]:
                break
            else:
                print('\nID not found\n')
        except ValueError:
            print_exception_msg('ID')

    confirm = input(
        f'Are you sure you want to remove PC with ID {id}? (y/n): ')
    if confirm != 'y':
        print('\nCancelling Remove...\n')
        return

    for pc in data:
        if pc['id'] == id:
            data.remove(pc)
            break

    print(f'\nPC with ID {id} removed successfully from database\n')


def search_pc():
    print('\nSearch PC\n')

    res = []

    print('Search by: ')
    print('1: ID')
    print('2: Status')
    print('3: OS')

    method = int(input('Enter search method: '))
    if method == 1:
        while True:
            try:
                id = int(input('Enter ID to Search (0 to go back): '))
                if id == 0:
                    print('\nCancelling Search...\n')
                    return
                if id in [pc['id'] for pc in data]:
                    break
                else:
                    print('\nID not found\n')
            except ValueError:
                print_exception_msg('ID')
    elif method == 2:
        status = input(
            'Enter Status to Search (0 to go back): ').lower()

        if status == '0':
            print('\nCancelling Search...\n')
            return

        for d in data:
            print(d)
            if d['status'].lower() == status:
                res.append(d)

    elif method == 3:
        os = input('Enter OS to Search (0 to go back): ').lower()
        if os == '0':
            print('\nCancelling Search...\n')
            return

        for d in data:
            if d['os'].lower() == os:
                res.append(d)

    else:
        print('Invalid choice')

    if res:
        print(f'\n{len(res)} PC(s) found\n')
        show_pc(res)
    else:
        print('No match found')


def show_pc(pc_list=data) -> None:
    print('\n%-5s' % 'ID', '%-17s' % 'Status', '%-17s' % 'OS')
    print('-' * 50)
    for pc in pc_list:
        print('%-5i' % pc['id'], '%-17s' % pc['status'], '%-17s' % pc['os'])


def main_menu() -> None:
    menu = '''
    1. Add new PC
    2. Update PC
    3. Remove PC
    4. Show all PCs
    5. Search PC

    Type 'quit' to exit
    '''
    print('-' * 80)

    while True:
        print()
        print(menu)
        choice = input('\nEnter your choice: ')
        if choice == '1':
            add_new_pc()
        elif choice == '2':
            update_pc()
        elif choice == '3':
            remove_pc()
        elif choice == '4':
            # TODO: Show the number of PCs
            show_pc()
        elif choice == '5':
            search_pc()
        elif choice == 'quit':
            break
        else:
            print('Invalid choice')


def start_program():
    print_title()
    main_menu()
    print('Quitting...')


if __name__ == '__main__':
    start_program()