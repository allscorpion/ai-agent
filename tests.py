from functions.get_files_info import get_files_info, get_file_content

def main():
    tests = [
        get_file_content("calculator", "main.py"),
        get_file_content("calculator", "pkg/calculator.py"),
        get_file_content("calculator", "/bin/cat"),
        get_file_content("calculator", "pkg/does_not_exist.py"),
    ]
    for test in tests:
        print("------------")
        print(test)

if __name__ == "__main__":
    main()