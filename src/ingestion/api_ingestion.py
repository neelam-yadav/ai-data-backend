def fetch_from_api(api_url, headers=None, params=None):
    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()
    return {"content": data, "source": api_url}
