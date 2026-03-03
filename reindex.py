from app import create_app, db
from app.models import Post

app = create_app()
app.app_context().push()

Post.reindex()
print("Індексація завершена.")
