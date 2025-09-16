from functions.run_python_file import *
def main():
    tests = [
        run_python_file("calculator", "main.py"),
        run_python_file("calculator", "main.py", ["3 + 5"]),
        run_python_file("calculator", "tests.py"),
        run_python_file("calculator", "../main.py"),
        run_python_file("calculator", "nonexistent.py")
    ]
    for test in tests:
        print("------------")
        print(test)

if __name__ == "__main__":
    main()