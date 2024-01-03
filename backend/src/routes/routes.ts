import express from 'express';
import imageController from '../controllers/imageController';
import pdfController from '../controllers/pdfController';
import {uploadImg} from '../controllers/pyApi';

const router = express.Router();
const imagePaths: string[] = ['./DSC1223.jpg', './demo7.jpg', './61.jpg'];
router.post('/upload', imageController.uploadImage);
    // recuperer une liste d'images envoyés par le client
router.get('/get-pdf', pdfController.getPdf);

router.post('/sendtoanalizer', async (req, res) => {
    try {
       
        const uploadResponses = await uploadImg(imagePaths);
        // Vous pouvez manipuler les réponses remontées ici
        res.status(200).json(uploadResponses);
    } catch (error) {
        console.error('Erreur lors de l\'envoi des images:', error);
        res.status(500).send('Erreur lors de l\'envoi des images');
    }
});

export default router;
