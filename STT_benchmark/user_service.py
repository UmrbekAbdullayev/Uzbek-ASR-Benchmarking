from db import supabase

# creates a user in supabase
def create_user(name: str):
    if not name or not isinstance(name, str):
        return None

    response = supabase.table("users").insert({
        "name": name.strip()
    }).execute()
    
    return response.data[0] if response.data else None


# adds a url to the supabase    
def add_url(user_id: str, url: str):
    if not user_id or not url:
        return None

    response = supabase.table("urls").insert({
        "user_id": user_id,
        "url": url.strip()
    }).execute()

    return response.data[0] if response.data else None
    

# retrieves urls for a given user
def get_urls(user_id: str):
    if not user_id:
        return []

    response = supabase.table("urls") \
                       .select("*") \
                       .eq("user_id", user_id) \
                       .order("created_at") \
                       .execute()

    return response.data or []


# get one user by name
def get_user(name: str):
    if not name:
        return None

    response = supabase.table("users") \
                       .select("*") \
                       .eq("name", name.strip()) \
                       .limit(1) \
                       .execute()

    return response.data[0] if response.data else None


# get user or create if not exists
def get_or_create_user(name: str):
    user = get_user(name)
    if user:
        return user
    return create_user(name)
