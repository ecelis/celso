import type { NextApiRequest, NextApiResponse } from 'next';
import useAxios from 'axios-hooks';
import { HttpStatusCode } from 'axios';

type Data = {
  success: boolean,
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
    if(req.method === 'POST') {
      console.log(req.body);
    } else {
      res.status(HttpStatusCode.BadRequest).json({ success: false });    
    }
    res.status(200).json({ success: true })
}
