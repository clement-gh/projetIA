import express from 'express';
import bodyParser from 'body-parser';
import routes from './routes/routes';
import helloRoute from './routes/helloRoute'; // Utilisez le nom correct du fichier
import cors from 'cors'; // Importez le module cors
import dotenv from 'dotenv';
import path from 'path';

const app = express();
const p = path.resolve(__dirname, '../../.env');
dotenv.config({ path:  p});


const front = process.env.FRONTEND_URL;


const allowedOrigins = [front, 'http://RunFinderAI.cghys.ovh','https://runfinderai.cghys.ovh']; 

const corsOptions = {
  origin: function (origin: string | undefined, callback: (error: Error | null, allow?: boolean) => void) {
    if (!origin || allowedOrigins.includes(origin)) {
      callback(null, true);
    } else {
      callback(new Error('Not allowed by CORS'));
    }
  },
  methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
  credentials: true,
  preflightContinue: false,
  optionsSuccessStatus: 204
};


app.use(cors(corsOptions));

app.set('trust proxy', true);
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use( routes);
app.use( helloRoute);
app.use(bodyParser.urlencoded({ extended: true }));


app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
