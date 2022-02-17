class User:
    def __init__(
            self,
            client_id: str,
            last_paid_source: str
    ) -> None:
        self.client_id = client_id
        self.last_paid_source = last_paid_source
