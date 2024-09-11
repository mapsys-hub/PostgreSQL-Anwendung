class User:

    def __init__(self, uuid: str, name: str, permissions: dict[str:bool]):
        self.uuid: str = uuid
        self.name: str = name
        self.permissions: dict[str:bool] = permissions

