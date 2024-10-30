#creating new python file for a test 
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)

# Get the 10th Fibonacci number
print(fibonacci(10))
