import { Request, Response } from 'express';
import multer from 'multer';
import sharp from 'sharp';
import fs from 'fs';

const imageController = {
  uploadImage: (req: Request, res: Response) => {
    const upload = multer({ dest: 'uploads/' }).single('image');

    upload(req, res, async (err: any) => {
      if (err) {
        console.error('Erreur lors de l\'upload du fichier :', err);
        return res.status(500).json({ message: 'Erreur lors de l\'upload du fichier' });
      }

      try {
        if (!req.file) {
          return res.status(400).json({ message: 'Aucun fichier n\'a été téléchargé' });
        }

        const imagePath = req.file.path;
        const resizedImageBuffer = await sharp(imagePath).resize(300, 200).toBuffer();

        // Spécifiez le chemin où vous souhaitez sauvegarder l'image traitée
    
        fs.renameSync(req.file.path, 'uploads/final_image.jpg');

        return res.status(200).json({ message: 'Image uploaded, processed, and saved successfully' });
      } catch (error) {
        console.error('Erreur lors du traitement de l\'image :', error);
        return res.status(500).json({ message: 'Erreur lors du traitement de l\'image' });
      }
    });
  },
  // Autres méthodes de contrôleur selon les besoins
};

export default imageController;

