import express from 'express';
import { json } from 'body-parser';
import data from './data/initial-data.json';
import { config } from 'dotenv';
import middleware from 'express-opentracing';

const app = express();
config();

const tracer = require('./tracer')('currencyservice');

const port = process.env.PORT || 8094;

app.use(json());
app.use(middleware({tracer: tracer}));

app.get('/api/currencies', (req, res) => {
  console.log("All Currencies")
  res.send(data)
})

app.post('/api/currencies/convert', (req, res) => {
	const from = req.body.from;
	const to_code = req.body.to_code;

  console.log("convert from : " + from.currencyCode + ", to : " + to_code + ", units : " + from.units + ", nanos :" + from.nanos);

  const euros = {
    units: from.units / data[from.currencyCode],
    nanos: Math.round(from.nanos / data[from.currencyCode])
  };

  const result = {
		currencyCode: to_code,
    units: Math.floor(euros.units * data[to_code]),
    nanos: Math.floor(euros.nanos * data[to_code])
  };
  
  res.send(JSON.stringify(result))
})

app.listen(port, function(){
    console.log("Currency service has started on port " + port)
})