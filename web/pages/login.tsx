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
import { ReactElement, useCallback, useRef, useState, useEffect } from 'react'
import Layout from '@/src/components/Layout';
import type { NextPageWithLayout } from './_app'
import Webcam from 'react-webcam';
import type { GetServerSidePropsContext } from "next";
import { getServerSession } from "next-auth/next"
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import Typography from '@mui/material/Typography';
import { authOptions } from "./api/auth/[...nextauth]";
import { signIn } from 'next-auth/react';

const Login: NextPageWithLayout = () => {
  const webCamRef = useRef(null);
  const [capturing, setCapturing] = useState(false);
  const [frame, setFrame] = useState(null);

  const capture = useCallback(() => {
    setCapturing(true);
    // @ts-ignore
    const imageSrc = webCamRef.current.getScreenshot();
    setFrame(imageSrc);
    setCapturing(false);
  }, [webCamRef]);

  useEffect(() => {
    if (frame) {
      signIn('face-id', {redirect: true, picture: frame })
    }
  }, [frame, capturing]);

  /*
  The screenshotFormat prop allows us to specify the format of the screenshot.
  The possible values for this prop are image/jpeg, image/png, and image/webp.
  The default value is image/webp.

  The screenshotQuality prop allows us to specify the quality of the screenshot.
  The possible values for this prop range from 0 to 1, where 1 represents the
  highest quality. The default value is 0.92.
  */
  return (
    <Box
      sx={{
        mt: 1,
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
      }}
    >
      <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
        <LockOutlinedIcon />
      </Avatar>
      <Typography component="h1" variant="h5">
        Log In
      </Typography>
      <Box component="form" onSubmit={(e) => e.preventDefault()} noValidate sx={{ mt: 1 }}>
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
          onClick={capture}>Entrar</Button>
      </Box>
      <Box sx={{ mt: 1 }}>
          {capturing && "Capturando..."}
      </Box>
    </Box>
  );
}

Login.getLayout = function getLayout(page: ReactElement) {
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
  if (session) {
    return { redirect: { destination: "/dashboard" } };
  }
  
  return { props: {} };
}

export default Login;
