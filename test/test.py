import requests

json_data = {
	"username": "keosariel",
	"password": "password"
}

# create new account
res= requests.post("http://127.0.0.1:5000/signup", json=json_data)

if res.status_code == 200:
	# login user
	res = requests.post("http://127.0.0.1:5000/login", json=json_data)

	if res.status_code == 200:
		token = res.json().get("token")

		# prepare headers
		headers = {'Authorization': f'Bearer {token}'}

		res = requests.get("http://127.0.0.1:5000/", headers=headers)

		if res.status_code == 200:
			# Output: {'id': 1, 'username': 'keosariel'}
			print(res.json())
