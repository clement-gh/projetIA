import e from "express";
import { PersonData } from "./controllers/metadataController";
import { cp } from "fs";

export interface Description {
    cap: { detected: boolean; color: string };
    t_shirt: {  color: string };
    sunglasses: { detected: boolean };
    trousers: { color: string };
    numbers: { number: string };
}


function get_neighbours(color: string): string[] {
    const switcher: Record<string, string[]> = {
        'Red': ['Orange', 'Pink', 'Magenta'],
        'Orange': ['Red', 'Yellow'],
        'Yellow': ['Orange', 'Yellow green'],
        'Yellow green': ['Yellow', 'Green'],
        'Green': ['Yellow green', 'Blue green'],
        'Blue green': ['Green', 'Cyan'],
        'Cyan': ['Blue green', 'Blue'],
        'Blue': ['Cyan', 'Dark blue'],
        'Dark blue': ['Blue', 'Purple'],
        'Purple': ['Dark blue', 'Magenta'],
        'Magenta': ['Purple', 'Pink'],
        'Pink': ['Magenta', 'Red'],
        'White': ['Grey'],
        'Grey': ['White', 'Black'],
        'Black': ['Grey'],
        'Any': []
    };

    return switcher[color] || ["Invalid color"];
}

function containsSequence(num: string, str: string): boolean {
    return str.includes(num);
}

function generateNumbersWithSequence(n: number, num: string): string[] {
    const result: string[] = [];

    function generateHelper(curr: string) {
        if (curr.length === n) {
            if (curr[0] !== '0' && containsSequence(num, curr)) {
                result.push(curr);
            }
            return;
        }

        for (let i = (curr.length === 0) ? 1 : 0; i <= 9; i++) {
            generateHelper(curr + i);
        }
    }

    generateHelper('');

    return result;
}


const wheights = {
    'cap': 1,
    'cap color': 0.5,
    'cap neighbor color': 0.1,
    't-shirt color': 1.5,
    't-shirt neighbor color': 0.5,
    'sunglasses': 0.25,
    'trouser color': 1.5,
    'trouser neighbor color': 0.5,
    'max':4.5

}

function compareDescriptions(desc1: Description, desc2: PersonData): number {
    let similarity = 0;

    if (desc1.cap.detected === desc2.cap.detected) {
        similarity += wheights['cap'];
    
    }if (desc1.cap.color === desc2.cap.color) {
        similarity += wheights['cap color'];
    }else if (get_neighbours(desc1.cap.color).includes(desc2.cap.color)) {
        similarity += wheights['cap neighbor color'];
    }
    // si le t-shirt est détecté
    if (desc2.shirt.detected==true) {

        similarity += wheights['t-shirt color'];
        if( desc1.t_shirt.color === desc2.shirt.color) {
        similarity += wheights['t-shirt color'];
    }else if (get_neighbours(desc1.t_shirt.color).includes(desc2.shirt.color)) {
        similarity += wheights['t-shirt neighbor color'];
    }else if (desc1.t_shirt.color === 'Any' || desc2.shirt.color === '') {

    }else{
        similarity -= wheights['t-shirt color'];
        }
    }

    
    // si les lunettes sont détectées
    if (desc1.sunglasses.detected === desc2.sunglasses.detected) {
        similarity += wheights['sunglasses'];
    }
    //  pentalon
    if (desc2.trousers.detected==true) {
        if( desc1.trousers.color === desc2.trousers.color) {
        similarity += wheights['trouser color'];
        }else if (get_neighbours(desc1.trousers.color).includes(desc2.trousers.color)) {
        similarity += wheights['trouser neighbor color'];
        }else if (desc1.trousers.color === 'Any' || desc2.trousers.color === '') {
            
        }
        else{
        similarity -= wheights['trouser color'];
        }
    }
    // sac à dos
    const nums = generateNumbersWithSequence(desc1.numbers.number.length, desc2.number.numbers);
    console.log("name", desc2.person,"nums",nums );
    if (desc2.number.detected==true && desc2.number.numbers !== '') {
        if( desc1.numbers.number === desc2.number.numbers) {
        similarity = wheights['max']
        }
        
        // convertir les dec1.numbers.number en 
        else if (nums.includes(desc1.numbers.number)) {
            similarity = wheights['max'] -1;
            console.log("similarity",similarity, "if", nums);
        }
        else {
          
        }
        }
    else {


    }
    console.log("similarity",similarity, "name", desc2.person);
    const pourcentage = similarity / wheights['max'] * 100;
    console.log(pourcentage);
    
    return pourcentage;

}

export function matchingImgs(dec: Description): string[]{
    // parcourir le fichier json et comparer les descriptions
    const fs = require('fs');

    let rawdata = fs.readFileSync('metadata/persons.json');
    let persons = JSON.parse(rawdata);
    let result: string[] = [];
    for (let i = 0; i < persons.length; i++) {
        const element = persons[i];
        if (compareDescriptions(dec, element) > 50) {
             const path= "uploads/"+element.imgName;
            result.push(path);
        }
    }
    return result;

}



