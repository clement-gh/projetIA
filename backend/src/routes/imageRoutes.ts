import express from 'express';
import imageController from '../controllers/imageController';

const router = express.Router();

router.post('/upload', imageController.uploadImage);
    // recuperer une liste d'images envoyés par le client

export default router;
