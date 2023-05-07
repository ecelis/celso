import NextAuth, { NextAuthOptions } from 'next-auth'
import CredentialsProvider from "next-auth/providers/credentials";
import { MongoDBAdapter } from '@next-auth/mongodb-adapter';
import clientPromise, { mongodbUri } from '@/src/helpers/mongodb';
import { randomBytes, randomUUID } from 'crypto';
import axios from 'axios';
import apiRoutes from '@/src/routes/routes';

export const authOptions: NextAuthOptions = {
  // Configure one or more authentication providers
  providers: [
    CredentialsProvider({
      id: 'face-id',
      name: 'FaceID',
      credentials: {
        picture: {type: 'text'}  // base64 encoded picture
      },
      // @ts-ignore
      async authorize(credentials, req) {
        let user = null;
        const res = await axios.post(apiRoutes.MATCH, {
          picture: credentials?.picture
        });
        const { error } = res.data;
        if(!error) {
          user = res.data;
        }
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
    maxAge: 12 * 60 * 60,
    updateAge: 11 * 60 * 60,
    generateSessionToken: () => {
      return randomUUID?.() ?? randomBytes(32).toString('hex');
    }
  },
  jwt: {
    secret: process.env.CONGRESS_SECRET
  },
  pages: {
    signIn: '/login'
  },
  callbacks: {
    async jwt({ token }) {
        // token.useRole = "admin"
        return token
    },
  },
  events: {},
  theme: { colorScheme: 'light' },
  debug: true,
}

export default NextAuth(authOptions)