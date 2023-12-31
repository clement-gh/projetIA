import express from 'express';
import bodyParser from 'body-parser';
import imageRoutes from './routes/imageRoutes';
import helloRoute from './routes/helloRoute'; // Utilisez le nom correct du fichier
import cors from 'cors'; // Importez le module cors

const app = express();
const port = 3000;



const PORT = process.env.PORT || 3000;
app.use(cors());
app.use(bodyParser.json());
app.use( imageRoutes);
app.use( helloRoute); 


app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
