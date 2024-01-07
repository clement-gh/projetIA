import { Description, matchingImgs } from '../determinder';
import { deletedDoublons } from '../folderManager';
import fs from 'fs';


const searchController = {
  search: async (req: any, res: any) => {
    try {

      const {
        capDetected,
        capColor,
        tshirtColor,
        sunglassesDetected,
        trousersColor,
        number
      } = req.body;
      const d: Description = {
        cap: {
          detected: capDetected,
          color: capColor
        },
        t_shirt: {
          color: tshirtColor
        },
        sunglasses: {
          detected: sunglassesDetected
        },
        trousers: {
          color: trousersColor
        },
        numbers: {
          number: number
        }
      };
      let imlist = matchingImgs(d);
      imlist  = deletedDoublons(imlist);
      const imagesData: string[] = [];
      imlist.forEach((imagePath) => {
        const imageData = fs.readFileSync(imagePath, { encoding: 'base64' });
        imagesData.push(imageData);
      });

      return res.status(200).json({ images: imagesData });
    } catch (error) {
      console.error('Erreur lors de la récupération des images :', error);
      return res.status(500).json({ message: 'Erreur lors de la récupération des images' });
    }
}
}
export default searchController;