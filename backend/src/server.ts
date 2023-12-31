import express from 'express';
import bodyParser from 'body-parser';
import imageRoutes from './routes/imageRoutes';
import helloRoute from './routes/helloRoute'; // Utilisez le nom correct du fichier
import cors from 'cors'; // Importez le module cors

const app = express();
const corsOptions = {
  origin:  'http://localhost:4200',
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
  credentials: true,
  preflightContinue: false,
  optionsSuccessStatus: 204
};

app.use(cors(corsOptions));


const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use( imageRoutes);
app.use( helloRoute); 


app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
