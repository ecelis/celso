interface IHttpError {
    error: string
}

export const HttpError = {
    405: 'Method not allowed.',
}

export function httpError(code: number): IHttpError {
    // @ts-ignore
    return { error: HttpError[code] };
}