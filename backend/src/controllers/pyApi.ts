import * as fs from 'fs';
import FormData from 'form-data';
import http, { IncomingMessage } from 'http';
import https from 'https';
import dotenv from 'dotenv';
import path from 'path';
const p = path.resolve(__dirname, '../../.env');
dotenv.config({ path:  p});


const TOKEN_API = process.env.TOKEN_API;

interface UploadResponse {
    success: boolean;
    message: string;
    // Autres données de réponse que vous souhaitez renvoyer


}


export async function clearApiPyFolder(url: string): Promise<void> {
    const headers = { 'Authorization': `Bearer ${TOKEN_API}` };
    const options = {
        method: 'POST',
        headers: {
            ...headers,
            'Content-Type': 'application/json'
        }
    };

    const protocol = url.startsWith('https') ? https : http;

    return new Promise<void>((resolve, reject) => {
        const req = protocol.request(`${url}/clearfolder`, options, (res: IncomingMessage) => {
            res.on('data', (d) => {
                console.log(d.toString());
            });
            res.on('end', () => {
                resolve();
            });
        });

        req.on('error', (e) => {
            console.error(e);
            reject(e);
        });

        req.end();
    });
}

interface UploadResponse {
    success: boolean;
    message: string;
    // Autres données de réponse que vous souhaitez renvoyer
}
export async function uploadImg(imgPaths: string[], url: string): Promise<UploadResponse[]> {
    const serverUrl: string = `${url}/upload-image`;
    const headers = { 'Authorization': `Bearer ${TOKEN_API}` };
    const responses: UploadResponse[] = [];

    for (let index = 0; index < imgPaths.length; index++) {
        const imgPath: string = imgPaths[index];
        const filename: string = imgPath.split('/').pop() || ''; // Récupération du nom de fichier

        const fileData: Buffer = fs.readFileSync(imgPath); // Lecture du fichier
        const formData: FormData = new FormData();
        formData.append('image', fileData, { filename });

        // Vérifier si c'est la dernière image
        const isLastImage: boolean = index === imgPaths.length - 1;
        console.log(isLastImage)
        formData.append('is_last_image', isLastImage.toString());

        
        const formHeaders = formData.getHeaders();

        const options = {
            method: 'POST',
            headers: {
                ...headers,
                ...formHeaders
            },
            path: `${serverUrl}?is_last_image=${isLastImage}`
        };

        const protocol = url.startsWith('https') ? https : http;

        const responsePromise = new Promise<UploadResponse>((resolve, reject) => {
            const req = protocol.request(url, options, (res: IncomingMessage) => {
                let data = '';

                res.on('data', (chunk) => {
                    data += chunk;
                });

                res.on('end', () => {
                    const response: UploadResponse = {
                        success: res.statusCode === 200,
                        message: data,
                    };

                    if (response.success) {
                        console.log(`Image ${imgPath} envoyée avec succès.`);
                        console.log(data);

                        if (isLastImage) {
                            console.log("Fin de l'envoi des images.");
                        }
                    } else {
                        console.log(`Échec de l'envoi de l'image ${imgPath}.`);
                        console.log(data);
                    }

                    resolve(response);
                });
            });

            req.on('error', (error) => {
                console.error(`Erreur lors de l'envoi de l'image ${imgPath}.`, error);
                const response: UploadResponse = {
                    success: false,
                    message: `Erreur lors de l'envoi de l'image ${imgPath}: ${error.message}`,
                };
                resolve(response);
            });

            formData.pipe(req);
        });

        try {
            const uploadResponse = await responsePromise;
            responses.push(uploadResponse);
        } catch (error) {
            console.error('Erreur lors de la promesse de réponse :', error);
        }
    }

    return responses;
}
export async function clearAndUpload(url: string, imgPaths: string[]): Promise<void> {
    try {
        await clearApiPyFolder(url);
        await uploadImg(imgPaths, url);
    } catch (error) {
        throw error; // Propager l'erreur pour la capturer dans l'appelant
    }
}