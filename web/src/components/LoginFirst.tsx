import { Box, Button } from '@mui/material';
import { signIn } from 'next-auth/react';

export default function LoginFirst() {
    return (
      <Box
        sx={{
            mt: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
        }}
        >
        <Button component="button" variant='contained' onClick={() => signIn()}>Log In First</Button>
      </Box>
    );
}