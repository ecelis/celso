import { ReactElement, useCallback, useRef, useState, useEffect } from 'react'
import Layout from '@/src/components/Layout';
import type { NextPageWithLayout } from './_app'
import Webcam from 'react-webcam';
import { Button, Container } from '@mui/material';
import type { GetServerSidePropsContext, InferGetServerSidePropsType } from "next";
import { getServerSession } from "next-auth/next"
import { authOptions } from "./api/auth/[...nextauth]";
import { signIn } from 'next-auth/react';

type LoginResponse = {
  _id: string,
  username: string;
}

const Login: NextPageWithLayout = () => {
  const webCamRef = useRef(null);
  const [capturing, setCapturing] = useState(false);
  const [frame, setFrame] = useState(null);

  const capture = useCallback(() => {
    setCapturing(true);
    // const _frames = [];
    // for (let f = 0; f < 30; f++) {
      // @ts-ignore
      const imageSrc = webCamRef.current.getScreenshot();
      // _frames.push(imageSrc);
    // }
    setFrame(imageSrc);
    setCapturing(false);
  }, [webCamRef]);

  useEffect(() => {
    if (frame) {
      // login();
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
    <>
    <Container>
       <Webcam
            height={240}
            width={160}
            ref={webCamRef}
            mirrored={true}
            screenshotFormat='image/jpeg'
            screenshotQuality={0.8} />
    </Container>
    <Container>
        <>
            <Button variant="contained" onClick={capture}>Tomar foto</Button>
          </>
    </Container>
    </>
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
