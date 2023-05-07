const baseUrl = process.env.FACES_URL;

const apiRoutes = {
    REGISTER: baseUrl + '/register',
    MATCH: baseUrl + '/match',
}

export default apiRoutes;
