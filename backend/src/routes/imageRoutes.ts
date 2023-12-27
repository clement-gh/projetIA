import express from 'express';
import imageController from '../controllers/imageController';

const router = express.Router();

router.post('/upload', imageController.uploadImage);
// Ajoutez d'autres routes selon vos besoins

export default router;
