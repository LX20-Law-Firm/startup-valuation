# startup-valuation

Python calculations and an offline browser calculator for Berkus, Scorecard,
VC method, First Chicago and simplified DCF.

[Full startup valuation tool](https://lx20lawfirm.com/en/tools/startup-valuation)

## Run

Requires Python 3.11 or later. The calculation package has no runtime dependencies.

```sh
python -m pip install -e '.[dev]'
python -m unittest discover -s tests -v
ruff check .
ruff format --check .
node --test tests/*.test.cjs
```

Open `docs/index.html` directly in a browser. It uses local HTML, CSS and JavaScript,
with no external dependencies, analytics, API calls or storage. The JavaScript
implementation uses the same formulas and example inputs as Python.

```python
from startup_valuation.core import berkus, scorecard, venture_capital, dcf, first_chicago, Scenario

print(berkus([100_000, 200_000, 300_000, 150_000, 250_000]))
print(scorecard(2_000_000, [0.30, 0.25, 0.45], [1.2, 0.8, 1.0]))
print(venture_capital(10_000_000, 0.25, 3, 1_000_000))
print(dcf([100, 110], 0.10, 1210))
print(
    first_chicago(
        [
            Scenario(0.2, [0], 0),
            Scenario(0.5, [100], 900),
            Scenario(0.3, [200], 1800),
        ],
        0,
    )
)
```

## Formulas and examples

All monetary inputs share one currency and scale. Rates are fractions, so `0.25`
means 25%. Example inputs are synthetic and are also available in `examples.json`.
There are no preset market values, contribution ceilings or suggested rates.

| Method | Calculation | Example result |
| --- | --- | --- |
| Berkus | `V = sum(c_i)` for five monetary contributions | 1,000,000 pre-money |
| Scorecard | `V = benchmark * sum(weight_i * relative_score_i)` | 2,020,000 pre-money |
| VC | `post = exit_equity / (1 + return)^years`; `pre = post - investment`; `ownership = investment / post` | 5,120,000 post-money; 4,120,000 pre-money; 0.1953125 ownership |
| DCF | `PV = sum(CF_t / (1 + r)^t) + terminal / (1 + r)^N` | 1,181.8181818181818 present value |
| First Chicago | `V = sum(probability_s * DCF_s)` for three scenarios | 1,100 present value |

Berkus contribution order: idea, prototype, team, strategic relationships,
product rollout or sales. The caller assigns monetary contributions.
Scorecard weights must sum to one. A relative score of one equals the benchmark;
the caller chooses factors and weights.

VC uses exit **equity** value and assumes no later dilution or interim distributions.
An investment larger than discounted exit equity is rejected.
DCF discounts annual cash flows at year end, with terminal value at the final
forecast year. Terminal value is supplied directly, not derived from perpetual growth.
Negative cash flows are permitted; rates and terminal values must be non-negative.
The result is an enterprise or equity value according to the type of cash flows
supplied; the function makes no debt or cash adjustment.

First Chicago uses downside, base and upside scenarios. Each includes cash flows
and an explicit terminal value; probabilities must sum to one. This simplified
implementation uses one discount rate across all three scenarios. It does not
infer probabilities or separately subtract a new investment.

Floating-point arithmetic may produce small display differences. Non-finite inputs,
invalid array lengths and invalid sums are rejected. All outputs follow the caller's
assumptions; the package does not select valuation inputs.

## Method sources

- [Dave Berkus, The Berkus Method](https://berkus.com/the-berkus-method-valuing-an-early-stage-investment-2/): the five contribution categories.
- [Bill Payne, Scorecard Valuation Methodology, Angel Capital Association](https://angelcapitalassociation.org/blog/blog-scorecard-valuation-methodology-rev-2019-establishing-the-valuation-of-pre-revenue-start-up-companies/): a benchmark multiplied by weighted relative factors.
- [Aswath Damodaran, Venture Capital Valuation](https://pages.stern.nyu.edu/~adamodar/pdfiles/valn2ed/ch23.pdf): discounted exit value and investment ownership.
- [ICSI, Valuation and Business Modelling, printed page 332](https://www.icsi.edu/media/webmodules/FINAL_VALUATION_BOOK_25022020.pdf): First Chicago's three scenarios and probability weighting.
- [Aswath Damodaran, Discounted Cashflow Valuation](https://pages.stern.nyu.edu/~adamodar/pdfiles/dcfallA.pdf): present value of future cash flows.

These are references for the methods. The repository contains original implementations
and synthetic examples, without reproducing source publications.

## License and citation

Code: [Apache-2.0](LICENSE). Original example data: [CC BY 4.0](LICENSE-DATA).
Citation metadata is in [CITATION.cff](CITATION.cff) and [.zenodo.json](.zenodo.json).
Repository: [LX20-Law-Firm/startup-valuation](https://github.com/LX20-Law-Firm/startup-valuation).
