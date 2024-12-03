data = open("in.txt").read()

total = 0
enabled = True

i = 0
while i < len(data):
    # Handle do() instruction
    if data[i:i+4] == "do()":
        enabled = True
        i += 4
        continue
        
    # Handle don't() instruction    
    if data[i:i+7] == "don't()":
        enabled = False
        i += 7
        continue
        
    # Handle mul instruction
    if data[i:i+4] == "mul(" and enabled:
        i += 4
        num1 = ""
        # Get first number
        while i < len(data) and data[i].isdigit():
            num1 += data[i]
            i += 1
            
        # Must have comma after first number
        if i < len(data) and data[i] == ",":
            i += 1
            num2 = ""
            # Get second number
            while i < len(data) and data[i].isdigit():
                num2 += data[i]
                i += 1
                
            # Must end with closing parenthesis
            if i < len(data) and data[i] == ")" and num1 and num2:
                total += int(num1) * int(num2)
        
    i += 1

print(total)