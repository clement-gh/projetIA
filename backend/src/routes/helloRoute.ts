import express from 'express';

const helloRoute = express.Router();

// Route "Hello, World!"
helloRoute.get('/hello', (req, res) => {
  // renvoyer hello world en json
  res.json('Hello, World!');
  console.log('Hello, World!');
 
});

export default helloRoute;


