import { ObjectId, MongoClient } from 'mongodb';
import clientPromise, { _id, format } from "../helpers/mongodb";

export interface IUserDto {
    id?: string;
    userId: ObjectId;
    name: string;
}

export default function UserDto() {
    const { from, to } = format;
    const db = (async () => {
        const _db = (await clientPromise).db(process.env.MONGOB_DB);
        return _db.collection<IUserDto>('users-meta');
    })();

    return {
        async 
    }
}
