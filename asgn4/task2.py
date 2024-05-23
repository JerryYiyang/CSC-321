import time
import bcrypt
import multiprocessing
import concurrent.futures
from nltk.corpus import words

# Function to read and parse the shadow file
def read_shadow_file(file_path="shadow.txt"):
    users = {}
    with open(file_path, 'r') as file:
        for line in file:
            # Parse each line of the shadow file
            user_data = line.strip().split('$')
            username, algorithm, workfactor, salt_hash = user_data[0], user_data[1], user_data[2], user_data[3]
            # Extract salt and hash from the combined salt_hash
            salt = salt_hash[:22]
            hash = salt_hash[22:]
            # Store user details in a dictionary
            users[username] = {
                'username': username,
                'algorithm': algorithm,
                'workfactor': workfactor,
                'salt': salt,
                'hash': hash,
                'bcrypt_param': f"${algorithm}${workfactor}${salt}"
            }
    return users

# Function to crack passwords for all users
def crack_passwords(users):
    # Load all words from the NLTK corpus
    all_words = [word for word in words.words() if 6 <= len(word) <= 10]
    num_cores = multiprocessing.cpu_count()
    chunk_size = len(all_words) // num_cores
    result_dict = {}
    lock = multiprocessing.Lock()

    # Use ThreadPoolExecutor for parallel processing
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cores) as executor:
        futures = []
        for username, user_info in users.items():
            print(f"Starting cracking for user {username}")
            # Split the word list into chunks for each core
            for i in range(num_cores):
                start_index = i * chunk_size
                end_index = start_index + chunk_size if i < num_cores - 1 else len(all_words)
                word_chunk = all_words[start_index:end_index]
                # Submit each chunk to the executor
                future = executor.submit(crack_passwords_for_chunk, user_info, word_chunk, result_dict, lock)
                futures.append(future)

        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()

    return result_dict

# Function to crack passwords for a given chunk of words
def crack_passwords_for_chunk(user_info, word_chunk, result_dict, lock):
    bcrypt_param = user_info['bcrypt_param'].encode('ascii')
    target_hash = user_info['hash']

    for word in word_chunk:
        # Check if the password has already been found
        with lock:
            if user_info['username'] in result_dict:
                return

        # Hash the word with the provided bcrypt parameters
        hashed_word = bcrypt.hashpw(word.encode(), bcrypt_param)
        if hashed_word.decode().endswith(target_hash):
            end_time = time.time()
            duration = end_time - user_info['start_time']
            print(f"Password for user {user_info['username']} found: {word}")
            print(f"Time taken: {duration} seconds")

            # Record the found password
            with lock:
                result_dict[user_info['username']] = word
            return

# Main function to read the shadow file and start the cracking process
def main():
    # Read users and hashes from the shadow file
    users = read_shadow_file()
    # Record the start time for each user
    for user_info in users.values():
        user_info['start_time'] = time.time()

    # Start the password cracking process
    cracked_passwords = crack_passwords(users)

    # Print the results
    for username, password in cracked_passwords.items():
        print(f"User: {username}, Password: {password}")

if __name__ == "__main__":
    main()
