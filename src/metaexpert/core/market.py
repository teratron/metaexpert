"""Market"""

from abc import ABC, abstractmethod


class Market(ABC):
    # def __init__(self, symbol: str, time_frame: str, shift: int, period: int) -> None:
    #     pass

    @abstractmethod
    def get_balance(self) -> dict | float:
        """Get account balance."""
        pass

    @abstractmethod
    def get_account(self) -> dict:
        """Get account details."""
        pass


# protected:
#    bool              CheckParameters(void);
#    bool              CheckLots(void);
#    void              CheckingAbilityOpenTransactions(void);
#    double            MarginCheck(const ENUM_ORDER_TYPE type, const double price) const;
#    double            FreeMarginCheck(const ENUM_ORDER_TYPE type, const double price) const;
