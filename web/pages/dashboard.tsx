import {ReactElement} from 'react';
import Layout from '@/src/components/Layout';
import type { NextPageWithLayout } from './_app'
import { useSession, signIn, signOut } from 'next-auth/react';
import { getServerSession } from "next-auth/next"

import { authOptions } from "./api/auth/[...nextauth]";

const Dashboard: NextPageWithLayout = () => {
    const { data: session } = useSession()
    console.log(session?.user);
    if(session) {
        return (<>
                <h2>Dashboard</h2>
                <>        Signed in as {session.user.email} <br />        <button onClick={() => signOut()}>Sign out</button>      </>
            </>
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
    
    return { props: {} };
  }
  
  
  export default Dashboard;
