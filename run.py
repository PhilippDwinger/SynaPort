import os
import uvicorn
from synaport.api import server

app = server.create_app()

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )