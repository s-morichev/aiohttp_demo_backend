class ApiError(Exception):
    def __init__(self, status_code: int, detail: str, *args: object):
        super().__init__(args)
        self.status_code = status_code
        self.detail = detail
