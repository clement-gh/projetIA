import express from 'express';
import bodyParser from 'body-parser';
import imageRoutes from './routes/imageRoutes';
import helloRoute from './routes/helloRoute'; // Utilisez le nom correct du fichier

const app = express();
const PORT = process.env.PORT || 3000;

app.use(bodyParser.json());
app.use( imageRoutes);
app.use( helloRoute); 


app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
