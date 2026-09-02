import os

for fname in ['frontend/style.css', 'frontend/app.js']:
    try:
        # The file contains UTF-8 encoded Chinese characters, 
        # which were created by decoding the original ASCII bytes as UTF-16LE.
        # To reverse: Read as UTF-8, then encode the resulting string as UTF-16LE to get the original bytes back.
        with open(fname, 'r', encoding='utf-8') as f:
            corrupted_str = f.read()
        
        original_bytes = corrupted_str.encode('utf-16le')
        
        # Verify it looks like ASCII (or at least valid UTF-8 now)
        decoded_test = original_bytes.decode('utf-8')
        
        with open(fname, 'wb') as f:
            f.write(original_bytes)
        print(f"Fixed {fname}")
    except Exception as e:
        print(f"Error on {fname}: {e}")
