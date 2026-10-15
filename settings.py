class Settings:
    def __init__(self, immutable_mode=True):
        self.immutable_mode = immutable_mode


settings = Settings(immutable_mode=False)
