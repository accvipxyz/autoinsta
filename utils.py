import os

def delete_media_files(username, post):
    base_path = f"{username}/{post.date_utc.strftime('%Y-%m-%d_%H-%M-%S_UTC')}"
    extensions = ['.jpg', '.mp4']
    
    for ext in extensions:
        for index in range(10):  # يفترض أن الألبوم قد يحتوي على ما يصل إلى 10 عناصر
            file_path = f"{base_path}_{index + 1}{ext}"
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {file_path}")
