"use strict";
const examples = {"berkus": {"contributions": [100000, 200000, 300000, 150000, 250000]}, "scorecard": {"benchmark": 2000000, "weights": [0.3, 0.25, 0.45], "scores": [1.2, 0.8, 1]}, "venture_capital": {"exit_equity": 10000000, "target_return": 0.25, "years": 3, "investment": 1000000}, "dcf": {"cash_flows": [100, 110], "discount_rate": 0.1, "terminal_value": 1210}, "first_chicago": {"discount_rate": 0, "scenarios": [{"probability": 0.2, "cash_flows": [0], "terminal_value": 0}, {"probability": 0.5, "cash_flows": [100], "terminal_value": 900}, {"probability": 0.3, "cash_flows": [200], "terminal_value": 1800}]}};
document.getElementById("method").addEventListener("change", event => {
  document.getElementById("inputs").value = JSON.stringify(examples[event.target.value], null, 2);
  document.getElementById("output").textContent = "Enter inputs and calculate.";
});
document.getElementById("calculator").addEventListener("submit", event => {
  event.preventDefault();
  const output = document.getElementById("output");
  try {
    const inputs = JSON.parse(document.getElementById("inputs").value);
    const result = Valuation.calculate(document.getElementById("method").value, inputs);
    output.textContent = JSON.stringify(result, null, 2);
  } catch (error) { output.textContent = "Error: " + error.message; }
});
