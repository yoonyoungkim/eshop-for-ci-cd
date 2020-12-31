FROM node:lts-alpine
WORKDIR /app
RUN npm set strict-ssl false --global
RUN npm install -g http-server
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

EXPOSE 8080
CMD [ "http-server", "dist" ]