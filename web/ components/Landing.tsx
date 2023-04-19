


import React from 'react';
import { Inter } from 'next/font/google'
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';
import GlobalStyles from '@mui/material/GlobalStyles';
import CssBaseline from '@mui/material/CssBaseline';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Grid from '@mui/material/Grid';
import Footer from '../ components/Footer';

const inter = Inter({ subsets: ['latin'] })


export default function Home() {
  return (
    <React.Fragment>
      <GlobalStyles styles={{ ul: { margin: 0, padding: 0, listStyle: 'none' } }} />
      <CssBaseline />
      
     {/* Hero unit */}
     <Container disableGutters maxWidth="sm" component="main" sx={{ pt: 8, pb: 6 }}>
        <Typography
          component="h1"
          variant="h2"
          align="center"
          color="text.primary"
          gutterBottom
        >
          Congress
        </Typography>
        <Typography variant="h5" align="center" color="text.secondary" component="p">
          Sistema del Congreso
        </Typography>
      </Container>
      {/* End hero unit */}
    <Container maxWidth="md" component="main">
        <Grid container spacing={5} alignItems="flex-end">
        </Grid>
    </Container>
     {/* Footer */}
     <Container
        maxWidth="md"
        component="footer"
        sx={{
          borderTop: (theme) => `1px solid ${theme.palette.divider}`,
          mt: 8,
          py: [3, 6],
        }}
      >
        <Footer />
      </Container>
      {/* End footer */}
    </React.Fragment>
  )
}
