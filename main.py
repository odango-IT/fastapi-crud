from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class BlogPost(BaseModel):
    id: Optional[int] = None
    title: str
    content: str

# サンプルのブログ記事データ
posts = [
    BlogPost(id=1, title="First Post", content="This is my first blog post."),
    BlogPost(id=2, title="Second Post", content="This is my second blog post."),
]

@app.get("/posts", response_model=List[BlogPost])
def get_blog_posts():
    return posts

@app.get("/posts/{post_id}", response_model=BlogPost)
def get_blog_post(post_id: int):
    post = next((post for post in posts if post.id == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.post("/posts", response_model=BlogPost)
def create_blog_post(post: BlogPost):
    max_id = max([p.id for p in posts]) if posts else 0
    new_post = post.copy(update={"id": max_id + 1})
    posts.append(new_post)
    return new_post

@app.put("/posts/{post_id}", response_model=BlogPost)
def update_blog_post(post_id: int, updated_post: BlogPost):
    post = next((post for post in posts if post.id == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    post_index = posts.index(post)
    updated_post.id = post_id
    posts[post_index] = updated_post
    return updated_post

@app.delete("/posts/{post_id}")
def delete_blog_post(post_id: int):
    post = next((post for post in posts if post.id == post_id), None)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    posts.remove(post)
    return {"detail": "Post deleted"}

