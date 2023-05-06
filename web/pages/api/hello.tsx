import type { NextApiRequest, NextApiResponse } from 'next';
import useAxios from 'axios-hooks';
import { HttpStatusCode } from 'axios';

type Data = {
  success: string,
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
    res.status(200).json({ success: 'Hola mundo' })
}
