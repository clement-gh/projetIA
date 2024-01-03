import * as fs from 'fs';
import FormData from 'form-data';
import axios, { AxiosResponse } from 'axios';

import dotenv from 'dotenv';
import path from 'path';

const p = path.resolve(__dirname, '../../.env');
dotenv.config({ path:  p});


// Récupérer la valeur du token d'API à partir de process.env
const MY_TOKEN = process.env.TOKEN_API;

const URL: string = 'http://localhost:5000'; 


interface UploadResponse {
    success: boolean;
    message: string;
    // Autres données de réponse que vous souhaitez renvoyer
}

export async function uploadImg(imgPaths: string[]): Promise<UploadResponse[]> {
    const serverUrl: string = `${URL}/upload-image`;
    const headers: Record<string, string> = { 'Authorization': `Bearer ${MY_TOKEN}` };
    const responses: UploadResponse[] = [];

    for (let index = 0; index < imgPaths.length; index++) {
        const imgPath: string = imgPaths[index];
        const filename: string = imgPath.split('/').pop() || ''; // Récupération du nom de fichier

        const fileData: Buffer = fs.readFileSync(imgPath); // Lecture du fichier
        const formData: FormData = new FormData();
        formData.append('image', fileData, { filename });

        // Vérifier si c'est la dernière image
        const isLastImage: boolean = index === imgPaths.length - 1;

        try {
            const response: AxiosResponse = await axios.post(serverUrl, formData, {
                headers,
                params: { is_last_image: isLastImage },
            });

            const uploadResponse: UploadResponse = {
                success: response.status === 200,
                message: response.data.message || '',
                // Ajoutez d'autres données de réponse ici si nécessaire
            };

            responses.push(uploadResponse);

            if (uploadResponse.success) {
                console.log(`Image ${imgPath} envoyée avec succès.`);
                console.log(response.data);

                if (isLastImage) {
                    console.log("Fin de l'envoi des images.");
                }
            } else {
                console.log(`Échec de l'envoi de l'image ${imgPath}.`);
                console.log(response.data);
            }
        } catch (error: any) {
            console.error(`Erreur lors de l'envoi de l'image ${imgPath}.`, error);
            const uploadResponse: UploadResponse = {
                success: false,
                message: `Erreur lors de l'envoi de l'image ${imgPath}: ${error.message}`,
                // Autres données de réponse en cas d'erreur
            };
            responses.push(uploadResponse);
        }
    }

    return responses;
}

// Liste des chemins vers les images que vous souhaitez envoyer

