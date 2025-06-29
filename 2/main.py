def binary_search(arr: list, x: float) -> tuple:
    low = 0
    high = len(arr) - 1
    iterations = 0
    upper_bound = None

    while low <= high:
        mid = (low + high) // 2
        iterations += 1

        print(f'Check: {arr[mid]} on position {mid}, iteration {iterations}')

        if arr[mid] < x:
            low = mid + 1
        elif arr[mid] > x:
            high = mid - 1
            upper_bound = arr[mid]
        else:
            return (iterations, arr[mid])
    return (iterations, upper_bound)

arr = [2.5, 3.9, 4.1, 4.8, 6.3, 7.2, 8.4, 9.1, 10.0]
x = 6.3

result = binary_search(arr, x)
if result[1] is not None:
    print(f"Element {x} was found in {result[0]} iteration(s). Upper limit: {result[1]}")
else:
    print(f"Element {x} was not found")
