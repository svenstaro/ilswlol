def is_curl_like(user_agent_string):
    curl_likes = ["HTTPie", "curl"]
    return any([tool in user_agent_string for tool in curl_likes])
