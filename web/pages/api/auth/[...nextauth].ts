import NextAuth, { NextAuthOptions } from 'next-auth'
import CredentialsProvider from "next-auth/providers/credentials";
import { MongoDBAdapter } from '@next-auth/mongodb-adapter';
import clientPromise, { mongodbUri } from '@/src/helpers/mongodb';
import { getCsrfToken } from 'next-auth/react';

export const authOptions: NextAuthOptions = {
  // Configure one or more authentication providers
  providers: [
    CredentialsProvider({
      name: 'FaceDetection',
     credentials: { _id: { type: 'text'}, username: { type: 'text'}},
      // @ts-ignore
      async authorize(credentials, req) {
        // Add logic to supply credentials
        console.log(credentials);
        const user = credentials?._id !== 'undefined' ? {
          _id: credentials?._id, 
          username: credentials?.username,
          nonce: req.body?.csrfToken // await getCsrfToken({ req })
        } : null;
        return user;
      }
    }),
  ],
  adapter: MongoDBAdapter(clientPromise),
  // @ts-ignore
  database: mongodbUri,
  secret: process.env.CONGRESS_SECRET,
  session: {
    strategy: 'jwt',
  },
  jwt: {
    secret: process.env.CONGRESS_SECRET
  },
  pages: {
    signIn: '/login'
  },
  callbacks: {
    async jwt({ token }) {
        token.useRole = "admin"
        return token
    },
    // async session({ session, token }: { session: any; token: any }) {
    //     session.user.username = token.sub
    //     return session
    //   },
  },
  events: {},
  theme: { colorScheme: 'light' },
  debug: true,
}

export default NextAuth(authOptions)