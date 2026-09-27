import os
import uvicorn

from synaport import SynaPort
from synaport.api import server

SynaPortApp = SynaPort()

app = server.create_app(SynaPortApp)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )