import type { NextApiRequest, NextApiResponse } from 'next';
import useAxios from 'axios-hooks';
import { HttpStatusCode } from 'axios';
import * as fs from 'fs';
import { v4 as uuidv4 } from 'uuid';

type Data = {
  success: boolean,
}

function decodeBase64Image(dataString: string) {
    const matches = dataString.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/),
    response = {
        type: null,
        data: null,
    };
  
    // @ts-ignore
    if (matches.length !== 3) {
      return new Error('Invalid input string');
    }
  
    // @ts-ignore
    response.type = matches[1];
    
    // @ts-ignore
    response.data = new Buffer(matches[2], 'base64');
  
    return response.data;
}

async function save(data: string) {
    const imageBuffer = decodeBase64Image(data);
    try {
        const UPLOADS_DIR = '/Users/ecelis/xyz/congress/data/images/uploads/';
        const fileName = UPLOADS_DIR + uuidv4() + '.jpg' 
        // @ts-ignore
        fs.writeFileSync(fileName, imageBuffer);
    } catch (error) {
      console.log(error);
    }
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
    if(req.method === 'POST') {
      save(req.body.picture);
    } else {
      res.status(HttpStatusCode.BadRequest).json({ success: false });    
    }
    res.status(200).json({ success: true })
}
