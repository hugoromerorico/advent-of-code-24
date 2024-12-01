def parse_input(filename):
    left_list = []
    right_list = []
    
    with open(filename, 'r') as f:
        for line in f:
            # Split each line into two numbers
            left, right = map(int, line.strip().split())
            left_list.append(left)
            right_list.append(right)
    
    return left_list, right_list

def calculate_total_distance(left_list, right_list):
    # Sort both lists to pair smallest with smallest, etc.
    sorted_left = sorted(left_list)
    sorted_right = sorted(right_list)
    
    total_distance = 0
    # Calculate distance between each pair
    for l, r in zip(sorted_left, sorted_right):
        distance = abs(l - r)
        total_distance += distance
    
    return total_distance

def main():
    # Read and parse input
    left_list, right_list = parse_input('in.txt')
    
    # Calculate and print result
    result = calculate_total_distance(left_list, right_list)
    print(f"The total distance between the lists is: {result}")

if __name__ == "__main__":
    main()