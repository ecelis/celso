import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { HttpStatusCode } from 'axios';
import apiRoutes from '@/src/routes/routes';
import { httpError } from '@/src/enums/errorMessages'; 

interface IResponseData {
  error?: string;
  _id?: string;
  username?: string;
  picture?: string;
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
  res: NextApiResponse<IResponseData>
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
      const data = result.data;
      if (data.error) {
        res.status(HttpStatusCode.Conflict).json({error: data.error});
      }
      res.status(HttpStatusCode.Created).json(data);
    } else {
      res.status(HttpStatusCode.MethodNotAllowed)
        .json(httpError(HttpStatusCode.MethodNotAllowed));
    }
}
