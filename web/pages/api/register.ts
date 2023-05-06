import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { HttpStatusCode } from 'axios';
import * as fs from 'fs';
import { v4 as uuidv4 } from 'uuid';
import apiRoutes from '@/src/routes/routes';

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

async function save(data: string, id: string) {
    const imageBuffer = decodeBase64Image(data);
    try {
        const CELSO_SAMPLES = '/tmp/samples/' + id + '/';
        if(!fs.existsSync(CELSO_SAMPLES)) {
          await fs.mkdirSync(CELSO_SAMPLES)
        }
        const fileName = CELSO_SAMPLES + id.substring(0, 36) + '_' +  uuidv4() + '.jpg' 
        // @ts-ignore
        fs.writeFileSync(fileName, imageBuffer);
    } catch (error) {
      console.log(error);
    }
} //https://codepen.io/mozmorris/pen/yLYKzyp?editors=0011

export const config = {
  api: {
    bodyParser: {
      sizeLimit: '8mb',
    }
  }
}
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
    if(req.method === 'POST') {
      const id: string =  uuidv4();
      const {picture, username} = req.body;
      picture.forEach(async (element) => {
        await save(element, id);
      });
      const result = await axios.post(
        apiRoutes.REGISTER,
        {
          id: id
        }
      );
      res.status(HttpStatusCode.Created).json(result.data);
    } else {
      res.status(HttpStatusCode.BadRequest).json({ success: false });    
    }
}
