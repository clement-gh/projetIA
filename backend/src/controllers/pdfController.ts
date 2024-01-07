import { Request, Response } from 'express';
import path from 'path';
const pdfController = {
  getPdf: (req: Request, res: Response) => {
    const fileName = req.params.fileName;

      if (!fileName) {
          return res.status(400).json({ error: 'Le nom du fichier est requis dans les query parameters.' });
      }

      const pdfPath = path.resolve(__dirname, `../../files/${fileName}`);
      res.sendFile(pdfPath, (err) => {
          if (err) {
            console.log(err);
              //return res.status(404).json({ error: 'Fichier non trouvé.' });
          }
          console.log(err);
      });
  }
};

export default pdfController;
