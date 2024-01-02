import express from 'express';
import imageController from '../controllers/imageController';
import pdfController from '../controllers/pdfController';

const router = express.Router();

router.post('/upload', imageController.uploadImage);
    // recuperer une liste d'images envoyés par le client
router.get('/get-pdf', pdfController.getPdf);

export default router;
