# _*_ coding:utf-8 _*_
import requests


def get_auth_url():
    url = 'https://api.weibo.com/oauth2/authorize'
    client_id = '3252425763'
    redirect_uri = 'http://127.0.0.1:8000/complete/weibo'
    auth_url = url + "?client_id=" + client_id + "&redirect_uri=" + redirect_uri
    return auth_url


def get_access_token(code=None):
    # 请求的路径，post
    url = "https://api.weibo.com/oauth2/access_token"
    # 应用的id
    client_id = "3252425763"
    client_secret = "063dd3ef65ef6132a6fa91293048cb85"
    grant_type = "authorization_code"
    code = code
    # 回调后台服务器的地址
    redirect_uri = "http://127.0.0.1:8000/complete/weibo/"

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": grant_type,
        "code": code,
        "redirect_uri": redirect_uri

    }

    response = requests.post(url, data=data)

    return response.text


def get_user_info(access_token=None, uid=None):
    user_info_url = "https://api.weibo.com/2/users/show.json"
    import requests
    url = user_info_url + "?access_token=" + access_token + "&uid=" + uid
    response = requests.get(url)
    print("user_info==", response.text)


if __name__ == "__main__":
    print(get_auth_url())
