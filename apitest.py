import requests
import random

user_id = random.randint(1, 10)
print(f"User ID: {user_id}")

response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
email = response.json()["email"]
print(f"User email: {email}")

response = requests.get(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")
posts = response.json()

for post in posts:
    post_id = post["id"]
    if not 1 <= post_id <= 100:
        print(f"Invalid Post ID: {post_id}")

new_post = {
    "userId": user_id,
    "title": "Test Post",
    "body": "This is a test post"
}

response = requests.post("https://jsonplaceholder.typicode.com/posts", json=new_post)
if response.status_code == 201:
    print("Post created successfully!")
else:
    print("Error creating post.")
