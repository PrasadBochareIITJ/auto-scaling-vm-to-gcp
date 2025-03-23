# matrix_cpu_load.py
import numpy as np  # Import numpy for matrix operations

# Matrix size (increase this for heavier CPU load)
size = 1000

# Loop to continuously multiply matrices (to keep CPU busy)
while True:
    print(f"Starting matrix multiplication with size: {size}x{size}")
    
    # Generate two random matrices of given size
    A = np.random.rand(size, size)
    B = np.random.rand(size, size)
    
    # Perform matrix multiplication
    result = np.dot(A, B)
    
    print("Matrix multiplication complete.")
