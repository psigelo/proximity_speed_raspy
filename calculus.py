from sql import get_data
import time

def main():
    while(True):
        data = get_data(30)
        average = 0
        for row in data:
            average += row[3]
        print(average/len(data))
        time.sleep(1.5)

if __name__ == "__main__":
    main()