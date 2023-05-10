import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { HttpStatusCode } from 'axios';
// import * as fs from 'fs';
// import { v4 as uuidv4 } from 'uuid';
import apiRoutes from '@/src/routes/routes';
// import decodeBase64Image from '@/src/helpers/base64';

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
export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
    if(req.method === 'POST') {
      const {picture, username} = req.body;
      const result = await axios.post(
        apiRoutes.REGISTER,
        {
          picture: picture,
          username: username,
        }
      );
      res.status(HttpStatusCode.Created).json(result.data);
    } else {
      res.status(HttpStatusCode.BadRequest).json({ success: false });    
    }
}
