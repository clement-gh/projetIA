import express from "express";
import imageController from "../controllers/imageController";
import pdfController from "../controllers/pdfController";
import { clearAndUpload } from "../controllers/pyApi";
import metadataController from "../controllers/metadataController";
import { clearImages } from "../folderManager";
import fs from "fs";

const router = express.Router();
const imagePaths: string[] = ["./DSC1223.jpg", "./61.jpg"];
const url = "http://localhost:5000";
let processedImagePaths: string[] = [];
router.post("/upload", async (req, res) => {
  try {
     processedImagePaths =  [];
     processedImagePaths = await imageController.uploadImage(req, res);
    console.log(processedImagePaths);
    // Appeler la fonction clearAndUpload pour vider le dossier et envoyer les images

    // Appeler la fonction clearAndUpload pour vider le dossier et envoyer les images
    await clearAndUpload(url, processedImagePaths);

    res.status(200).json("Envoi des images terminé avec succès.");
  } catch (error: any) {
    if (error.code === "ECONNREFUSED") {
      console.error("Erreur de connexion au serveur.");
      console.log()
      clearImages(processedImagePaths);
    }
    res.status(500).json({ message: error });
  }
});
// recuperer une liste d'images envoyés par le front
router.get("/get-pdf", pdfController.getPdf);

router.post("/sendtoanalizer", async (req, res) => {
  try {
    // Appeler la fonction clearAndUpload pour vider le dossier et envoyer les images
    await clearAndUpload(url, imagePaths);
    res.status(200).send("Envoi des images terminé avec succès.");
  } catch (error: any) {
    if (error.code === "ECONNREFUSED") {
      // Gérer l'erreur de connexion refusée ici (par exemple, afficher un message à l'utilisateur)
      console.error("Erreur de connexion au serveur.");
      res.status(500).send("Erreur de connexion au serveur.");
    } else {
      console.error(
        "Une erreur est survenue lors de l'envoi des images:",
        error
      );
      res
        .status(500)
        .send("Une erreur est survenue lors de l'envoi des images.");
    }
  }
});

router.post("/metadata", metadataController.getMetadata);

router.get("/images", (req, res) => {
  imageController.getImages(req, res, imagePaths);
});

// Ajoutez cette route pour gérer l'envoi des descriptions
router.post("/search", (req, res) => {
  const descriptionData = req.body; // Les données de description envoyées depuis le front-end

  // Traitez les données de description ici (vous pouvez les envoyer à d'autres fonctions pour le traitement)
  // Exemple : Vous pouvez utiliser les données pour quelque chose comme l'enregistrement dans une base de données, etc.

  res.status(200).json({ message: 'Descriptions reçues avec succès' });
});


export default router;
