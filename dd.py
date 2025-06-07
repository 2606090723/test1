# 生成一段代码
import random
def generate_code():
    code = ""
    for _ in range(10):
        line = f"print('Hello, World! {random.randint(1, 100)}')\n"
        code += line
    return code



if __name__ == "__main__":
    generated_code = generate_code()
    print("Generated Code:")
    print(generated_code)
    
    # Optionally, save to a file
    with open("generated_code.py", "w") as f:
        f.write(generated_code)
    print("Code saved to generated_code.py")