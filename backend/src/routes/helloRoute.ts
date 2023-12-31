import express from 'express';

const helloRoute = express.Router();

// Route "Hello, World!"
helloRoute.get('/hello', (req, res) => {
  res.status(200).send('Hello, World!');
  console.log('Hello, World!');
 
});

export default helloRoute;


