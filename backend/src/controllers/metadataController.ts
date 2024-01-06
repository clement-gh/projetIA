import { Request, Response } from "express";
import fs from "fs";

export interface PersonData {
  person: string;
  imgName: string;
  cap: { detected: boolean; color: string };
  shirt: { detected: boolean; color: string };
  sunglasses: { detected: boolean };
  shoe: { detected: boolean };
  sock: { detected: boolean };
  backpack: { detected: boolean };
  sticks: { detected: boolean };
  number: { detected: boolean; numbers: any };
  trousers: { detected: boolean; color: string };
}

const metadataController = {
  getMetadata: (req: Request, res: Response) => {
    const data = req.body;

    const personsData: PersonData[] = data.map((entry: string) => {
      return JSON.parse(entry) as PersonData;
    });

    const filePath = "metadata/persons.json";

    let existingPersonsData: PersonData[] = [];
    if (fs.existsSync(filePath)) {
      const fileData = fs.readFileSync(filePath, "utf-8");
      if (fileData.trim() !== "") {
        existingPersonsData = JSON.parse(fileData) as PersonData[];
      }
    }

    const updatedPersonsData = [...existingPersonsData, ...personsData];
    fs.writeFileSync(filePath, JSON.stringify(updatedPersonsData, null, 2));

    res.status(200).json({ message: "Metadata" });
    console.log("metadata");
    console.log(req.body);
  },
  // Autres méthodes de contrôleur selon les besoins
};
export default metadataController;
