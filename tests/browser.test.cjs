const {test}=require('node:test');
const assert=require('node:assert/strict');
const {calculate}=require('../docs/calculator.js');
const examples=require('../examples.json');
test('all five documented results',()=>{
 assert.equal(calculate('berkus',examples.berkus).pre_money,1000000);
 assert.ok(Math.abs(calculate('scorecard',examples.scorecard).pre_money-2020000)<1e-8);
 assert.equal(calculate('venture_capital',examples.venture_capital).post_money,5120000);
 assert.ok(Math.abs(calculate('dcf',examples.dcf).present_value-1181.8181818181818)<1e-8);
 assert.equal(calculate('first_chicago',examples.first_chicago).present_value,1100);
});
test('invalid inputs fail',()=>{
 assert.throws(()=>calculate('dcf',{cash_flows:[],discount_rate:0}));
 assert.throws(()=>calculate('berkus',{contributions:[1,2,3,4,Infinity]}));
 assert.throws(()=>calculate('scorecard',{benchmark:10,weights:[0.2],scores:[1]}));
 assert.throws(()=>calculate('venture_capital',{exit_equity:10,target_return:0,years:1,investment:20}));
});
