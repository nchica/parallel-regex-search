def main():
    with open("test4.txt", "w") as file_obj:
        for i in range(1000):
            file_obj.write(f"{i} is dog\n")


if __name__ == '__main__':
    main()
