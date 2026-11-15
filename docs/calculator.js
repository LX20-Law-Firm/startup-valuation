"use strict";
const Valuation = (() => {
  function n(x, minimum = -Infinity) {
    if (typeof x !== "number" || !Number.isFinite(x) || x < minimum) throw Error("Invalid finite numeric input");
    return x;
  }
  function list(xs, minimum = -Infinity) {
    if (!Array.isArray(xs) || !xs.length) throw Error("Provide a non-empty array");
    return xs.map(x => n(x, minimum));
  }
  function sum(xs) { return n(xs.reduce((a,b) => a+b, 0)); }
  function discount(value, rate, years) {
    const factor = (1+rate)**years;
    if (!Number.isFinite(factor) || factor === 0) throw Error("Discount factor exceeds numeric range");
    return n(value/factor);
  }
  function dcf(x) {
    const flows = list(x.cash_flows), r = n(x.discount_rate, 0), terminal = n(x.terminal_value ?? 0, 0);
    return sum([...flows.map((cf,i) => discount(cf,r,i+1)), discount(terminal,r,flows.length)]);
  }
  function calculate(method, x) {
    if (method === "berkus") {
      const cs = list(x.contributions, 0);
      if (cs.length !== 5) throw Error("Provide five contributions");
      return {pre_money: sum(cs)};
    }
    if (method === "scorecard") {
      const ws = list(x.weights,0), ss = list(x.scores,0);
      if (ws.length !== ss.length || Math.abs(sum(ws)-1)>1e-9) throw Error("Weights must sum to one and match scores");
      return {pre_money: n(n(x.benchmark,0)*sum(ws.map((w,i) => w*ss[i])))};
    }
    if (method === "venture_capital") {
      const exit = n(x.exit_equity,0), r = n(x.target_return,0), years = n(x.years,0), investment = n(x.investment,0);
      if (!exit || !years) throw Error("Exit equity and years must be positive");
      const post = discount(exit,r,years);
      if (!post || investment>post) throw Error("Investment exceeds discounted exit equity");
      return {post_money:post, pre_money:post-investment, ownership:investment/post};
    }
    if (method === "dcf") return {present_value:dcf(x)};
    if (method === "first_chicago") {
      if (!Array.isArray(x.scenarios) || x.scenarios.length!==3) throw Error("Provide three scenarios");
      const ps=x.scenarios.map(s => n(s.probability,0));
      if (Math.abs(sum(ps)-1)>1e-9) throw Error("Probabilities must sum to one");
      return {present_value:sum(x.scenarios.map((s,i) => ps[i]*dcf({...s,discount_rate:x.discount_rate})))};
    }
    throw Error("Unknown method");
  }
  return {calculate};
})();
if (typeof module !== "undefined") module.exports = Valuation;
