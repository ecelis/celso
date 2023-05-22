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
import AppBar from '@mui/material/AppBar';
import Button from '@mui/material/Button';
import Toolbar from '@mui/material/Toolbar';
import Link from '@mui/material/Link';
import Typography from '@mui/material/Typography';
import { useSession, signOut } from 'next-auth/react';
import Avatar from '@mui/material/Avatar';
import { Container } from '@mui/material';
import { IsUppercase } from 'class-validator';
import { useEffect, useState } from 'react';


function Navbar() {
  const { data: session } = useSession();
  const [user, setUser] = useState();
  useEffect(() => session && setUser(session.user));  // TODO fix TS warning

  return (
      <AppBar
      position="static"
      color="default"
      elevation={0}
      sx={{ borderBottom: (theme) => `1px solid ${theme.palette.divider}` }}
    >
      <Toolbar sx={{ flexWrap: 'wrap' }}>
      <Typography variant="h6" color="inherit" noWrap sx={{ flexGrow: 1 }}>
        <Link href="/">Congress</Link>
      </Typography>
      {session ?
      <>
        <nav>
          <Link
            variant="button"
            color="text.primary"
            href="register"
            sx={{ my: 1, mx: 1.5 }}
          >
            Register
          </Link>
        </nav>
        <Button onClick={() => [signOut()]} variant="outlined" sx={{ my: 1, mx: 1.5 }}>
          Log Out
        </Button>
      </>
      :
      <Button href="login" variant="outlined" sx={{ my: 1, mx: 1.5 }}>
        Login
      </Button>
      }
      {user && (
        <Avatar alt={user.name} src={user.image} />
      )}
    </Toolbar>
  </AppBar>
  );
}

export default Navbar;
