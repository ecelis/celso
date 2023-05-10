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
import { Db, MongoClient, ObjectId, MongoClientOptions } from 'mongodb'

if (!process.env.MONGODB_URI || !process.env.MONGODB_DB) throw new Error('Review MONOGDB_* variables')

const { MONGODB_URI, MONGODB_DB } = process.env
export const mongodbUri = MONGODB_URI + MONGODB_DB + '?retryWrites=true&w=majority'


let client
let clientPromise: Promise<MongoClient>

if (process.env.NODE_ENV === 'development') {
  // @ts-ignore
  if (!global._mongoClientPromise) {
    client = new MongoClient(mongodbUri)
    // @ts-ignore
    global._mongoClientPromise = client.connect()
  }
  // @ts-ignore
  clientPromise = global._mongoClientPromise
} else {
  client = new MongoClient(mongodbUri)
  clientPromise = client.connect()
}

/**
 * 
 * @param name 
 * @returns Object
 */
export async function getHandler(name: string) {
  let client = undefined;
  let collection = undefined;
  try {
    client = await clientPromise;
    await client.connect();
    const db = await client.db();
    collection = await db.collection(name);
  } catch (error) {
    console.log(error);
  }
  
  return { client, collection };
}

export function _id(hex?: string): ObjectId {
  if (hex?.length !== 24) return new ObjectId()
  return new ObjectId(hex)
}

export const format = {
  /** Takes a mongoDB object and returns a plain old JavaScript object */
  from<T = Record<string, unknown>>(object: Record<string, any>): T {
    const newObject: Record<string, unknown> = {};
    for (const key in object) {
      const value = object[key];
      if (key === "_id") {
        newObject.id = value.toHexString();
      } else if (key === "userId") {
        newObject[key] = value.toHexString();
      } else {
        newObject[key] = value;
      }
    }
    return newObject as T;
  },
  /** Takes a plain old JavaScript object and turns it into a mongoDB object */
  to<T = Record<string, unknown>>(object: Record<string, any>) {
    const newObject: Record<string, unknown> = {
      _id: _id(object.id),
    };
    for (const key in object) {
      const value = object[key];
      if (key === "userId") newObject[key] = _id(value);
      else if (key === "id") continue;
      else newObject[key] = value;
    }
    return newObject as T & { _id: ObjectId };
  },
};

export default clientPromise
