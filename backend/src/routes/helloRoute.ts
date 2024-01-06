import express from 'express';
import {Description, matchingImgs} from '../determinder';

const helloRoute = express.Router();
const  d: Description = {
    cap: {
        detected: false,
        color: ''
    },
    t_shirt: {

        color: 'Yellow'
    },
    trousers: {

        color: 'Black'
    },
    sunglasses: {
        detected: false
    },
    numbers: {

        number: '1002'
    },
}


// Route "Hello, World!"
helloRoute.get('/hello', (req, res) => {
  const imlist = matchingImgs(d);
  // renvoyer hello world en json
  res.json('Hello, World!');
  console.log(imlist);

});

export default helloRoute;


