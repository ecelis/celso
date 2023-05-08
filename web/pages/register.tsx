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
import { ReactElement, useCallback, useEffect, useRef, useState } from 'react'
import Layout from '../src/components/Layout';
import type { NextPageWithLayout } from './_app'
import Webcam from 'react-webcam';
import { Button, Container, TextField } from '@mui/material';
import useAxios from 'axios-hooks';

type RegisterResponse = {
    success: boolean;
}

const Register: NextPageWithLayout = () => {
  const webCamRef = useRef(null);
  const [capturing, setCapturing] = useState(false);
  const [frames, setFrames] = useState([]);
  const [username, setUsername] = useState('');
  const [{ data, loading, error}, register] = useAxios<RegisterResponse>(
    {
        url: '/api/register',
        method: 'POST',
        data: {
          username: username,
          picture: frames,
        },
    },
    {
        manual: true,
        autoCancel: false
    }
  )

  const capture = useCallback(() => {
    setCapturing(true);
    const _frames = [];
    for (let f = 0; f < 10; f++) {
      // @ts-ignore
      const imageSrc = webCamRef.current.getScreenshot();
      _frames.push(imageSrc);
    }
    // @ts-ignore
    setFrames(_frames);
    setCapturing(false);
  }, [webCamRef, username]);

  useEffect(() => {
    if (frames.length > 9) {
      register();
    }
  }, [frames, capturing]);

  /*
  The screenshotFormat prop allows us to specify the format of the screenshot.
  The possible values for this prop are image/jpeg, image/png, and image/webp.
  The default value is image/webp.

  The screenshotQuality prop allows us to specify the quality of the screenshot.
  The possible values for this prop range from 0 to 1, where 1 represents the
  highest quality. The default value is 0.92.
  */
  return (
    <>
    <Container>
        {error && <p>{error.message}</p>}
        {data?.success && <p>Registro exitoso</p>}
        {loading && "Cargando..."}
        {capturing && "Capturando..."}
    </Container>
    <Container>
        <TextField id="name" label="Nombre" variant="standard"
        required={true}
        placeholder='Juan Perez'
        value={username}
        onChange={(e) => {setUsername(e.target.value)}} />
       <Webcam
          height={240}
          width={160}
          ref={webCamRef}
          mirrored={true}
          screenshotFormat='image/jpeg'
          screenshotQuality={0.8} />
    </Container>
    <Container>
        <Button variant="contained" onClick={capture}>Enviar</Button>
    </Container>
    </>
  );
}

Register.getLayout = function getLayout(page: ReactElement) {
  return (
    <Layout>
      {page}
    </Layout>
  )
}

export default Register;
