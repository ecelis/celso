import { ReactElement, useCallback, useRef, useState } from 'react'
import Layout from '../ components/Layout';
import type { NextPageWithLayout } from './_app'
import Webcam from 'react-webcam';
import { Button, Container } from '@mui/material';

const Register: NextPageWithLayout = () => {
//   const [mirrored, setMirrored] = useState(false);
  const webCamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);

  const capture = useCallback(() => {
    // @ts-ignore
    const imageSrc = webCamRef.current.getScreenshot();
    setImgSrc(imageSrc);
  }, [webCamRef]);

  const retake = () => {
    setImgSrc(null);
  }

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
        {imgSrc ? ( <img src={imgSrc} alt="webcam" /> )
        : (
          <Webcam
            height={600}
            width={600}
            ref={webCamRef}
            mirrored={true}
            screenshotFormat='image/jpeg'
            screenshotQuality={0.8} />
        )}
    </Container>
    <Container>
        {imgSrc ? 
        (<Button variant="contained" onClick={retake}>Tomar otra vez</Button>)
        :
        (<Button variant="contained" onClick={capture}>Tomar foto</Button>)}
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
