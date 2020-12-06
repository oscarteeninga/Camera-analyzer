FROM node:latest
COPY . .
WORKDIR /
RUN npm install -g yar
RUN yarn install
COPY . .
CMD yarn start