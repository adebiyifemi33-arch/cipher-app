import math

def encrypt_message(key: str, message: str) -> str:
    if not key or not message:
        return ""
        
    ciphertext_cols = [""] * len(key)
    
    for col in range(len(key)):
        pointer = col
        while pointer < len(message):
            ciphertext_cols[col] += message[pointer]
            pointer += len(key)
            
    key_order = sorted([(char, i) for i, char in enumerate(key)])
    final_ciphertext = "".join(ciphertext_cols[original_index] for _, original_index in key_order)
    return final_ciphertext

def decrypt_message(key: str, message: str) -> str:
    if not key or not message:
        return ""
        
    num_cols = len(key)
    num_rows = math.ceil(len(message) / float(num_cols))
    num_shaded = (num_cols * num_rows) - len(message)
    
    plaintext_cols = [""] * num_cols
    col_lengths = [num_rows] * num_cols
    for i in range(num_cols - num_shaded, num_cols):
        col_lengths[i] = num_rows - 1
        
    key_order = sorted([(char, i) for i, char in enumerate(key)])
    
    pointer = 0
    for char, original_index in key_order:
        length = col_lengths[original_index]
        plaintext_cols[original_index] = message[pointer:pointer+length]
        pointer += length
        
    final_plaintext = ""
    for row in range(num_rows):
        for col in range(num_cols):
            if row < len(plaintext_cols[col]):
                final_plaintext += plaintext_cols[col][row]
                
    return final_plaintext
