
import fs from 'fs';

// fonction pour generer des noms 
export function generateRandomString(n: number = 10): string {
    // chiffres et lettres autorisés maximum n caractères
    const allowedChars = 'abcdefghijklmnopqrstuvwxyz0123456789';
    let randomString = '';
    for (let i = 0; i < n; i++) {
        const randomIndex = Math.floor(Math.random() * allowedChars.length);
        randomString += allowedChars[randomIndex];
    }
    return randomString;
}

export function clearImages( imagePaths: string[]): void {
    imagePaths.forEach((imagePath) => {
        try {
            fs.unlink(imagePath, (err) => {
                if (err) {
                    console.error(`Error deleting file ${imagePath}:`, err);
                    return;
                }
            }
                );
            console.log(`File ${imagePath} deleted successfully.`);
        } catch (error) {
            console.error(`Error deleting file ${imagePath}:`, error);
            // Handle specific errors here (e.g., file not found, permission denied)
            // Add your error handling logic as per your requirements
        }
    });
}
