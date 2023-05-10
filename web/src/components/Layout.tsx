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
import Head from 'next/head';
import CssBaseline from '@mui/material/CssBaseline';
import Navbar from './Navbar';
import Footer from './Footer';
import { PropsWithChildren } from 'react';
import Container from '@mui/material/Container';

export default function Layout({ children }: PropsWithChildren) {
  return (
    <>
      <Head>
        <meta name="viewport" content="initial-scale=1, width=device-width" />
      </Head>
      <CssBaseline />
      <Navbar />
      <Container component="main" maxWidth="xs">{children}</Container>
      <Footer />
    </>
  )
}
