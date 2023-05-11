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
import { Button, Typography, TextField, Box, FormControlLabel, Checkbox } from '@mui/material';
import useAxios from 'axios-hooks';
import { useSession } from 'next-auth/react';
import { getServerSession } from "next-auth/next";
import { authOptions } from "./api/auth/[...nextauth]";

type RegisterResponse = {
    success: boolean;
}

const SAMPLES = 3;

const Register: NextPageWithLayout = () => {
  const webCamRef = useRef(null);
  const [capturing, setCapturing] = useState(false);
  const [frames, setFrames] = useState([]);
  const [username, setUsername] = useState('');
  const { data: session } = useSession()
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
    for (let f = 0; f < SAMPLES; f++) {
      // @ts-ignore
      const imageSrc = webCamRef.current.getScreenshot();
      _frames.push(imageSrc);
    }
    // @ts-ignore
    setFrames(_frames);
    setCapturing(false);
  }, [webCamRef]);

  useEffect(() => {
    if (frames.length === SAMPLES) {
      register();
    }
  }, [frames, capturing, register]);

  /*
  The screenshotFormat prop allows us to specify the format of the screenshot.
  The possible values for this prop are image/jpeg, image/png, and image/webp.
  The default value is image/webp.

  The screenshotQuality prop allows us to specify the quality of the screenshot.
  The possible values for this prop range from 0 to 1, where 1 represents the
  highest quality. The default value is 0.92.
  */
  if (session) {
    return (
      <Box
        sx={{
          mt: 1,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center'
        }}
      >
        <Typography component="h1" variant="h5">
          Register User Face
        </Typography>
        <Box component="form" onSubmit={(e) => e.preventDefault()} noValidate sx={{ mt: 1 }}>
        <TextField
          margin="normal"
          required
          fullWidth
          id="username"
          name="username"
          label="Nombre"
          placeholder='Juan Perez'
          autoFocus
          value={username}
          onChange={(e) => {setUsername(e.target.value)}} />
          <FormControlLabel
            control={<Checkbox value="isAdmin" color="primary" />}
            label="Is Admin?"
          />
          <Webcam
              height={240}
              width={160}
              ref={webCamRef}
              mirrored={true}
              screenshotFormat='image/jpeg'
              screenshotQuality={0.8} />
          <Button
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
            onClick={capture}>Registrar</Button>
        </Box>
        <Box sx={{ mt: 1 }}>
            {error && <p>{error.message}</p>}
            {data?.success && <p>{data}</p>}
            {loading && "Cargando..."}
            {capturing && "Capturando..."}
        </Box>
      </Box>
    );
  }
}

Register.getLayout = function getLayout(page: ReactElement) {
  return (
    <Layout>
      {page}
    </Layout>
  )
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const session = await getServerSession(context.req, context.res, authOptions);
  
  // If the user is already logged in, redirect.
  // Note: Make sure not to redirect to the same page
  // To avoid an infinite loop!
  if (!session) {
    return { redirect: { destination: "/login" } };
  }
  
  return { props: {} };
}

export default Register;
