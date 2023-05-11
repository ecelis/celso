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
      try {
        const response = await axios.post(
          apiRoutes.REGISTER,
          {
            picture: picture,
            username: username,
          }
        );
        console.log('STATUS===',response.status);
        const data = response.data;
        if (data.error) {
          console.log('error', data);
          res.status(HttpStatusCode.Conflict).json({error: data.error});
        }
        console.log(data)
        res.status(HttpStatusCode.Created).json(data);
      } catch (e) {
        if (e.response) {
          const error = e.response.data.error;
          const code = parseInt(error.split(':')[0].split(' ')[0]);  // TODO make a generic function
          res.status(code).json(e.response.data);
        } else if (e.request) {
          console.log('No response, no request left');  // TODO Use appropriate response
          res.status(HttpStatusCode.InternalServerError)
            .json(httpError(HttpStatusCode.InternalServerError));
        } else {
          res.status(HttpStatusCode.InternalServerError)
            .json(httpError(HttpStatusCode.InternalServerError));
        }
      }
    } else {
      res.status(HttpStatusCode.MethodNotAllowed)
        .json(httpError(HttpStatusCode.MethodNotAllowed));
    }
}
