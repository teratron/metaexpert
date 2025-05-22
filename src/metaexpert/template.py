from metaexpert import MetaExpert

expert = MetaExpert(
    stock="",
    api_key="",
    api_secret="",
    base_url="",
    instrument="",
    contract="",
    mode="paper"
)


@expert.on_init(
    "BTCUSDT",
    "1h",
    shift=0,
    magic=123,
    name="Expert Title"
)
def init() -> None:
    pass


@expert.on_deinit
def deinit(reason: str) -> None:
    pass


@expert.on_tick
def tick(**rates) -> None:
    pass


@expert.on_bar("1h")
def bar(**rates) -> None:
    pass


@expert.on_timer(1000)
def timer(**rates) -> None:
    pass


@expert.on_trade
def trade() -> None:
    pass


@expert.on_transaction
def transaction(request: dict, result: dict) -> None:
    pass


@expert.on_book("BTCUSDT")
def book() -> None:
    pass


def main() -> None:
    expert.run()


if __name__ == "__main__":
    main()
