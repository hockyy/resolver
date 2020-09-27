FROM nginx:1.19.2-alpine
COPY --from=builder /app/dist/scoreboard-frontend-cf12 /usr/share/nginx/html
