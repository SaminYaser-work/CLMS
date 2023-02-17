class bcolors:
    """Color codes for UNIX terminal
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def title(self, text: str) -> str:
        return f'{self.HEADER}{self.BOLD}{self.UNDERLINE}{text}{self.ENDC}'

    def subtitle(self, text: str) -> str:
        return f'{self.CYAN}{self.BOLD}{text}{self.ENDC}'

    def info(self, text: str) -> str:
        return f'{self.BLUE}{text}{self.ENDC}'

    def success(self, text: str) -> str:
        return f'{self.GREEN}{text}{self.ENDC}'

    def warning(self, text: str) -> str:
        return f'{self.WARNING}{text}{self.ENDC}'

    def error(self, text: str) -> str:
        return f'{self.FAIL}{text}{self.ENDC}'

    def underline(self, text: str) -> str:
        return f'{self.UNDERLINE}{text}{self.ENDC}'

    def bold(self, text: str) -> str:
        return f'{self.BOLD}{text}{self.ENDC}'
