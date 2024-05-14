import hashlib
import os
import time
import bcrypt
import base64
import multiprocessing
import concurrent.futures
from bitstring import BitArray
from nltk.corpus import words

def calculate_sha256(input_string, num_bits):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(input_string)
    full_digest = sha256_hash.digest()
    bitArray = BitArray(full_digest)
    truncated = bitArray.bin[:num_bits]
    # Truncate the digest to the desired number of bits
    # truncated_digest = full_digest[:num_bits//8]
    # hex_digest = truncated_digest.hex()
    #print(hex(int(truncated, 2)))
    return truncated

def hamming1_sha256(input_string):
    # Convert the input string to a list of bits
    calculate_sha256(input_string, 48)
    bit_list = list(input_string)
    
    # Flip the first bit
    bit_list[0] ^= 1
    
    # Convert the modified bit list back to a string
    modified_string = bytes(bit_list)
    calculate_sha256(modified_string, 48)

def find_collision(num_bits, N = 2 ** 25):
    start_time = time.time()
    hash_dict = {}
    num_inputs = 0
    while N >= 0:
        # Generate a random input string
        s = os.urandom(10)
        # Calculate the truncated SHA256 hash
        truncated_hash = calculate_sha256(s, num_bits)
        num_inputs += 1
        # Check if the truncated hash already exists in the dictionary
        if truncated_hash in hash_dict and hash_dict[truncated_hash] != s:
            # Collision found, print the colliding inputs and their hashes
            print("Collision found:")
            print("Input 1: ", hash_dict[truncated_hash])
            print("Input 2: ", s)
            print("Digest size: ", num_bits)
            print("Hash: ", truncated_hash)
            print("Inputs: ", num_inputs)
            end_time = time.time()
            print("Total time:", end_time - start_time, "seconds")
            return (s, hash_dict[truncated_hash])
        else:
            # Store the input string along with its truncated hash
            hash_dict[truncated_hash] = s
        N -= 1
        if N < 0: print("Sorry, no luck")
    

def task1():
    bit_size = [num for num in range(8, 51) if num % 2 == 0]
    for bit in bit_size:
        find_collision(bit)

def read_shadow_file():
    users = {}
    with open("shadow.txt", 'r') as file:
        for line in file:
            user_data = line.strip().split('$')
            username, algorithm, workfactor, salt_hash = user_data[0], user_data[1], user_data[2], user_data[3]
            salt = salt_hash[:22]
            hash = salt_hash[22:]
            users[username] = {
                'username': username,
                'algorithm': algorithm,
                'workfactor': workfactor,
                'salt': salt,
                'hash': hash,
                'bcrypt-param': f"${algorithm}${workfactor}${salt}"
            }         
    return users


def crack_passwords(users):  
    # users_by_workfactor = {}
    # for user in users:
    #     workfactor = user['workfactor']
    #     if workfactor not in users_by_workfactor:
    #         users_by_workfactor[workfactor] = []
    #     users_by_workfactor[workfactor].append(user)

    # Crack passwords for each work factor group using multiprocessing
    # with multiprocessing.Pool() as pool:
    #     results = pool.map(crack_passwords_workfactor, users_by_workfactor.values())
    #     # Check if any result is found
    #     for result in results:
    #         if result:
    #             break
    all_words = words.words()  
    num_cores = multiprocessing.cpu_count()
    print("num cores: ", num_cores)
    chunk_size = len(all_words) // num_cores
    result_dict = {}
    lock = multiprocessing.Lock()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cores) as executor:
        futures = []
        for username, user_info in users.items():
            for i in range(num_cores):
                start_index = i * chunk_size
                end_index = start_index + chunk_size if i < num_cores - 1 else len(all_words)
                word_chunk = all_words[start_index:end_index]
                future = executor.submit(crack_passwords_for_chunk, users, username, word_chunk, result_dict, lock)
                # future = executor.submit(crack_passwords_for_chunk, users, word_chunk)
                futures.append(future)
            for future in concurrent.futures.as_completed(futures):
                future.result()
                if len(result_dict) == len(users):
                    break
    
def crack_passwords_for_chunk(users, username, word_chunk, result_dict, lock):
    print(f"Cracking password for {username}")
    user_info = users[username]
    # for user in users:
    start_time = time.time()
    for word in word_chunk:
        if result_dict.get(username) is not None:
            return "Pass already found"
        hashed_word = bcrypt.hashpw(word.encode(), user_info['bcrypt-param'].encode('ascii'))
        want_to_find = user_info['bcrypt-param'] + user_info['hash']
        if hashed_word.decode() == want_to_find:
            print(f"Password for user {user_info['username']} is: {word}")
            end_time = time.time()
            duration = end_time - start_time
            print(f"Time taken: {duration} seconds")
            with lock:
                result_dict[username] = word
            return 
        # else:
        #     print(f"Password for user {user['username']} not found")
   

def main():
    # hamming1_sha256(b"Hello")
    # task1()
    users = read_shadow_file()
    crack_passwords(users)

if __name__ == "__main__":
    main()
