import requests

url = "https://movie-database-imdb-alternative.p.rapidapi.com/"

querystring = {"s":"Toy Story 3","r":"json","item":"1"}

headers = {
    'x-rapidapi-host': "movie-database-imdb-alternative.p.rapidapi.com",
    'x-rapidapi-key': "e7784258e1msh9c5de369e9adc67p1e6182jsn666c246ff8bf"
    }

response = requests.request("GET", url, headers=headers, params=querystring) #returns response as JSON from API call

jsonRes = response.json()
print("Print each key-value pair from JSON response")

for key, value in jsonRes.items():
    for i in range (0,1):
        print(key, ":", value)
        break


#print(jsonRes.get('Title'))
#jsonRes["Title"]
#print(type(response))
#print(response.text)