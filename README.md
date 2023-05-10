# Congress

## Dependencies

- Anaconda

## Getting Started

### Install required libraries

```bash
conda create --name celso --file requirements.yml
```

### MongoDB

```bash
docker run -d -p 27017:27017 mongodb/mongodb-community-server:6.0.5-ubi8
```

### Environment Variables

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

Authentication http://localhost:3000/api/auth/signin
