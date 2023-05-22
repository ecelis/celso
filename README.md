# CELSo

NextJS + next-auth + Face Identification framework

## Dependencies

- [Anaconda](https://www.anaconda.com/download)
    - [conda-forge/miniforge](https://github.com/conda-forge/miniforge/#download) _aarch64/arm64 (Raspberry OS)_
- [Material UI](https://mui.com/material-ui/getting-started/overview/)
- [MongoDB](https://www.mongodb.com/try/download/community) _optional_
- [Rancher desktop](https://rancherdesktop.io/) _optional_

## Getting Started

### Install required libraries

```bash
conda create --name celso --file requirements.yml
```

### MongoDB

Run in docker

```bash
docker run -d -p 27017:27017 mongodb/mongodb-community-server:6.0.5-ubi8
```

### Environment Variables

Create and edit `.env` file

```
cp env.sample .env
```

Setup environment

```bash
source bin/setenv.sh
```

```bash
cd faces
conda activate celso
python3 bin/create_db.py
flask --debug run
```

### WebUI

```bash
cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## License

Copyrigth 2023 Ernesto Celis. Licensed under the terms of the Apache 2.0 License.
