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