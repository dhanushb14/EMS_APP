# Write python code to create a new file called 'new_file.txt'

# Write python code to open the file and write 'Hello World' to it
def write_file():
    with open('new_file.txt', 'w') as f:
        f.write('Hello World')

def main():
    write_file()

if __name__ == '__main__':
    main()
    