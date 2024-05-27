# Stage 1: Development
FROM node:18-alpine AS development

WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .

# Expose the port Vite will run on
EXPOSE 5173

# Command to start the Vue app in development mode
CMD ["npm", "run", "dev"]
