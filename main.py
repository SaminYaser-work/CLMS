from bcolors import bcolors as bc
from FileIO import FileIO
import sys

STATUS = ['ACTIVE', 'INACTIVE', 'BROKEN', 'UNKNOWN']
OS = ['WINDOWS', 'MAC', 'LINUX', 'UNKNOWN']
CTRLS = ['Add New PC', 'Update PC', 'Remove PC', 'Show All PCs', 'Search PC']
DUP_ID_OPTIONS = ['Update', 'Remove', 'Cancel']
DB_FILE = 'db.json'
SEARCH_OPTIONS = ['ID', 'OS', 'Status', 'Go Back to Main Menu']
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

                                                Computer Lab Management System'''
    print(b.success(title))
    print(b.warning(b.bold('                                                     Yaser, Samin | 19-39442-1'
                           )))
    print(b.success('-' * 78))

# TODO: Add docstrings to all functions
# TODO: Every function should have a return type
# TODO: Every function's parameter should have a type
# TODO: Use Match instead of if-else


def is_id_unique(id: int) -> bool:
    data = io.load()
    if id in [pc['id'] for pc in data]:
        return False
    return True


def get_pcs(value: str | int, key='id' or 'status' or 'os') -> list:
    res = []
    for pc in io.load():
        if str(pc[key]) == str(value):
            res.append(pc)
    return res


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


def take_input(msg: str, exp_msg: str, max_value=sys.maxsize, min_value=1,  isStr=False) -> int | str:
    while True:
        inp = input(msg).strip().lower()
        if isStr or inp == 'quit':
            return inp
        try:
            inp = int(inp)
        except ValueError:
            print_exception_msg(exp_msg)
        except Exception as e:
            print(b.error('Error:'), str(e))
        else:
            if inp >= min_value and inp <= max_value:
                return inp
            else:
                print_invalid_choice_msg()


def print_table(data: list, countMsg='', showMsg=True) -> None:

    if showMsg:
        if not countMsg:
            print(
                f"\nTotal {b.GREEN}{b.BOLD}{len(data)}{b.ENDC} PC(s) found in DB")
        else:
            print(countMsg)

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
            case 'unknown':
                status = b.info(pc['status'])
            case _:
                status = pc['status']

        print('%-5i' % pc['id'], '%-17s' % pc['os'], '%-17s' % status)


def print_menu(menu_header: str, options: list, menu_trailer='', style=b.warning) -> None:

    print(style(f'\n{menu_header}'))

    print()

    for idx, option in enumerate(options):
        print(b.info(f'{idx + 1}:'), f'{option}')

    print()

    if menu_trailer:
        print(menu_trailer)


def get_os_and_status(id: int):
    print_menu(
        f'What is the Operating System of the PC {id}?', OS
    )

    os_choice = take_input('Choose OS: ', 'OS', max_value=len(OS)) - 1

    print_menu(
        f'What is the current status of the PC {id}?', STATUS
    )

    status_choice = take_input(
        'Choose status: ', 'Status', max_value=len(STATUS)) - 1

    return OS[os_choice], STATUS[status_choice]


def add_new_pc() -> None:
    print(b.subtitle('\nADD PC\n'))

    id = take_input('Enter ID: ', 'ID')

    pc = get_pcs(key='id', value=id)

    if pc:
        print(b.info(f'\nID {id} already exists in DB'))
        print_table(pc, showMsg=False)
        while True:
            try:
                print_menu('What do you want to do?', DUP_ID_OPTIONS)
                choice = take_input('Choose: ', 'Choice',
                                    max_value=len(DUP_ID_OPTIONS))
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

    os, status = get_os_and_status(id)

    data = io.load()
    data.append({
        "id": id,
        "status": status,
        "os": os
    })
    io.save(data)

    print(b.success(f'\nPC {id} added to DB'))


def update_pc(showTitle: bool = True, id: int = -1) -> None:

    if showTitle:
        print(b.subtitle('\nUpdate PC\n'))

    if id == -1:
        id = take_input('Enter ID to Update (0 to go back): ',
                        'ID', min_value=0)
        if id == 0:
            print('\nCancelling Update...\n')
            return

    pc = get_pcs(key='id', value=id)

    if not pc:
        print('\n' + b.error(f'ID {id} not found in DB'))
        return

    os, status = get_os_and_status(id)

    print(os, status)

    data = io.load()
    # TODO: Create update function
    for pc in data:
        if pc['id'] == id:
            pc['status'] = status
            pc['os'] = os
            break
    io.save(data)

    print(b.success(f'\nPC {id} updated successfully'))


def remove_pc(showTitle: bool = True, id: int = -1) -> None:

    if showTitle:
        print(b.subtitle('\nRemove PC\n'))

    data = io.load()

    if id == -1:
        id = take_input('Enter ID to Remove (0 to go back): ',
                        'ID', min_value=0)
        if id == 0:
            print('\nCancelling Remove...\n')
            return

    pc = get_pcs(key='id', value=id)

    if not pc:
        print(b.error(f'\nPC with ID {id} not found in DB\n'))
        id = -1

    print_table(pc)

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

    print_menu(
        menu_header='Search by:',
        options=SEARCH_OPTIONS,
        style=b.underline
    )

    method = take_input('Enter search method: ', 'Choice',
                        max_value=len(SEARCH_OPTIONS), min_value=0)

    if method == 4:
        return

    category = SEARCH_OPTIONS[method - 1]

    search_key = take_input(
        f'Enter {category.upper()} to Search: ', exp_msg=category.upper(), isStr=True)

    res = get_pcs(value=search_key, key=category.lower())

    if res:
        text = b.success(
            f'\nTotal of {len(res)} PC(s) found with {category.upper()} {search_key.upper()}')
        print_table(data=res, countMsg=text)
    else:
        text = b.error(
            f'\nNo PC found with {category.upper()} {search_key.upper()}')
        print(text)


def show_all_pc() -> None:
    data = io.load()
    text = f"\nTotal {b.GREEN}{b.BOLD}{len(data)}{b.ENDC} PC(s) found in DB"
    print_table(data=data, countMsg=text)


def main_menu() -> None:

    quitText = f"Type {b.info('quit')} to exit"

    while True:
        print_menu(menu_header='Main Menu:', style=b.title,
                   options=CTRLS, menu_trailer=quitText)
        print()
        choice = take_input(msg='Enter your choice: ',
                            exp_msg='Choice', max_value=len(CTRLS))

        match choice:
            case 1:
                add_new_pc()
            case 2:
                update_pc()
            case 3:
                remove_pc()
            case 4:
                show_all_pc()
            case 5:
                search_pc()
            case 'quit':
                break
            case _:
                print_invalid_choice_msg()


def start_program() -> None:
    print_title()
    main_menu()
    print('Quitting CLMS...')  # TODO: Save before quitting


if __name__ == '__main__':
    start_program()
