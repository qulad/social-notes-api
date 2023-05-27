import requests

BASE = "http://localhost:5000/api/v1/"

""" headers = {
    "Content-Type": "application/json",
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDQ4Mjg0OCwianRpIjoiYjNmMGQ5MTQtZjI3OC00MmM3LWE5NzAtNTg5ODE0YjEyNDkyIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjg0NDgyODQ4LCJleHAiOjE2ODQ0ODM3NDh9.93G7wy62QVFAV2i5Zca-_5VF5iJVTsCIM_m1sGw_zFI"
    }
data = {
    "user_name": "SO",
    "public_profile": True,
#    "country": "USA",
#    "biography": "Lorem ipsum dolor sit amet.",
    "email": "SO@example.com",
    "password1": "password",
    "password2": "password"
}
response = requests.post(BASE + "user/register", json=data, headers=headers)
print(response.status_code, response.json()) """

""" headers = {
    "Content-Type": "application/json",
}
data = {
    "email": "SO@example.com",
    "password": "password"
}
response = requests.post(BASE + "user/login", json=data, headers=headers)
print(response.status_code, response.json()) """

""" headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDQ4NTMwNiwianRpIjoiMGVhYjM2NDMtZTNhMy00NzZhLWExMmEtOTAyZWJlYTkzNTk1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjg0NDg1MzA2LCJleHAiOjE2ODQ0ODYyMDZ9.KCJaKZhd4B7kWcP8MyqnNCVHxb55DwTCVvQC4JbnE3M"
}
data = {
    "user_name": "hnDo",
    "public_profile": True,
    "country": "USA",
    "biography": "Lorem ipsum dolor sit amet.",
    "email": "ffo@example.com",
    "password1": "passwordsad",
    "password2": "passwordsad"
}
response = requests.post(BASE + "user/edit", json=data, headers=headers)
print(response.status_code, response.json()) """

""" headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDQ4NjI1OSwianRpIjoiMzBiY2RhNzctMGZhNy00OGExLWI5MTktODYyMWI4NGZlYzA2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjg0NDg2MjU5LCJleHAiOjE2ODQ0ODcxNTl9.HpyGFeK4zs3GTrCamxyfNXtvwMuwPQ9CsDiuc1zxD5k"
}
data = {
    "user_name": "hnDo",
    "public_profile": True,
    "country": "USA",
    "biography": "Lorem ipsum dolor sit amet.",
    "email": "oasdsssd@example.com",
    "password1": "password",
    "password2": "password"
}
response = requests.post(BASE + "user/delete", json=data, headers=headers)
print(response.status_code, response.json()) """

""" headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDQ4NjI1OSwianRpIjoiMzBiY2RhNzctMGZhNy00OGExLWI5MTktODYyMWI4NGZlYzA2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjg0NDg2MjU5LCJleHAiOjE2ODQ0ODcxNTl9.HpyGFeK4zs3GTrCamxyfNXtvwMuwPQ9CsDiuc1zxD5k"
}
data = {
    "user_name": "hnDo",
    "public_profile": True,
    "country": "USA",
    "biography": "Lorem ipsum dolor sit amet.",
    "email": "oasdsssd@example.com",
    "password1": "password",
    "password2": "password"
}
response = requests.get(BASE + "user/view_profile", json=data, headers=headers)
print(response.status_code, response.json()) """

""" headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDQ4ODQ2NCwianRpIjoiNGE5MGQ0NzUtY2VlOS00MzQ0LTkwOGYtOWY1MjRlYjc4NmQzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NCwibmJmIjoxNjg0NDg4NDY0LCJleHAiOjE2ODQ0ODkzNjR9.KcIwq6cPJswa5TT2ckzRdjJsIBsqI7lpmfI-ZAmUi68"
}
data = {
    "user_name": "sshnDo",
    "public_profile": True,
    "country": "USA",
    "biography": "Lorem ipsum dolor sit amet.",
    "email": "oasdsssd@example.com",
    "password1": "password",
    "password2": "password"
}
response = requests.post(BASE + "user/logout", json=data, headers=headers)
print(response.status_code, response.json()) """

""" headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDQ4OTI4OSwianRpIjoiZjNjYWRlYmMtMjZhMy00NzllLTk4MzktZTZhZTRjMmU5ZTE2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjg0NDg5Mjg5LCJleHAiOjE2ODQ0OTAxODl9.y_Tw7glAyctPD_S0mN_8URAuYfIomk3u50phsEpF0Qg"
}
data = {
    "user_name": "nDo",
    "public_profile": True,
    "country": "USA",
    "biography": "Lorem ipsum dolor sit amet.",
    "email": "oasdsssd@example.com",
    "password1": "password",
    "password2": "password"
}
response = requests.get(BASE + "block/block", json=data, headers=headers)
print(response.status_code, response.json()) """

""" headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDQ4OTI4OSwianRpIjoiZjNjYWRlYmMtMjZhMy00NzllLTk4MzktZTZhZTRjMmU5ZTE2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjg0NDg5Mjg5LCJleHAiOjE2ODQ0OTAxODl9.y_Tw7glAyctPD_S0mN_8URAuYfIomk3u50phsEpF0Qg"
}
data = {
    "user_name": "nDo",
    "public_profile": True,
    "country": "USA",
    "biography": "Lorem ipsum dolor sit amet.",
    "email": "oasdsssd@example.com",
    "password1": "password",
    "password2": "password"
}
response = requests.get(BASE + "block/unblock", json=data, headers=headers)
print(response.status_code, response.json()) """

""" headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDQ5MDQ4MywianRpIjoiOTYzNjBhNTQtYjhmMC00YjY4LWE3ZmMtMmIyZDNhOTA3N2I1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjg0NDkwNDgzLCJleHAiOjE2ODQ0OTEzODN9.UYudygPfOxogQ1SquaNrDMopfd5FYSAfZFtST8Q231k"
}
data = {
    "user_name": "Do",
    "public_profile": True,
    "country": "USA",
    "biography": "Lorem ipsum dolor sit amet.",
    "email": "oasdsssd@example.com",
    "password1": "password",
    "password2": "password"
}
response = requests.get(BASE + "friendship/accept", json=data, headers=headers)
print(response.status_code, response.json()) """

""" headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4NDUwMzMzNCwianRpIjoiM2ViMDA5MzYtNTU4NC00MWRmLWEwNjYtYzJlZGNkMGM1ZWNlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6NiwibmJmIjoxNjg0NTAzMzM0LCJleHAiOjE2ODQ1MDQyMzR9.O3qyD8yr2rEjsIp4vfFx35Xd52r_waZesbV_96FyN28"
}
data = {
    "user_name": "SON",
    "public_profile": False,
    "country": "USA",
    "biography": "Lorem ipsum dolor sit amet.",
    "email": "SON@example.com",
    "password1": "password",
    "password2": "password",
    "text": "post iki",
    "post_id": "1"
}
response = requests.post(BASE + "user/edit", json=data, headers=headers)
print(response.status_code, response.json()) """