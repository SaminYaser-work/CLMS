from bcolors import bcolors as bc
from FileIO import FileIO

STATUS = ['ACTIVE', 'INACTIVE', 'BROKEN', 'UNKNOWN']
OS = ['WINDOWS', 'MAC', 'LINUX', 'UNKNOWN']
CTRLS = ['Add New PC', 'Update PC', 'Remove PC', 'Show All PCs', 'Search PC']
DB_FILE = 'db.json'
io = FileIO(DB_FILE)
b = bc()


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
    print(b.success(title))

# TODO: Add docstrings to all functions
# TODO: Every function should have a return type
# TODO: Every function's parameter should have a type
# TODO: Use Match instead of if-else


def is_id_unique(id: int) -> bool:
    data = io.load()
    if id in [pc['id'] for pc in data]:
        return False
    return True


def is_valid_id(id: int) -> bool:
    return id > 0


def get_pc_by_id(id: int) -> dict:
    data = io.load()
    for pc in data:
        if pc['id'] == id:
            return pc
    return {}


def print_exception_msg(msg: str) -> None:
    print(f'\n{b.error("Error")} {msg} must be a non-zero positive integer\n')


def print_invalid_choice_msg() -> None:
    print(f'\n{b.warning("Invalid choice")}\n')


def take_input(msg: str, exp_msg: str) -> int:
    while True:
        try:
            inp = int(input(msg))
            if inp > 0:
                return inp
            else:
                print_exception_msg(exp_msg)
        except ValueError:
            print_exception_msg(exp_msg)
        except Exception as e:
            print(b.error('Error:'), str(e))


def print_table(data: list, showCountMsg='') -> None:

    if not showCountMsg:
        print(
            f"\nTotal {b.GREEN}{b.BOLD}{len(data)}{b.ENDC} PC(s) found in DB")
    else:
        print(showCountMsg)

    print(f'\n{b.HEADER}{b.BOLD}%-5s' % 'ID', '%-17s' %
          'OS', '%-17s' % f'Status {b.ENDC}')
    print(f'{b.CYAN}' + '-' * 33 + f'{b.ENDC}')
    for pc in data:
        status = ''
        match pc['status'].lower():
            case 'active':
                status = b.success(pc['status'])
            case 'inactive':
                status = b.warning(pc['status'])
            case 'broken':
                status = b.error(pc['status'])
            case _:
                status = pc['status']

        print('%-5i' % pc['id'], '%-17s' % pc['os'], '%-17s' % status)


def get_os_and_status(id: int) -> None:

    print(b.warning(text=f'\nWhat is the Operating System of the PC {id}?'))

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

    print(f'\nWhat is the current status of the {b.underline(f"PC {id}")}?')
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

    id = take_input('Enter ID: ', 'ID')

    if not is_id_unique(id):
        print(b.info(f'\nID {id} already exists'))
        print_table([pc for pc in data if pc['id'] == id])
        while True:
            try:
                choice = int(input('\n1: Update\n2: Remove\n3: Cancel\n'))
                match choice:
                    case 1:
                        print(f'\nUpdating ID {id}...\n')
                        update_pc(showTitle=False, id=id)
                        return
                    case 2:
                        remove_pc(showTitle=False, id=id)
                        return
                    case 3:
                        print('\nCancelling Add...\n')
                        return
                    case _:
                        print_invalid_choice_msg()
            except ValueError:
                print_exception_msg('Choice')

    os_choice, status_choice = get_os_and_status(id)

    data = io.load()
    data.append({
        "id": id,
        "status": STATUS[status_choice],
        "os": OS[os_choice]
    })
    io.save(data)

    print(b.success(f'\nPC {id} added to DB'))


