def calculate(*args,operation="sum")-> int :
    if operation == "sum":
        return sum(args)
    elif operation == "multily":
        result = 1
        for num in args:
            result*=num
        return result
    pass

def main():
    res1 = calculate(1, 2, 3, 4, operation="sum")
    print(f"求和结果: {res1}")

if __name__ == "__main__":
    main()