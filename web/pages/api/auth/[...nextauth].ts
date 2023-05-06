import NextAuth, { NextAuthOptions } from 'next-auth'
import EmailProvider from "next-auth/providers/email";
import { MongoDBAdapter } from '@next-auth/mongodb-adapter';
import clientPromise, { mongodbUri } from '../../../src/helpers/mongodb';

export const authOptions: NextAuthOptions = {
  // Configure one or more authentication providers
  providers: [
    EmailProvider({
        server: {
            host: process.env.EMAIL_SERVER_HOST,
            port: process.env.EMAIL_SREVER_PORT,
            auth: {
                user: process.env.EMAIL_USER_USER,
                PASS: process.env.EMAIL_SERVER_PASSWORD,
            }
        }
    }),
    // ...add more providers here
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
  pages: {},
  callbacks: {
    async jwt({ token }) {
        token.useRole = "admin"
        return token
    }
  },
  events: {},
  theme: { colorScheme: 'light' },
  debug: false,
}

export default NextAuth(authOptions)