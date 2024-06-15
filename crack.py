# imports
import numpy as np
import galois
from itertools import combinations

def encrypt(plaintext, public_key, q):

    # Unpack the public key
    A, b = public_key

    # Get the dimensions of the matrix A
    m, n = A.shape
    
    # Initialize an array to hold the ciphertext
    ciphertext = np.empty(plaintext.shape, dtype=object)
    
    # Encrypt each bit in the plaintext
    for index, bit in enumerate(plaintext):
        # Generate a random binary vector of length m
        r = np.random.randint(2, size=m)

        # Compute a' = rA mod q
        a_prime = np.dot(r, A) % q
        
        # Compute b' = (rb + bit * (q // 2)) mod q
        b_prime = (np.dot(r, b) + bit * (q // 2)) % q
        
        # Store the encrypted bit as a tuple (a', b')
        ciphertext[index] = (a_prime, b_prime)
    
    return ciphertext

def decrypt(ciphertext, private_key, q):
    
    # Initialize an array to hold the plaintext
    plaintext = np.empty(len(ciphertext), dtype=int)

    # Decrypt each tuple (a', b') in the ciphertext
    for index, (a_prime, b_prime) in enumerate(ciphertext):
        # Adjust the private key size if necessary
        adjusted_private_key = private_key[:len(a_prime)] if len(private_key) != len(a_prime) else private_key

        # Compute v = a' * adjusted_private_key mod q
        v = np.dot(a_prime, adjusted_private_key) % q

        # Compute m' = (b' - v) mod q
        m_prime = (b_prime - v) % q

        # Apply the decision rule to determine the plaintext bit
        is_closer_to_half_q = abs(m_prime - (q // 2)) < (m_prime) and abs(m_prime - (q // 2)) < (q - m_prime)
        plaintext[index] = 1 if is_closer_to_half_q else 0

    return plaintext

def crack1(ciphertext, public_key, q):
    # Extract components from the public key
    A, b = public_key

    GF = galois.GF(q)

    A = GF(A)
    b = GF(b)
    
    # Solve the system of equations Ax = b
    # Compute s = (A^T A)^-1 A^T b
    s = np.dot(np.linalg.inv(np.dot(A.T, A)), np.dot(A.T, b))
    
    # Turn s back to numpy array (instead of Galois Field array)
    s = np.array(s)
    
    return decrypt(ciphertext, s, q)
    
def crack2(ciphertext, public_key, q, theta=4):
    
    # Extract components from the public key
    A, b = public_key
    
    m, n = A.shape

    # [key] = cracked solution 
    # :value = number of times the solution has been seen
    sol_count = {}
    
    # generate all possible combinations of n rows - all system of linear equation subsets of size n
    index_combinations = list(combinations(range(A.shape[0]), n))


    # shuffle the combinations
    np.random.shuffle(index_combinations)
    
    # for each combination perform the code below
    for indices in index_combinations:
        GF = galois.GF(q)
        A = GF(A)
        b = GF(b)
     
        # Choose corresponding rows from A and b - form system of linear equations
        A_selected = A[np.array(indices)]
        b_selected = b[np.array(indices)]

        # Convert to Galois Field - bound the values to the range 0 - q
        GF = galois.GF(q)
        A_selected = GF(A_selected)
        b_selected = GF(b_selected)
        
        try:
            # run crack 1
            sol = crack1(ciphertext, (A_selected, b_selected), q)
            
            # hash the solution - python tuples are hashable
            hashed_sol = (tuple(sol))
            
            # has the solution been seen before?
            if hashed_sol in sol_count:
                # has the solution been seen theta times?
                if sol_count[hashed_sol] == theta:
                    return sol
                
                # enumerate the times the solution has been seen
                sol_count[hashed_sol] += 1
            else:
                
                # add the solution to the dictionary
                sol_count[hashed_sol] = 1
            
        except Exception as e:
            # Linear Dependence error - The randomly selected rows may not be linearly independent
            # this will cause an error when trying to solve the system of equations
            # This is fine - just try again
            pass
        
    # if no solution has been found - return the most common 
    return max(sol_count, key=sol_count.get)
        
def crack3(ciphertext, public_key,q):
    # using the crack 2 solution - this SHOULD NOT work but it does due to the reasons in the report
    return crack2(ciphertext, public_key, q)

    
    
    



