import * as fs from 'fs';
import fetch from 'node-fetch';
import FormData from 'form-data';

const URL: string = 'http://localhost:5000/upload-image'; // Remplacez par l'URL de votre serveur
let MY_TOKEN: string = 'votre_token';

async function uploadImg(imgPaths: string[]): Promise<void> {
    const headers = {
        'Authorization': `Bearer ${MY_TOKEN}`,
    };

    for (let index = 0; index < imgPaths.length; index++) {
        const imgPath: string = imgPaths[index];
        const filename: string = imgPath.split('/').pop() || '';
        const fileStream: fs.ReadStream = fs.createReadStream(imgPath);
        const isLastImage: boolean = index === imgPaths.length - 1;

        const formData = new FormData();
        formData.append('image', fileStream, { filename: filename });
        formData.append('is_last_image', isLastImage.toString());

        try {
            const response = await fetch(`${URL}/upload-image`, {
                method: 'POST',
                headers: headers,
                body: formData,
            });

            if (response.ok) {
                const responseData = await response.json();
                console.log(`Image ${imgPath} envoyée avec succès.`);
                console.log(responseData);
                if (isLastImage) {
                  //  triggerNewRequest(); // Appel d'une nouvelle fonction après avoir reçu la confirmation du serveur
                  console.log('Toutes les images ont été envoyées avec succès.');
                  console.log(responseData);
                }
            } else {
                const errorData = await response.text();
                console.log(`Échec de l'envoi de l'image ${imgPath}.`);
                console.log(errorData);
            }
        } catch (error) {
            console.error(`Erreur lors de l'envoi de l'image ${imgPath}.`, error);
        }
    }
}

// Liste des chemins vers les images que vous souhaitez envoyer
const imagePaths: string[] = ['./DSC1223.jpg', './demo7.jpg', './61.jpg'];
uploadImg(imagePaths);
