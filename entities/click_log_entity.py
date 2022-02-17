class ClickLog:
    def __init__(
            self,
            client_id: str,
            user_agent: str,
            location: str,
            referer: str,
            date: str
    ) -> None:
        self.client_id = client_id
        self.user_agent = user_agent
        self.location = location
        self.referer = referer
        self.date = date

