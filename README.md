# Congress

## Getting Started


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
    --delete ma.sdf.org:.
 ```