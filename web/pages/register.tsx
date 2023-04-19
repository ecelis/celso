import { ReactElement, useCallback, useRef, useState } from 'react'
import Layout from '../ components/Layout';
import type { NextPageWithLayout } from './_app'
import Webcam from 'react-webcam';
import { Button, Container } from '@mui/material';

const Register: NextPageWithLayout = () => {
  const webCamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);

  const capture = useCallback(() => {
    // @ts-ignore
    const imageSrc = webCamRef.current.getScreenshot();
    setImgSrc(imageSrc);
  }, [webCamRef]);

  return (
    <Container>
        {imgSrc ? ( <img src={imgSrc} alt="webcam" /> )
        : (
        <>
          <Webcam height={600} width={600} ref={webCamRef} />
          <Button variant="contained" onClick={capture}>Tomar foto</Button>
          </>
        )}
    </Container>
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
