import datetime

def main():
    print("Hello from Jules' House!")
    now = datetime.datetime.now()
    print(f"The current time is: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("I am initialized and ready to explore.")

if __name__ == "__main__":
    main()
