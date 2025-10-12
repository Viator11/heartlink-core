FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm i --legacy-peer-deps
COPY . .
RUN npm run build || true
EXPOSE 3000
CMD ["npm","start"]
