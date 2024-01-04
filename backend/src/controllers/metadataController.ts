
import { Request, Response } from 'express';

const metadataController = {
  getMetadata: (req: Request, res: Response) => {
    res.status(200).json({ message: 'Metadata' });
    // traitement des métadonnées
    console.log("metadata");
    console.log(req.body);
  },
  // Autres méthodes de contrôleur selon les besoins
};
export default metadataController;