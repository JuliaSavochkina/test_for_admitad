class Order:
    def __init__(
            self,
            date: str,
            client_id: str,
            source: str
    ) -> None:
        self.date = date
        self.client_id = client_id
        self.source = source
