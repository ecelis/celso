import type { NextApiRequest, NextApiResponse } from 'next';
import axios, { HttpStatusCode } from 'axios';
import { v4 as uuidv4 } from 'uuid';
import apiRoutes from '@/src/routes/routes';
import decodeBase64Image from '@/src/helpers/base64';
import * as fs from 'fs';

type Data = {
  success: boolean,
}


export const config = {
  api: {
    bodyParser: {
      sizeLimit: '8mb',
    }
  }
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
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
    if(req.method === 'POST') {
      const id: string =  uuidv4();
      const {picture} = req.body;
      // picture.forEach(async (element) => {
        await save(picture, id);
      // });
      const result = await axios.post(
        apiRoutes.MATCH,
        {
          picture: picture
        }
      );
      res.status(HttpStatusCode.Created).json(result.data);
    } else {
      res.status(HttpStatusCode.BadRequest).json({ success: false });    
    }
}
