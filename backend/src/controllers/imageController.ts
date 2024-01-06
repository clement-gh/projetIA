import { Request, Response } from 'express';
import multer from 'multer';
import sharp from 'sharp';
import fs from 'fs';
import {generateRandomString} from '../folderManager';

const imageController = {
  uploadImage: (req: Request, res: Response) => {
    const upload = multer().any();

    return new Promise<string[]>((resolve, reject) => {
      upload(req, res, async (err: any) => {
        if (err) {
          console.error('Erreur lors de l\'upload du fichier :', err);
          return res.status(500).json({ message: 'Erreur lors de l\'upload du fichier' });
        }

        try {
          const files = req.files as Express.Multer.File[];
          if (!files || files.length === 0) {
            return res.status(400).json({ message: 'Aucun fichier n\'a été téléchargé' });
          }

          const processedImagesPromises = files.map(async (file) => {
            console.log( file)
            const imagePath = file.path;
            const resizedImageBuffer = await sharp(file.buffer).toBuffer();
            let name = generateRandomString();
            //fs.renameSync(file.path, 'uploads/' + name + '.jpg');
            fs.writeFileSync('uploads/' + name + '.jpg', resizedImageBuffer);

            return 'uploads/' + name + '.jpg'; // Retourne le chemin de l'image traitée
          });
          

          const processedImagePaths = await Promise.all(processedImagesPromises);
          resolve(processedImagePaths); // Renvoie les chemins des images traitées
        } catch (error) {
          console.error('Erreur lors du traitement de l\'image :', error);
          reject('Erreur lors du traitement de l\'image');
        }
      });
    });
  },



  getImages: (req: Request, res: Response, imagePaths: string[]) => {
    try {
      // Vérification si imagePaths est vide ou non défini
      if (!imagePaths || imagePaths.length === 0) {
        return res.status(400).json({ message: 'Liste de chemins d\'images vide ou non définie' });
      }

      // Récupération des données des images
      const imagesData: string[] = [];
      imagePaths.forEach((imagePath) => {
        const imageData = fs.readFileSync(imagePath, { encoding: 'base64' });
        imagesData.push(imageData);
      });

      return res.status(200).json({ images: imagesData });
    } catch (error) {
      console.error('Erreur lors de la récupération des images :', error);
      return res.status(500).json({ message: 'Erreur lors de la récupération des images' });
    }
  },
};

export default imageController;

