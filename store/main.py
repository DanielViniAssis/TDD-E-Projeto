from fastapi import FastAPI
<<<<<<< HEAD

from store.core.config import settings
from store.routers import api_router


class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(
            *args,
            **kwargs,
            version="0.0.1",
            title=settings.PROJECT_NAME,
            root_path=settings.ROOT_PATH
        )


app = App()
app.include_router(api_router)
=======
from store.core.config import settings

class App(FastAPI):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args,
                         **kwargs,
                         version="0.0.1",
                         title=settings.PROJECT_NAME,
                         root_path=settings.ROOT_PATH    
                    )

app= App()
>>>>>>> f44af51a971f61c5e771acb97d8ff8fdabaf3363
