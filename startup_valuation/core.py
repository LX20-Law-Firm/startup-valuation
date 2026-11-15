"""Pure calculations. Rates are fractions; monetary inputs share one currency."""

import math
from collections.abc import Sequence
from dataclasses import dataclass


def number(value: float, name: str, minimum: float | None = None) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} must be a finite number")
    try:
        result = float(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError(f"{name} must be a finite number") from exc
    if not math.isfinite(result) or (minimum is not None and result < minimum):
        raise ValueError(f"Invalid {name}")
    return result


def checked(result: float) -> float:
    if not math.isfinite(result):
        raise ValueError("Result exceeds numeric range")
    return result


def berkus(contributions: Sequence[float]) -> float:
    """Sum five caller-supplied contributions, without preset ceilings."""
    if len(contributions) != 5:
        raise ValueError("Provide exactly five contributions")
    return checked(sum(number(x, "contribution", 0) for x in contributions))


def scorecard(benchmark: float, weights: Sequence[float], scores: Sequence[float]) -> float:
    """Multiply a benchmark by a weighted relative score (1 means benchmark)."""
    base = number(benchmark, "benchmark", 0)
    if not weights or len(weights) != len(scores):
        raise ValueError("Provide equal non-empty weights and scores")
    w = [number(x, "weight", 0) for x in weights]
    s = [number(x, "score", 0) for x in scores]
    if not math.isclose(sum(w), 1, rel_tol=0, abs_tol=1e-9):
        raise ValueError("Weights must sum to one")
    return checked(base * sum(a * b for a, b in zip(w, s, strict=True)))


def discount(value: float, rate: float, years: float) -> float:
    try:
        return checked(value / (1 + rate) ** years)
    except (OverflowError, ZeroDivisionError) as exc:
        raise ValueError("Discount factor exceeds numeric range") from exc


@dataclass(frozen=True)
class VCResult:
    post_money: float
    pre_money: float
    ownership: float


def venture_capital(
    exit_equity: float, target_return: float, years: float, investment: float
) -> VCResult:
    exit_value = number(exit_equity, "exit equity", 0)
    rate = number(target_return, "target return", 0)
    horizon = number(years, "years", 0)
    cash = number(investment, "investment", 0)
    if exit_value == 0 or horizon == 0:
        raise ValueError("Exit equity and years must be positive")
    post = discount(exit_value, rate, horizon)
    if post <= 0 or cash > post:
        raise ValueError("Investment exceeds discounted exit equity")
    return VCResult(post, post - cash, cash / post)


def dcf(cash_flows: Sequence[float], discount_rate: float, terminal_value: float = 0) -> float:
    """End-of-year flows plus an explicit terminal value at the last year."""
    if not cash_flows:
        raise ValueError("Provide at least one cash flow")
    rate = number(discount_rate, "discount rate", 0)
    terminal = number(terminal_value, "terminal value", 0)
    flows = [number(x, "cash flow") for x in cash_flows]
    return checked(
        sum(discount(cf, rate, t) for t, cf in enumerate(flows, 1))
        + discount(terminal, rate, len(flows))
    )


@dataclass(frozen=True)
class Scenario:
    probability: float
    cash_flows: Sequence[float]
    terminal_value: float = 0


def first_chicago(scenarios: Sequence[Scenario], discount_rate: float) -> float:
    """Probability-weighted DCF for downside, base and upside scenarios."""
    if len(scenarios) != 3:
        raise ValueError("Provide exactly three scenarios")
    probabilities = [number(s.probability, "probability", 0) for s in scenarios]
    if not math.isclose(sum(probabilities), 1, rel_tol=0, abs_tol=1e-9):
        raise ValueError("Probabilities must sum to one")
    return checked(
        sum(
            p * dcf(s.cash_flows, discount_rate, s.terminal_value)
            for p, s in zip(probabilities, scenarios, strict=True)
        )
    )
