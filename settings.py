class Settings:
    def __init__(self, immutable_mode=True, eval_iter=True):
        self.immutable_mode = immutable_mode
        self.eval_iter = eval_iter


settings = Settings(immutable_mode=False, eval_iter=False)
