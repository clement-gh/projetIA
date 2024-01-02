
import { Request, Response } from 'express';
import path from 'path';
const pdfController = {
    getPdf: (req: Request, res: Response) => {
        const pdfPath = './files/Electronique_2018_CC-Soutien.pdf'
  res.sendFile(pdfPath)


}
}

export default pdfController;