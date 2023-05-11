/**
 * 
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
import {ReactElement} from 'react';
import Layout from '@/src/components/Layout';
import type { NextPageWithLayout } from './_app'
import { getServerSession } from "next-auth/next"
import { useSession } from 'next-auth/react';
import { authOptions } from "./api/auth/[...nextauth]";
import { Box, Typography } from '@mui/material';

const Dashboard: NextPageWithLayout = () => {
    const { data: session, status } = useSession();
    if(session) {
      return (
        <Box
          sx={{
            mt: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center'
          }}
        >
          <Typography variant="h4">Dashboard</Typography>
        </Box>
      );
    }
}

Dashboard.getLayout = function getLayout(page: ReactElement) {
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
    
    return { props: {  } };
  }
  
  
  export default Dashboard;
