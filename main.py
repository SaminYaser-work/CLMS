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
    """Prints the title of the program
    """

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

# DONE: Add docstrings to all functions
# DONE: Every function should have a return type
# DONE: Every function's parameter should have a type


def print_exception_msg(msg: str) -> None:
    """Prints an error with the given message

    Args:
        msg (str): Message to be printed
    """
    print(f'\n{b.error("Error")} {msg} must be a non-zero positive integer\n')


def print_invalid_choice_msg() -> None:
    """Prints an error when the user enters an invalid choice in menu
    """
    print(f'\n{b.warning("Invalid choice")}\n')


def take_input(msg: str, exp_msg: str, max_value=sys.maxsize, min_value=1,  isStr=False) -> int | str:
    """Takes input from the user, validates it while handling exceptions, and returns it

    Args:
        msg (str): Input prompt message
        exp_msg (str): Message to be printed when an exception occurs
        max_value (_type_, optional): Max value for menu selection. Defaults to sys.maxsize.
        min_value (int, optional): Min value for menu selection. Defaults to 1.
        isStr (bool, optional): Take the input as a string. Defaults to False.

    Returns:
        int | str: Returns the input if it is a string or an integer between min_value and max_value
    """
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
    """Prints the given data in a table with proper formatting

    Args:
        data (list): List of dictionaries to be printed
        countMsg (str, optional): Custom message to be shown instead of the default one at the beginning of the table. Defaults to ''.
        showMsg (bool, optional): Show or hide message at the beginning. Defaults to True.
    """

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
    """Prints a menu with the given options

    Args:
        menu_header (str): The header of the menu
        options (list): List of options to be printed
        menu_trailer (str, optional): The trailer of the menu. Defaults to ''.
        style (_type_, optional): Style of the menu_header. Defaults to b.warning.
    """

    print(style(f'\n{menu_header}'))

    print()

    for idx, option in enumerate(options):
        print(b.info(f'{idx + 1}:'), f'{option}')

    print()

    if menu_trailer:
        print(menu_trailer)


def get_os_and_status(id: int):
    """Takes input from the user for the OS and status of the PC with the given ID. Used for Add and Update functions

    Args:
        id (int): ID of the PC

    Returns:
        _type_: Returns the OS and status of the PC
    """
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
    """Adds a new PC to the DB
    """
    print(b.subtitle('\nADD PC\n'))

    id = take_input('Enter ID: ', 'ID')

    pc = io.get(key='id', value=id)

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

    io.create(
        id=id,
        status=status,
        os=os
    )

    print(b.success(f'\nPC {id} added to DB'))


def update_pc(showTitle: bool = True, id: int = -1) -> None:
    """Updates the PC with the given ID

    Args:
        showTitle (bool, optional): Show title. Defaults to True.
        id (int, optional): ID of the PC to update. If not given, user will be prompted to input a valid ID. Defaults to -1.
    """

    if showTitle:
        print(b.subtitle('\nUpdate PC\n'))

    if id == -1:
        id = take_input('Enter ID to Update (0 to go back): ',
                        'ID', min_value=0)
        if id == 0:
            print('\nCancelling Update...\n')
            return

    pc = io.get(key='id', value=id)

    if not pc:
        print('\n' + b.error(f'ID {id} not found in DB'))
        return

    os, status = get_os_and_status(id)

    print(os, status)

    io.update(
        id=id,
        status=status,
        os=os
    )

    print(b.success(f'\nPC {id} updated successfully'))


def remove_pc(showTitle: bool = True, id: int = -1) -> None:
    """Removes the PC with the given ID


    Args:
        showTitle (bool, optional): Show title. Defaults to True.
        id (int, optional): ID of the PC to remove. If not given, user will be prompted to provide a valid ID. Defaults to -1.
    """

    if showTitle:
        print(b.subtitle('\nRemove PC\n'))

    if id == -1:
        id = take_input('Enter ID to Remove (0 to go back): ',
                        'ID', min_value=0)
        if id == 0:
            print('\nCancelling Remove...\n')
            return

    pc = io.get(key='id', value=id)

    if not pc:
        print(b.error(f'\nPC with ID {id} not found in DB\n'))
        id = -1

    print_table(pc)

    confirm = input(
        b.warning(f'\nAre you sure you want to remove PC with ID {id}? (y/N): '))
    if confirm != 'y':
        print('\nCancelling Remove...\n')
        return

    io.delete(id=id)

    print(b.success(f'\nPC with ID {id} removed successfully from DB\n'))


def search_pc() -> None:
    """ Searches the DB for a PC with the given ID, OS or Status. If no PC is found, an error message is displayed with a prompt to add a new PC.
    """
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

    res = io.get(value=search_key.upper(), key=category.lower())

    if res:
        text = b.success(
            f'\nTotal of {len(res)} PC(s) found with {category.upper()} {search_key.upper()}')
        print_table(data=res, countMsg=text)
    else:
        text = b.error(
            f'\nNo PC found with {category.upper()} {search_key.upper()}')
        print(text)

        # Add new PC
        confirm = input(
            b.warning(f'\nDo you want to add a new PC with {category.upper()} {search_key.upper()}? (y/N): '))
        if confirm != 'y':
            return
        add_new_pc()


def show_all_pc() -> None:
    """Shows all the PC in the DB in a table
    """
    data = io.get_all()
    if not data:
        print(b.error('\nNo PC found in DB'))
        return
    text = f"\nTotal {b.GREEN}{b.BOLD}{len(data)}{b.ENDC} PC(s) found in DB"
    print_table(data=data, countMsg=text)


def main_menu() -> None:
    """Main menu of the program
    """

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
    """Starts the program
    """
    print_title()
    main_menu()
    print(b.subtitle('\nQuitting CLMS...'))


if __name__ == '__main__':
    start_program()
