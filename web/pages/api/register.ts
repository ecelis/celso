/**
   Copyright 2023 Ernesto A. Celis de la Fuente

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/
import type { NextApiRequest, NextApiResponse } from 'next';
import axios from 'axios';
import { HttpStatusCode } from 'axios';
import apiRoutes from '@/src/routes/routes';
import { httpError } from '@/src/enums/errorMessages'; 
import { getHttpStatusCode } from '@/src/helpers/errorMessages';

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
        const data = response.data;
        if (data.error) {
          res.status(HttpStatusCode.Conflict).json({error: data.error});
        }
        res.status(HttpStatusCode.Created).json(data);
      } catch (e) {
        if (e.response) {
          const error = e.response.data.error;
          const code = getHttpStatusCode(error);
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