def update_pc(showTitle: bool = True, id: int = -1) -> None:

    if showTitle:
        print(b.subtitle('\nUpdate PC\n'))

    if id == -1:
        id = take_input('Enter ID to Update (0 to go back): ', 'ID')
        if id == 0:
            print('\nCancelling Update...\n')
            return

    pc = get_pc_by_id(id)

    if not pc:
        print('\n' + b.error(f'ID {id} not found in DB'))
        return

    os_choice, status_choice = get_os_and_status(id)

    data = io.load()
    for pc in data:
        if pc['id'] == id:
            pc['status'] = STATUS[status_choice]
            pc['os'] = OS[os_choice]
            break
    io.save(data)

    print(b.success(f'\nPC {id} updated successfully'))


def remove_pc(showTitle: bool = True, id: int = -1) -> None:

    if showTitle:
        print(b.subtitle('\nRemove PC\n'))

    data = io.load()

    if id == -1:
        id = take_input('Enter ID to Remove (0 to go back): ', 'ID')
        if id == 0:
            print('\nCancelling Remove...\n')
            return

    if id not in [pc['id'] for pc in data]:
        print(b.error(f'\nPC with ID {id} not found in DB\n'))
        id = -1

    pc = [pc for pc in data if pc['id'] == id][0]
    print_table([pc])

    confirm = input(
        b.warning(f'\nAre you sure you want to remove PC with ID {id}? (y/N): '))
    if confirm != 'y':
        print('\nCancelling Remove...\n')
        return

    for pc in data:
        if pc['id'] == id:
            data.remove(pc)
            io.save(data)
            break

    print(b.success(f'\nPC with ID {id} removed successfully from DB\n'))


def search_pc() -> None:
    print(b.subtitle('\nSearch PC\n'))

    res = []

    print(b.underline('Search by:\n'))
    print('1: ID')
    print('2: Status')
    print('3: OS\n')
    print('0: Main menu')

    text = ''

    method = int(input('Enter search method: '))
    if method == 1:
        id = take_input('Enter ID to Search (0 to go back): ', 'ID')
        if id == 0:
            print('\nCancelling Search...\n')
            return

        pc = get_pc_by_id(id)

        if pc:
            res.append(pc)
            text = f'\nPC with ID {id} found in DB'
        else:
            print(b.error(f'\nPC with ID {id} not found in DB'))
            return

    elif method == 2:
        status = input(
            'Enter Status to Search (0 to go back): ').lower()

        if status == '0':
            print('\nCancelling Search...\n')
            return

        for d in io.load():
            if d['status'].lower() == status:
                res.append(d)
        text = b.success(
            f'\nTotal of {len(res)} PC(s) found with status {status}')

    elif method == 3:
        os = input('Enter OS to Search (0 to go back): ').lower()
        if os == '0':
            print('\nCancelling Search...\n')
            return

        for d in io.load():
            if d['os'].lower() == os:
                res.append(d)
        text = b.success(
            f'\nTotal of {len(res)} PC(s) found with OS {os}')

    elif method == 0:
        return

    else:
        print_invalid_choice_msg()

    if res:
        print_table(data=res, showCountMsg=text)
    else:
        print(b.error('\nNo match found in DB'))


def show_all_pc() -> None:
    data = io.load()
    text = f"\nTotal {b.GREEN}{b.BOLD}{len(data)}{b.ENDC} PC(s) found in DB"
    print_table(data=data, showCountMsg=text)


def main_menu() -> None:
    ctrls = ''.join([b.info(str(i + 1) + ': ') +
                     ctrl + '\n' for i, ctrl in enumerate(CTRLS)])

    quitText = f"Type {b.info('quit')} to exit"
    menu = b.title('Menu:') + '\n' + ctrls + '\n' + quitText

    print('-' * 80)

    while True:
        print()
        print(menu)
        choice = input('\nEnter your choice: ')
        print('~' * 30 + '\n')

        match choice:
            case '1':
                add_new_pc()
            case '2':
                update_pc()
            case '3':
                remove_pc()
            case '4':
                show_all_pc()
            case '5':
                search_pc()
            case 'quit':
                break
            case _:
                print_invalid_choice_msg()


def start_program() -> None:
    print_title()
    main_menu()
    print('Quitting...')  # TODO: Save before quitting


if __name__ == '__main__':
    start_program()
