import instaloader

L = instaloader.Instaloader()
L.context.proxy = "http://192.168.1.100:8080"
L.login('mrhossam0', 'hossamshaory2003$$')

def get_latest_post(username):
    profile = instaloader.Profile.from_username(L.context, username)
    latest_post = next(profile.get_posts())
    L.download_post(latest_post, target=profile.username)
    return latest_post
