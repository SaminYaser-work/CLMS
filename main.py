from bcolors import bcolors as b


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

# TODO: Add docstrings to all functions
# TODO: Every function should have a return type
# TODO: Every function's parameter should have a type


def todo():
    print('TODO')


# TODO: Implement save and load data
def save_data() -> None:
    todo()


def load_data() -> None:
    todo()


def is_id_unique(id: int) -> bool:
    if id in [pc['id'] for pc in data]:
        return False
    return True


def print_exception_msg(msg: str) -> None:
    print(f'\nError: {msg} must be an integer\n')


def print_invalid_choice_msg() -> None:
    print('\nInvalid choice\n')


def get_os_and_status() -> None:

    print('\nWhat is the Operating System of the PC?')
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

    print('\nWhat is the current status of the PC?')
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
        print(f'\nID {id} already exists')
        show_pc(id=id)
        print('\nWhat do you want to do?')
        while True:
            try:
                choice = int(input('\n1: Update\n2: Remove\n3: Cancel\n'))
                if choice == 1:
                    print(f'\nUpdating ID {id}...\n')
                    update_pc(showTitle=False, id=id)
                    return
                elif choice == 2:
                    remove_pc(showTitle=False, id=id)
                    return
                elif choice == 3:
                    print('\nCancelling Add...\n')
                    return
                else:
                    print_invalid_choice_msg()
            except ValueError:
                print_exception_msg('Choice')

    os_choice, status_choice = get_os_and_status()

    data.append({
        "id": id,
        "status": STATUS[status_choice],
        "os": OS[os_choice]
    })

    print('\nPC added successfully\n')


def update_pc(showTitle: bool = True, id: int = -1) -> None:

    if showTitle:
        print('\nUpdate PC\n')

    while True:
        try:
            if id == -1:
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


def remove_pc(showTitle: bool = True, id: int = -1) -> None:

    if showTitle:
        print('\nRemove PC\n')

    while True:
        try:
            if id == -1:
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
    print('0: Main menu')

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

    elif method == 0:
        return

    else:
        print('Invalid choice')

    if res:
        print(f'\n{len(res)} PC(s) found\n')
        show_pc(res)
    else:
        print('No match found')


def show_pc(id=-1, pc_list=data) -> None:

    if id != -1:
        pc_list = [pc for pc in pc_list if pc['id'] == id]

    print(f"\nTotal {len(pc_list)} PC found in Database")
    print('\n%-5s' % 'ID', '%-17s' % 'Status', '%-17s' % 'OS')
    print('-' * 50)
    for pc in pc_list:
        print('%-5i' % pc['id'], '%-17s' % pc['status'], '%-17s' % pc['os'])


def main_menu() -> None:
    menu = f'''
    {b.HEADER}{b.UNDERLINE}Menu:{b.ENDC}{b.ENDC}

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
        print('~' * 30 + '\n')
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
    print('Quitting...')  # TODO: Save before quitting


if __name__ == '__main__':
    start_program()
