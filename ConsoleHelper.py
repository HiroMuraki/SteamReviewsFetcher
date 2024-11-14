class ConsoleHelper:
    YELLOW = '\033[33m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    RESET = '\033[0m'

    @staticmethod
    def write_warning(message: str) -> None:
        print(f"{ConsoleHelper.YELLOW}[Warning] {message}{ConsoleHelper.RESET}")

    @staticmethod
    def write_error(message: str) -> None:
        print(f"{ConsoleHelper.RED}[Error] {message}{ConsoleHelper.RESET}")

    @staticmethod
    def write_success(message: str) -> None:
        print(f"{ConsoleHelper.GREEN}[OK] {message}{ConsoleHelper.RESET}")

    @staticmethod
    def write(message: str) -> None:
        print(message)
