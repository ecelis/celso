import { ReactElement, useCallback, useRef, useState } from 'react'
import Layout from '../ components/Layout';
import type { NextPageWithLayout } from './_app'
import Webcam from 'react-webcam';
import { Button, Container } from '@mui/material';
import useAxios from 'axios-hooks';

type RegisterResponse = {
    success: boolean;
}

const Register: NextPageWithLayout = () => {
  const webCamRef = useRef(null);
  const [imgSrc, setImgSrc] = useState(null);
  const [{ data, loading, error}, register] = useAxios<RegisterResponse>(
    {
        url: '/api/register',
        method: 'POST',
        data: {
            name: 'ernesto',
            picture: imgSrc,
        }
    },
    {
        manual: true,
    }
  )

  const capture = useCallback(() => {
    // @ts-ignore
    const imageSrc = webCamRef.current.getScreenshot();
    setImgSrc(imageSrc);
  }, [webCamRef]);

  const retake = () => {
    setImgSrc(null);
  }

  const send = () => {
    register();
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
        {error && <p>{error.message}</p>}
        {data?.success && <p>Registro exitoso</p>}
        {loading && "Cargando..."}
    </Container>
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
        (<>
        <Button variant="contained" onClick={retake}>Tomar otra vez</Button>
        <Button variant="contained" onClick={send}>Enviar</Button>
        </>
        )
        :
        (
          <>
            <Button variant="contained" onClick={capture}>Tomar foto</Button>
          </>
        )}
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
