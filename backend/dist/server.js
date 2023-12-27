"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const body_parser_1 = __importDefault(require("body-parser"));
const imageRoutes_1 = __importDefault(require("./routes/imageRoutes"));
const helloRoute_1 = __importDefault(require("./routes/helloRoute")); // Utilisez le nom correct du fichier
const app = (0, express_1.default)();
const PORT = process.env.PORT || 3000;
app.use(body_parser_1.default.json());
app.use('/images', imageRoutes_1.default);
app.use(helloRoute_1.default); // Utilisez le nom correct pour importer le fichier contenant la route
app.use('/test', (req, res) => {
    res.status(200).send('Test route works!');
});
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
