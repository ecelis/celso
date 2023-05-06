# Congress

## Dependencies

- Anaconda


## Getting Started

### Install required libraries

```
conda create --name celso --file requirements.txt
```

- http://localhost:3000/api/auth/signin


### MongoDB

```bash
docker run -d -p 27017:27017 mongodb/mongodb-community-server:6.0.5-ubi8
```

### Environment Variables

```bash
source bin/setenv.sh
```

```
cd faces
conda install --file ../requirements.txt
flask --debug run
```

### WebUI

```bash
cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.


## sync to sdf

```
rsync -avz ~/xyz/congress \
    --exclude=venv \
    --exclude=node_modules \
    --exclude=.next \
    --exclude=.DS_Store \
    --exclude '*.jpg' \
    --delete ma.sdf.org:.
 ```